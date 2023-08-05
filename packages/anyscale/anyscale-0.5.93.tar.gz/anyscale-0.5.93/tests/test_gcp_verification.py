import copy
import ipaddress
import json
from pathlib import Path
import re
import sys
from threading import Thread
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple
from unittest.mock import Mock, patch
from wsgiref.simple_server import make_server

from google.api_core.exceptions import NotFound
from google.auth.credentials import AnonymousCredentials
from google.cloud.compute_v1.types import Subnetwork
from google.cloud.compute_v1.types.compute import FirewallPolicyRule
from googleapiclient.errors import HttpError
import pytest

from anyscale.cli_logger import BlockLogger
from anyscale.gcp_verification import (
    _firewall_rules_from_proto_resp,
    _gcp_subnet_has_enough_capacity,
    _verify_filestore,
    _verify_firewall_policy,
    _verify_gcp_access_service_account,
    _verify_gcp_dataplane_service_account,
    _verify_gcp_networking,
    _verify_gcp_project,
    GCPLogger,
    GoogleCloudClientFactory,
    verify_gcp,
)
from anyscale.utils.network_verification import Direction, FirewallRule, Protocol


class RequestTracker:
    def __init__(self):
        self.responses: Dict[str, List[Tuple[int, Optional[str]]]] = {}
        self.seen_requests: List[Any] = []

    def reset(self, responses):
        for k, v in responses.items():
            re.compile(k)
            assert all(len(i) == 2 for i in v)
        self.responses = copy.deepcopy(responses)
        self.seen_requests = []


class GCloudMockHandler:
    def __init__(self, tracker, *args, **kwargs):
        self.tracker = tracker

    def __call__(self, env, start_response):
        self.tracker.seen_requests.append(env)

        path = env["PATH_INFO"]

        for regex in self.tracker.responses:
            if re.match(regex, path):
                code, body_file = self.tracker.responses[regex].pop(0)
                start_response(code, [("Content-Type", "application/json")])
                if body_file is not None:
                    with open(
                        Path(__file__).parent.joinpath("gcp_responses", body_file)
                    ) as f:
                        return [json.dumps(json.load(f)).strip().encode()]
                return []

        pytest.fail(
            f"Un handled request to {self.path}:\n{self.tracker.responses}",
            pytrace=False,
        )


@pytest.fixture()
def setup_mock_server() -> Iterator[Tuple[GoogleCloudClientFactory, RequestTracker]]:
    tracker = RequestTracker()
    server = make_server("localhost", 0, GCloudMockHandler(tracker))
    port = server.server_port
    print(f"Serving on (http://localhost:{port})")
    t = Thread(target=server.serve_forever, daemon=True)
    t.start()
    yield (
        GoogleCloudClientFactory(
            credentials=AnonymousCredentials(),
            force_rest=True,
            client_options={"api_endpoint": f"http://127.0.0.1:{port}"},
        ),
        tracker,
    )
    print(f"Shutting down server on (http://localhost:{port})")
    server.server_close()
    t.join(timeout=0.1)


_MOCK_RESOURCES = {
    "vpc_name": "vpc_one",
    "project_id": "anyscale-bridge-deadbeef",
    "anyscale_access_service_account": "anyscale-admin@anyscale-bridge-deadbeef.iam.gserviceaccount.com",
    "dataplane_service_account": "cld-xyz-access@anyscale-bridge-deadbeef.iam.gserviceaccount.com",
    "subnet_name": "subnet_one",
    "firewall_name": "firewall",
    "region": "us-west1",
    "filestore_id": "store-one",
    "filestore_location": "us-west1",
}


