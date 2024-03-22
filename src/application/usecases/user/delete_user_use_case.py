from src.framework.adapters.input.rest.response_formatter_utils import (
    ResponseFormatterUtils,
)
from src.framework.adapters.output.persistence.documentdb.documentdb import (
    DocumentDBAdapter,
)


class DeleteUserUseCase:

    def __init__(self, mongo_client: DocumentDBAdapter):
        self.mongo_client = mongo_client

    def process(self, event: dict):

        username = event["pathParameters"]["proxy"]

        found_user = self.mongo_client.delete({"username": username})

        if found_user:
            return ResponseFormatterUtils.get_response_message(
                {},
                204,
            )

        return ResponseFormatterUtils.get_response_message(
            {
                "error": "not_found",
                "error_description": "Username {} not found".format(username),
            },
            404,
        )
