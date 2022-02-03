import elasticsearch

from typing import List, Union
from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session

class EsService:
    def __init__(self, index: str = "posts"):
        self.es = Elasticsearch(HOST="http://localhost", PORT=9200)
        self.index = index


    def search_id(self, id) -> Union[list, None]:
        doc = self.es.search(
            index=self.index, 
            body={
                "_source": False,
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


    def search_text(self, text, sort, size) -> List[dict]:
        print(text, sort, size)
        doc = self.es.search(index=self.index, 
            body={
                "_source": False,
                "size": size,
                # "sort": sort,
                "query": {
                    "match": {
                        'text': 'привет',
                    }
                }
            }
        )
        print(doc)
        data_id = [
            {"id": item["_id"]} for item in doc["hits"]["hits"]
        ]
        return data_id


    def delete_id(self, id):
        try:
            self.es.delete(index=self.index, id=id)
            return True
        except elasticsearch.exceptions.NotFoundError:
            return False
