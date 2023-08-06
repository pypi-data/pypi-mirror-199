import os
from pymongo import MongoClient
# from pandas import DataFrame
from bson import json_util, BSON
from bson import Binary, Code, ObjectId, Int64, Any
import os, json
import urllib.parse
from tklogs import Tkauditlogs

# 13th March 2023 - Depreciated and to be removed in future after confirmation from saurav rawat.
class NumberLong(int):
    """Representation of the BSON int64 type.

    This is necessary because every integral number is an :class:`int` in
    Python 3. Small integral numbers are encoded to BSON int32 by default,
    but Int64 numbers will always be encoded to BSON int64.

    :Parameters:
      - `value`: the numeric value to represent
    """

    __slots__ = ()

    _type_marker = 18

    def __getstate__(self) -> Any:
        return {}

    def __setstate__(self, state: Any) -> None:
        pass


class Tkmongo():
    def __init__(self, db_name=None):
        """
        :param dbname: The database name in mongo db.
        """
        if db_name is None:
            raise ValueError("DB Name is missing in constructor params.")
        self.service_name = 'mongo'
        self.db_name = db_name
        self.mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
        self.mongo_password = os.getenv("MONGODB_PASSWORD")
        self.http_timeout = 60

    def get_client(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = self.mongo_connection_string.replace("{password}", urllib.parse.quote(self.mongo_password))
        client = MongoClient(CONNECTION_STRING)
        return client

    def get_collection(self, collection_name):
        """
        :param collection_name: returns the collection
        :return:
        """
        client = self.get_client()
        return client[self.db_name][collection_name]

    def insert_document(self, collection_name, document, audit_log=False):
        """
        :param collection_name: The name of the collection in which the document will be inserted
        :param document: Document that will be inserted in the collection
        :param audit_log: Do we need audit Logs (False by default)
        :return:
        """
        if audit_log is True:
            old_document = self.fetch_document_by_id(collection_name, document['id'])
            Tkauditlogs().put_mongo_log(document, old_document, username='None')
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)


    def update_document(self, collection_name, query, document, audit_log=False):
        """
        :param collection_name: The name of the collection in which the document will be inserted
        :param query: The Query to Update the Document
        :param document: The document which will be updated.
        :param audit_log: Do we need audit Logs (False by default)
        :return: Generic PyMongo response for "update_one"
        """
        if audit_log is True:
            old_document = self.fetch_document_by_id(collection_name, document['id'])
            Tkauditlogs().put_mongo_log(document, old_document, username=None)
        collection = self.get_collection(collection_name)
        return collection.update_one(query, document)

    def update_many_document(self, collection_name, query, document):
        """
        :param collection_name: The name of the collection in which the document will be inserted
        :param query: The Query to Update the Document
        :param document: The list of document which will be updated.
        :return: Generic PyMongo response for "update_one"
        """
        collection = self.get_collection(collection_name)
        return collection.update_many(query, document)

    def replace_document(self, collection_name, query, document, audit_log=False):
        """
        :param collection_name: The name of the collection in which the document will be replaced
        :param query: The Query to Replace the Document
        :param document: The document which will be replaced.
        :param audit_log: Do we need audit Logs (False by default)
        :return: Generic PyMongo response for "replace_one"
        """
        if audit_log is True:
            old_document = self.fetch_document_by_id(collection_name, document['id'])
            Tkauditlogs().put_mongo_log(document, old_document, username=None)
        collection = self.get_collection(collection_name)
        return collection.replace_one(query, document)

    def insert_many_document(self, collection_name, documents):
        """
        :param collection_name: The name of the collection in which the document will be inserted
        :param documents: Document that will be inserted in the collection
        :return: Generic PyMongo response for "insert_many"
        """
        collection = self.get_collection(collection_name)
        return collection.insert_many(documents)

    def delete_document(self, collection_name, query):
        """
        :param collection_name: The name of the collection in which the document will be deleted
        :param query: The Query to Delete the Document
        :return: Generic PyMongo response for "delete_one"
        """
        collection = self.get_collection(collection_name)
        return collection.delete_one(query)

    def delete_many_document(self, collection_name, query):
        """
        :param collection_name: The name of the collection in which the document will be deleted
        :param query: The Query to Delete multiple Documents
        :return: Generic PyMongo response for "delete_many"
        """
        collection = self.get_collection(collection_name)
        return collection.delete_many(query)

    def fetch_document_by_id(self, collection_name, document_id):
        """
        :param collection_name: The name of the collection from which the document will be fetched
        :param document_id: The Id of Document that needs to be fetched
        :return: Generic PyMongo response for "find_one" (The full object for the id)
        """
        collection = self.get_collection(collection_name)
        return collection.find_one({"_id": ObjectId(document_id)})

    def fetch_one_document_by_query(self, collection_name, query):
        """
        :param collection_name: The name of the collection from which the document will be fetched
        :param query: The query that will return only one document
        :return: Generic PyMongo response for "find_one" (The full object for the id)
        """
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def fetch_all_document(self, collection_name):
        """
        :param collection_name: The name of the collection from which the document will be fetched
        :return:
        """
        collection = self.get_collection(collection_name)
        item_details = collection.find()
        return json.loads(json_util.dumps(list(item_details)))

    def filter_document(self, collection_name, filter):
        """
        :param collection_name: The name of the collection from which the document will be fetched
        :param filter: Filter condition for the documents in the collection
        :return:
        """
        collection = self.get_collection(collection_name)
        item_details = collection.find(filter)
        return json.loads(json_util.dumps(list(item_details)))

    def create_index(self, collection_name, index_name):
        """
        :param collection_name: The name of the collection in which the index will be created
        :param index_name: name of the index.
        :return:
        """
        collection = self.get_collection(collection_name)
        category_index = collection.create_index(index_name)
        return category_index




