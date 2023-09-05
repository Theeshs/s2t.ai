import time
from typing import Any, Optional
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from utils.elasticsearch import ElasticSearchConnection
import json
from django.conf import settings

class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any):
        self.stdout.write('Creating elastic search documents')
        print(settings.ELASTICSEARCH_HOST, settings.ELASTICSEARCH_PORT)
        es = ElasticSearchConnection(settings.ELASTICSEARCH_HOST, settings.ELASTICSEARCH_PORT)
        # with open(r'C:\Users\theek\dev\S2T.ai\backend\data\doc_1.json', 'r') as json_file:
        #     doc_1_content = json.load(json_file)
            
        #     es.create_document(index="testasd", body={"bar_pie": doc_1_content}, id=1)
        
        with open(r'C:\Users\theek\dev\S2T.ai\backend\data\doc_2.json', 'r') as json_file2:
            doc_12_content = json.load(json_file2)
            es.create_document(index="line", body={"line": doc_12_content}, id=1)
            