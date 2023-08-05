import subprocess
from typing import Dict, List, Optional, Set, Tuple, Union

import google.auth
from google.auth.credentials import Credentials
from google.iam.v1.policy_pb2 import Binding

from anyscale.cli_logger import BlockLogger


def get_application_default_credentials(
    logger: BlockLogger,
) -> Tuple[Credentials, Optional[str]]:
    """Get application default credentials, or run `gcloud` to try to log in."""
    try:
        return google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError as e:
        logger.warning(
            "Could not automatically determine Google Application Default Credentials, trying to authenticate via GCloud"
        )
        auth_login = subprocess.run(["gcloud", "auth", "application-default", "login"])
        if auth_login.returncode != 0:
            raise RuntimeError("Failed to authenticate via gcloud") from e

        return google.auth.default()


def binding_from_dictionary(
    inp: List[Dict[str, Union[List[str], str]]]
) -> List[Binding]:
    return [Binding(role=b["role"], members=b["members"]) for b in inp]


def check_policy_bindings(
    iam_policy: List[Binding], member: str, possible_roles: Set[str]
) -> bool:
    return any(
        policy.role in possible_roles and member in policy.members
        for policy in iam_policy
    )
