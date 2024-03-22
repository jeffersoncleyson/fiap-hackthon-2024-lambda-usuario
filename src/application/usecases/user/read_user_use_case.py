import json

from src.framework.adapters.input.rest.response_formatter_utils import \
    ResponseFormatterUtils
from src.framework.adapters.output.persistence.documentdb.documentdb import \
    DocumentDBAdapter


class ReadUserUseCase:

    def __init__(self, mongo_client: DocumentDBAdapter):
        self.mongo_client = mongo_client

    def process(self, event: dict):

        username = event["pathParameters"]["proxy"]

        found_user = self.mongo_client.read({"username": username})

        if found_user is not None:
            return ResponseFormatterUtils.get_response_message(
                {
                    "id": str(found_user["_id"]),
                    "username": found_user["username"],
                    "role": found_user["role"],
                },
                200,
            )

        return ResponseFormatterUtils.get_response_message(
            {
                "error": "not_found",
                "error_description": "Username {} not found".format(username),
            },
            404,
        )
