import json
from http import HTTPStatus
from typing import Any, Union, Dict, List

from src.logger import get_logger

LOGGER = get_logger(__name__)

STATUS_CODE = "statusCode"


def response(status_code: int, body: Union[Dict, List] = None) -> dict:
    resp: Dict[str, Any] = {
        STATUS_CODE: status_code
    }

    if body is not None:
        resp["body"] = json.dumps(body)

    return resp


def success(body: Union[Dict, List] = None) -> dict:
    return response(HTTPStatus.OK, body)
