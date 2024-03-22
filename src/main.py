import pymongo
import logging
from src.application.environment import EnvironmentUtils
from src.application.environment_constants import EnvironmentConstants
from src.framework.adapters.output.persistence.documentdb.documentdb import DocumentDBAdapter
from src.framework.adapters.input.rest.response_formatter_utils import ResponseFormatterUtils
from src.application.usecases.user.create_user_use_case import CreateUserUseCase
from src.application.usecases.user.update_user_use_case import UpdateUserUseCase
from src.application.usecases.user.read_user_use_case import ReadUserUseCase
from src.application.usecases.user.delete_user_use_case import DeleteUserUseCase

logger = logging.getLogger()
logger.setLevel(logging.INFO)

mongo_uri = EnvironmentUtils.get_env(EnvironmentConstants.MONGO_URI.name)
database = EnvironmentUtils.get_env(EnvironmentConstants.DB_NAME.name)
database_client = pymongo.MongoClient(mongo_uri)
database_adapter = DocumentDBAdapter("users", database_client[database])

create_user_use_case = CreateUserUseCase(database_adapter)
update_user_use_case = UpdateUserUseCase(database_adapter)
read_user_use_case = ReadUserUseCase(database_adapter)
delete_user_use_case = DeleteUserUseCase(database_adapter)


def lambda_handler(event, context):

    resource_path = event["requestContext"]["resourcePath"]
    http_method = event["requestContext"]["httpMethod"]
    

    if http_method == "POST" and resource_path == "/usuario/create":
        return create_user_use_case.process(event)
    elif http_method == "PATCH" and resource_path == "/usuario/username/{proxy+}":
        return update_user_use_case.process(event)
    elif http_method == "GET" and resource_path == "/usuario/username/{proxy+}":
        return read_user_use_case.process(event)
    elif http_method == "DELETE" and resource_path == "/usuario/username/{proxy+}":
        return delete_user_use_case.process(event)
    
    return ResponseFormatterUtils.get_response_message(
        {
            "error": "not_found",
            "error_description": "%s %s is not a valid resource." % (http_method, resource_path)
         }, 404
    )