@pytest.mark.parametrize(
    ("responses", "expected_result", "num_calls"),
    [
        pytest.param(
            {".*/networks/.*": [("404 Not Found", None)]}, False, 1, id="Network404",
        ),
        pytest.param(
            {
                ".*/networks/.*": [("200 OK", "networks.json")],
                ".*/subnetworks/.*": [("404 Not Found", None)],
            },
            False,
            2,
            id="SubNet404",
        ),
        pytest.param(
            {
                ".*/networks/.*": [("200 OK", "networks.json")],
                ".*/subnetworks/.*": [("200 OK", "subnetworks.json")],
            },
            True,
            2,
            id="Success",
        ),
        pytest.param(
            {
                ".*/networks/.*": [("200 OK", "networks.json")],
                ".*/subnetworks/.*": [("200 OK", "subnetworks_other.json")],
            },
            False,
            2,
            id="WrongNetwrork",
        ),
    ],
)
def test_verify_gcp_networking(
    setup_mock_server, responses, expected_result: bool, num_calls: int
):
    factory, tracker = setup_mock_server
    tracker.reset(responses=responses)
    assert (
        _verify_gcp_networking(factory, _MOCK_RESOURCES, _gcp_logger())
        == expected_result
    )
    assert len(tracker.seen_requests) == num_calls, tracker.seen_requests


@pytest.mark.parametrize(
    ("cidr", "result", "log"),
    [
        ("10.0.0.0/16", True, ""),
        ("10.0.0.0/19", True, ""),
        ("10.0.0.0/21", True, "We suggest at least"),
        ("10.0.0.0/25", False, "We want at least"),
        pytest.param(
            "",
            False,
            "",
            marks=pytest.mark.xfail(raises=ValueError, strict=True),
            id="BadIPAddress",
        ),
    ],
)
def test_gcp_subnet_has_enough_capacity(cidr: str, result: bool, log: str, capsys):
    subnet = Subnetwork(ip_cidr_range=cidr)

    assert _gcp_subnet_has_enough_capacity(subnet, BlockLogger()) == result

    stdout, stderr = capsys.readouterr()
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)

    if log:
        assert re.search(log, stderr)


@pytest.mark.parametrize(
    "call_factory",
    [
        pytest.param(
            lambda f: f.compute_v1.NetworksClient().get(project="abc", network="cde"),
            id="Compute",
        ),
        pytest.param(
            lambda f: f.resourcemanager_v3.ProjectsClient().get_project(
                name="projects/abc"
            ),
            id="ResourceManager",
        ),
    ],
)
def test_client_factory_cloud_client(setup_mock_server, call_factory: Callable):
    factory, tracker = setup_mock_server
    tracker.reset(responses={".*": [("404 Not Found", None)]})
    with pytest.raises(NotFound):
        call_factory(factory)


def test_client_factory_apis(setup_mock_server):
    factory, tracker = setup_mock_server
    tracker.reset(responses={".*": [("418 I'm a teapot", None)]})

    with pytest.raises(HttpError) as e:
        factory.build("iam", "v1").projects().serviceAccounts().get(
            name="projects/-/serviceAccounts/abc"
        ).execute()
    assert e.value.status_code == 418


@pytest.mark.parametrize("projects_match", [True, False])
def test_gcp_verify_credentials_project(capsys, projects_match: bool):

    credentials_project = (
        _MOCK_RESOURCES["project_id"] if projects_match else "other_gcp_project"
    )
    with patch(
        "anyscale.gcp_verification.get_application_default_credentials"
    ) as mock_credentials, patch.multiple(
        "anyscale.gcp_verification",
        _verify_gcp_project=Mock(),
        _verify_gcp_access_service_account=Mock(),
        _verify_gcp_dataplane_service_account=Mock(),
        _verify_gcp_networking=Mock(),
        _verify_firewall_policy=Mock(),
        _verify_filestore=Mock(),
    ):
        mock_credentials.return_value = (
            AnonymousCredentials(),
            credentials_project,
        )
        assert verify_gcp(_MOCK_RESOURCES, BlockLogger())
        mock_credentials.assert_called_once()

    _, err = capsys.readouterr()
    assert ("Default credentials are for" in err) != projects_match


@pytest.mark.parametrize(
    ("responses", "expected_result"),
    [
        pytest.param({".*": [("404 Not Found", None)]}, False, id="NotFound"),
        pytest.param(
            {
                ".*": [
                    ("200 OK", "project_get.json"),
                    ("200 OK", "project_iam_bindings.json"),
                ]
            },
            True,
            id="ProjectExists",
        ),
        pytest.param(
            {".*": [("200 OK", "project_get_inactive.json")]},
            False,
            id="ProjectInactive",
        ),
    ],
)
def test_verify_gcp_project(setup_mock_server, responses, expected_result: bool):
    factory, tracker = setup_mock_server
    tracker.reset(responses)
    assert (
        _verify_gcp_project(factory, _MOCK_RESOURCES, _gcp_logger()) == expected_result
    )


