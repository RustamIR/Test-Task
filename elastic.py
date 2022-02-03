import elasticsearch

from typing import List, Union
from elasticsearch import Elasticsearch


def __init__(self, index: str = "posts"):
    self.es = Elasticsearch(HOST="http://localhost", PORT=9200)
    self.index = index


def search_id(self, id) -> Union[list, None]:
    """Поиск по id"""
    doc = self.es.search(
        index=self.index, 
        body={
            "size": 1,
            "sort": "created_date",
            "query": {
                "match": {
                    'id': id
                }
            }
        })["hits"]["hits"]
    if len(doc) == 0:
        return None
    return doc


def search_text(self, text, rubrics) -> List[dict]:
    doc = self.es.search(index=self.index, 
        body={
            "from":100,
            "size": 20,
            "sort": "created_date",
            "query": {
                "match": {
                    'text': text,
                }
            }
        })
    data_id = [
        {"id_": item["_id"], 
        "id": item["source"]["id"]} for item in doc["hits"]["hits"]
    ]
    return data_id


def delete_id(self, id):
    try:
        self.es.delete(index=self.index, id=id)
        return True
    except elasticsearch.exceptions.NotFoundError:
        return False