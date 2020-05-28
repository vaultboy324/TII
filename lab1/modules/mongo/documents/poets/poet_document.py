import os
from bson.json_util import dumps
from bson.json_util import loads

from lab1.modules.mongo import connect
from lab1.modules.mongo.documents.poets.poet_scheme import PoetScheme


class PoetDocument:
    _DEFAULT_COLLECTION_NAME = 'poets'
    _collection_name = os.environ.get('POETS_COLLECTION_NAME', _DEFAULT_COLLECTION_NAME)
    _poets_data = connect.get_collection_for_name(_collection_name)

    _filters = {
        '_id': False
    }

    @staticmethod
    def get_info():
        return loads(dumps(PoetDocument._poets_data.find({}, PoetDocument._filters)))[0]

    @staticmethod
    def remove():
        PoetDocument._poets_data.remove({})

    @staticmethod
    def post_one(parameters: dict):
        poet_info = {
            PoetScheme.COUNT_WORDS: parameters.get(PoetScheme.COUNT_WORDS),
            PoetScheme.POETS: parameters.get(PoetScheme.POETS),
            PoetScheme.WORDS: parameters.get(PoetScheme.WORDS)
        }

        PoetDocument._poets_data.insert_one(poet_info)