def test_verify_gcp_missing_bindigs(setup_mock_server, capsys):
    factory, tracker = setup_mock_server
    tracker.reset(
        {
            ".*": [
                ("200 OK", "project_get.json"),
                ("200 OK", "project_iam_bindings.json"),
            ]
        }
    )
    assert _verify_gcp_project(factory, _MOCK_RESOURCES, _gcp_logger())
    _, err = capsys.readouterr()
    assert (
        "The Compute Engine Service Agent does not have the standard IAM Role of 'roles/compute.serviceAgent'"
        in err
    )


@pytest.mark.parametrize(
    ("service_account", "expected_result"),
    [
        pytest.param(
            "anyscale-admin-owner@anyscale-bridge-deadbeef.iam.gserviceaccount.com",
            True,
            id="Owner",
        ),
        pytest.param(
            "anyscale-admin-editor@anyscale-bridge-deadbeef.iam.gserviceaccount.com",
            True,
            id="Editor",
        ),
        pytest.param(
            "anyscale-admin-editor-not-signer@anyscale-bridge-deadbeef.iam.gserviceaccount.com",
            False,
            id="EditorNotSigner",
        ),
        pytest.param(
            "nope@anyscale-bridge-deadbeef.iam.gserviceaccount.com",
            False,
            id="NotGranted",
        ),
    ],
)
def test_verify_gcp_access_service_account(
    setup_mock_server, service_account: str, expected_result: bool
):
    factory, tracker = setup_mock_server
    tracker.reset(
        {
            ".*": [
                ("200 OK", "access_service_account_permissions.json"),
                ("200 OK", "project_iam_binding_access.json"),
            ]
        }
    )
    assert (
        _verify_gcp_access_service_account(
            factory,
            {**_MOCK_RESOURCES, "anyscale_access_service_account": service_account},
            _gcp_logger(),
        )
        == expected_result
    )


@pytest.mark.parametrize(
    ("responses", "expected_result", "output"),
    [
        pytest.param(
            {".*": [("404 Not Found", None), ("404 Not Found", None)]},
            False,
            re.compile(".*"),
            id="Neither Exist",
        ),
        pytest.param(
            {
                ".*": [
                    ("200 OK", "global_firewall.json"),
                    ("200 OK", "subnetworks.json"),
                ],
            },
            True,
            re.compile(".*"),
            id="GlobalFirewall",
        ),
        pytest.param(
            {
                ".*": [
                    ("404 Not Found", None),
                    ("200 OK", "regional_firewall.json"),
                    ("200 OK", "subnetworks.json"),
                ],
            },
            True,
            re.compile("Global firweall policy .* not found"),
            id="RegionalFirewall",
        ),
        pytest.param(
            {".*": [("200 OK", "global_firewall_wrong_vpc.json")],},
            False,
            re.compile(".*is not associated with the VPC.*"),
            id="WrongNetwork",
        ),
    ],
)
def test_verify_firewall_policy(
    setup_mock_server, responses, expected_result: bool, output: re.Pattern, capsys
):
    factory, tracker = setup_mock_server
    tracker.reset(responses=responses)

    assert (
        _verify_firewall_policy(
            factory, _MOCK_RESOURCES, GCPLogger(BlockLogger(), "project")
        )
        == expected_result
    )
    _, stderr = capsys.readouterr()
    assert output.search(stderr), f"Missing output in {stderr}"


