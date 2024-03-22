import json

from src.application.erros.duplicate_item import DuplicateItemError
from src.application.ports.input.user.role import Role
from src.application.utils.encrypt_utils import EncryptUtils
from src.framework.adapters.input.rest.response_formatter_utils import (
    ResponseFormatterUtils,
)
from src.framework.adapters.output.persistence.documentdb.documentdb import (
    DocumentDBAdapter,
)


class UpdateUserUseCase:

    def __init__(self, mongo_client: DocumentDBAdapter):
        self.mongo_client = mongo_client

    def process(self, event: dict):

        username = event["pathParameters"]["proxy"]

        body_json = json.loads(event["body"])
        password = body_json.get("password", None)
        role = body_json.get("role", None)

        if password is None and role is None:
            return ResponseFormatterUtils.get_response_message(
                {
                    "error": "bad_request",
                    "error_description": "missing request parameters",
                },
                400,
            )

        if role is not None and role not in Role.__members__:
            return ResponseFormatterUtils.get_response_message(
                {
                    "error": "bad_request",
                    "error_description": f"Invalid role. Must be one of: {', '.join(Role.__members__)}",
                },
                400,
            )

        try:
            fields = {}

            if role is not None:
                fields["role"] = role

            if password is not None:
                fields["password"] = (EncryptUtils.encrypt(password),)

            update = {"$set": fields}

            is_user_updated = self.mongo_client.update({"username": username}, update)

            if is_user_updated:
                return ResponseFormatterUtils.get_response_message(
                    {
                        "username": username,
                        "role": role,
                    },
                    200,
                )
            else:
                return ResponseFormatterUtils.get_response_message(
                    {
                        "error": "not_found",
                        "error_description": "username {} not found".format(username),
                    },
                    404,
                )
        except Exception as err:
            return ResponseFormatterUtils.get_response_message(
                {
                    "error": "internal_server_error",
                    "error_description": "Unknown error",
                },
                500,
            )
