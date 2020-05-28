import os

from pymongo import MongoClient

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '27017'
DEFAULT_DB_NAME = 'labs'

host = os.environ.get('HOST', DEFAULT_HOST)
port = int(os.environ.get('PORT', DEFAULT_PORT))
db_name = os.environ.get('DB_NAME', DEFAULT_DB_NAME)

_client = MongoClient(host, port)
_db = _client[db_name]


def get_collection_for_name(name: str):
    return _db[name]