@pytest.mark.parametrize(
    ("proto", "rule"),
    [
        (FirewallPolicyRule(action="deny"), []),
        (
            FirewallPolicyRule(
                direction="EGRESS",
                action="allow",
                match={"src_ip_ranges": ["10.10.10.0/24"]},
            ),
            [
                FirewallRule(
                    direction=Direction.EGRESS,
                    protocol=Protocol.all,
                    network=ipaddress.ip_network("10.10.10.0/24"),
                    ports=None,
                )
            ],
        ),
        (
            FirewallPolicyRule(
                direction="EGRESS",
                action="allow",
                match={
                    "src_ip_ranges": ["10.10.10.0/24"],
                    "layer4_configs": [{"ip_protocol": "tcp"}],
                },
            ),
            [
                FirewallRule(
                    direction=Direction.EGRESS,
                    protocol=Protocol.tcp,
                    network=ipaddress.ip_network("10.10.10.0/24"),
                    ports=None,
                )
            ],
        ),
    ],
)
def test_firewall_rules_from_proto_resp(
    proto: FirewallPolicyRule, rule: List[FirewallRule]
):
    assert _firewall_rules_from_proto_resp([proto]) == rule
    assert _firewall_rules_from_proto_resp([proto, proto]) == rule * 2


def test_verify_gcp_access_service_account_does_not_exist(setup_mock_server):
    factory, tracker = setup_mock_server
    tracker.reset({".*": [("404 Not Found", None)]})
    assert not _verify_gcp_access_service_account(
        factory, _MOCK_RESOURCES, _gcp_logger(),
    )


@pytest.mark.parametrize(
    ("responses", "expected_result"),
    [
        pytest.param({".*": [("404 Not Found", None)]}, False, id="DoesNotExist"),
        pytest.param(
            {
                ".*": [
                    ("200 OK", "dataplane_service_account.json"),
                    ("200 OK", "project_iam_binding_access.json"),
                ]
            },
            True,
            id="DoesNotExist",
        ),
    ],
)
def test_verify_gcp_dataplane_service_account(
    setup_mock_server, responses, expected_result: bool, capsys
):
    factory, tracker = setup_mock_server
    tracker.reset(responses)
    assert (
        _verify_gcp_dataplane_service_account(factory, _MOCK_RESOURCES, _gcp_logger())
        == expected_result
    )

    _, err = capsys.readouterr()
    if expected_result:
        # Check if there is a warning about missing artifact Registry warnings if we pass verification.
        assert re.search("roles/artifactregistry.reader`", err) and re.search(
            "safe to ignore if you are not using", err
        )


def test_verify_gcp_dataplane_service_account_wrong_project(setup_mock_server, capsys):
    factory, tracker = setup_mock_server
    tracker.reset(
        {
            ".*": [
                ("200 OK", "dataplane_service_account.json"),
                ("200 OK", "project_iam_binding_access.json"),
            ]
        }
    )
    assert _verify_gcp_dataplane_service_account(
        factory, {**_MOCK_RESOURCES, "project_id": "something-else"}, _gcp_logger(),
    )

    _, stderr = capsys.readouterr()
    assert (
        "constraints/iam.disableCrossProjectServiceAccountUsage` is not enforced"
        in stderr
    )


@pytest.mark.parametrize(
    ("response", "result"),
    [
        pytest.param(("200 OK", "regional_filestore.json"), True, id="regional"),
        pytest.param(("200 OK", "zonal_filestore.json"), True, id="zonal"),
        pytest.param(
            ("200 OK", "regional_filestore_wrong_vpc.json"), False, id="wrong_vpc"
        ),
        pytest.param(("404 Not Found", None), False, id="not_found"),
    ],
)
def test_verify_filestore(setup_mock_server, response, result: bool):
    factory, tracker = setup_mock_server
    tracker.reset({".*": [response]})
    assert _verify_filestore(factory, _MOCK_RESOURCES, _gcp_logger(),) == result


@pytest.mark.parametrize(
    ("response", "has_warning"),
    [
        pytest.param(("200 OK", "regional_filestore.json"), False, id="Enterprise"),
        pytest.param(("200 OK", "zonal_filestore.json"), True, id="NonEnterprise"),
    ],
)
def test_verify_filestore_warn(setup_mock_server, capsys, response, has_warning: bool):
    factory, tracker = setup_mock_server
    tracker.reset({".*": [response]})
    assert _verify_filestore(factory, _MOCK_RESOURCES, _gcp_logger())
    _, err = capsys.readouterr()
    assert ("ENTERPRISE" in err) == has_warning


def _gcp_logger() -> GCPLogger:
    return GCPLogger(BlockLogger(), "project_abc", yes=True)
