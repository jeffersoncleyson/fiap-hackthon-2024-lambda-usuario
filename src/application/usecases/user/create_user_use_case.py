import json

from src.application.erros.duplicate_item import DuplicateItemError
from src.application.ports.input.user.role import Role
from src.application.utils.encrypt_utils import EncryptUtils
from src.framework.adapters.input.rest.response_formatter_utils import \
    ResponseFormatterUtils
from src.framework.adapters.output.persistence.documentdb.documentdb import \
    DocumentDBAdapter


class CreateUserUseCase:

    def __init__(self, mongo_client: DocumentDBAdapter):
        self.mongo_client = mongo_client

    def process(self, event: dict):

        body_json = json.loads(event["body"])
        username = body_json.get("username", None)
        password = body_json.get("password", None)
        role = body_json.get("role", None)

        if username is None or password is None or role is None:
            return ResponseFormatterUtils.get_response_message(
                {
                    "error": "bad_request",
                    "error_description": "missing request parameters (see docs page)",
                },
                400,
            )

        if role not in Role.__members__:
            return ResponseFormatterUtils.get_response_message(
                {
                    "error": "bad_request",
                    "error_description": f"Invalid role. Must be one of: {', '.join(Role.__members__)}",
                },
                400,
            )
        
        try:
            created_user = self.mongo_client.insert(
                {
                    "username": username,
                    "password": EncryptUtils.encrypt(password),
                    "role": role,
                }
            )
            del created_user["password"]
            return ResponseFormatterUtils.get_response_message(created_user, 201)
        except DuplicateItemError:
            return ResponseFormatterUtils.get_response_message(
                {
                    "error": "bad_request",
                    "error_description": "username {} already exists".format(username),
                },
                400,
            )
        except Exception:
            return ResponseFormatterUtils.get_response_message(
                {
                    "error": "internal_server_error",
                    "error_description": "Unknown error",
                },
                500,
            )
