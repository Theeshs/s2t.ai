from django.conf import settings
from elasticsearch import Elasticsearch


class ElasticSearchConnection:
    def __init__(
        self,
        host: str = settings.ELASTICSEARCH_HOST,
        port: int = settings.ELASTICSEARCH_PORT,
        index: str = None,
    ) -> None:
        self.host = host
        self.port = port
        self.index = index
        self.connection = self.connect()

    def connect(self):
        es = Elasticsearch([{"host": self.host, "port": self.port}])
        return es

    def create_index(self):
        if not self.connection.indices.exists(index=self.index):
            self.connection.indices.create(index=self.index)
        else:
            print("index alread exists")

    def create_document(self, index: str, body: dict, id: int, doc_type: str = "_doc"):
        self.index = index
        self.create_index()
        self.connection.index(index=self.index, doc_type=doc_type, id=id, body=body)

    def read_document(self, index: str, id: int, doc_type: str = "_doc"):
        doc_object = self.connection.get(index=index, doc_type=doc_type, id=id)
        return doc_object

    def list_index_docs(self, index: str):
        search_body = {
            "query": {
                "match_all": {}
            }
        }

        search_result = self.connection.search(index=index, body=search_body)
        docs = []
        for hit in search_result['hits']['hits']:
            print(hit['_id'])
            docs.append(hit['_id'])
        return docs