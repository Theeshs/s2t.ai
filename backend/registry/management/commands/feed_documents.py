import json
import os
import time
from typing import Any, Optional

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from utils.elasticsearch import ElasticSearchConnection


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Creating elastic search documents")
        directory_path = "../backend/data"
        es = ElasticSearchConnection(
            settings.ELASTICSEARCH_HOST, settings.ELASTICSEARCH_PORT
        )
        for path in os.listdir(directory_path):
            if os.path.isdir(os.path.join(directory_path, path)) and path == "line":
                files = os.listdir(os.path.join(directory_path, path))
                print(files)
                for file in files:
                    with open(f"{directory_path}/{path}/{file}") as json_file:
                        print(f"{file.split('.json')[0]}")
                        json_content = json.load(json_file)
                        es.create_document(index="line_charets", body={"line": json_content}, id=f"{file.split('.json')[0]}")
            elif os.path.isdir(os.path.join(directory_path, path)) and path == "pie_bar":
                files = os.listdir(os.path.join(directory_path, path))
                print(files)
                for file in files:
                    with open(f"{directory_path}/{path}/{file}") as json_file:
                        print(f"{file.split('.json')[0]}")
                        json_content = json.load(json_file)
                        es.create_document(index="pie_bar_charts", body={"pie_bar": json_content}, id=f"{file.split('.json')[0]}")
