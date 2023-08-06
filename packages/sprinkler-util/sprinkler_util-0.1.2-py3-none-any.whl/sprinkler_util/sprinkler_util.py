import json
import os
from typing import Any


class SprinklerSecretNotSetException(Exception):
    """Exception raised when a secret is not found."""


def get_request_body(as_json: bool = False) -> Any:
    """
    Returns the body from the webhook which triggered this job.
    Returns None if no body was given, or if it was a scheduled run.
    """
    body = json.loads(os.environ.get("SPRINKLER_TASK_INSTANCE_BODY", ""))
    if body == "":
        return None
    if as_json:
        return json.loads(body)
    return body


def send_response(response: Any) -> None:
    """
    Use within a call-and-response job to return a value to the triggering request.
    May only be called once.
    """
    print(
        f"""SPRINKLER*_*RESPONSE*_*START*{json.dumps(response, default=str)}*SPRINKLER*_*RESPONSE*_*END"""
    )


def get_secret(key: str) -> str:
    """
    Get a secret from the sprinkler secrets store.
    Will raise a SprinklerSecretNotSetException if it is not found.
    """
    secret = os.environ.get(f"SPRINKLER_SECRET_{key.upper()}")
    if secret is None:
        raise SprinklerSecretNotSetException(key)
    return secret
