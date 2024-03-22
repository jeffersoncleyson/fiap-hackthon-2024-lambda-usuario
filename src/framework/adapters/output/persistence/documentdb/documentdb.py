import logging

from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from src.application.erros.duplicate_item import DuplicateItemError
from src.application.erros.internal_error import InternalError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DocumentDBAdapter:

    def __init__(self, collection_name: str, database: Database):
        self.collection_name = collection_name
        self.database = database

    def insert(self, document: dict):

        try:
            created = self.database.get_collection(self.collection_name).insert_one(
                document
            )

            if created.acknowledged:
                document["_id"] = str(created.inserted_id)
                return document
        except DuplicateKeyError as err:
            raise DuplicateItemError("Duplicate database document")
        except Exception as err:
            logger.error(err)

        raise InternalError("Unknown error")

    def update(self, query: dict, document: dict):

        try:
            updated = self.database.get_collection(self.collection_name).update_one(
                query, document, upsert=False
            )

            if updated.modified_count == 1 or updated.matched_count == 1:
                return True
            else:
                return False
        except DuplicateKeyError as err:
            raise DuplicateItemError("Duplicate database document")
        except Exception as err:
            logger.error(err)

        raise InternalError("Unknown error")

    def read(self, document: dict):

        try:
            read_doc = self.database.get_collection(self.collection_name).find_one(
                document
            )

            if read_doc is not None:
                return read_doc
        except Exception as err:
            logger.error(err)
            raise InternalError("Unknown error")
    
    def delete(self, document: dict):

        try:
            delete_doc = self.database.get_collection(self.collection_name).delete_one(
                document
            )

            if delete_doc.deleted_count == 1:
                return True
        except Exception as err:
            logger.error(err)

        raise InternalError("Unknown error")
