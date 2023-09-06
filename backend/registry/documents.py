from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Chart, Dashboard


@registry.register_document
class DashboardDocument(Document):
    class Index:
        name = "dashboards"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Dashboard
        fields = ("id", "name")
