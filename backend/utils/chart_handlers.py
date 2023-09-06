import json
from abc import ABC, abstractmethod
from utils.elasticsearch import ElasticSearchConnection
from django.conf import settings


def get_columns(file_name, chart_type="pie"):
    data = read_document_from_elastic_search(chart_type, file_name)
    if chart_type in ["pie", "bar"]:
        if isinstance(data, list) and len(data) > 0:
            return data[0].keys()
        elif isinstance(data, dict):
            return data.keys()
    elif chart_type == "line":
        return [category.get("name") for category in data]
    return []


class HandleCharts(ABC):
    def __init__(self, file_name: str, x_axis: str, y_axis: str) -> None:
        self.file_name = file_name
        self.x_axis = x_axis
        self.y_axis = y_axis

    # @abstractmethod
    # def handle_pie(self):
    #     pass

    # @abstractmethod
    # def handle_bar(self):
    #     pass

    # @abstractmethod
    # def handle_line(self):
    #     pass


class PieChart(HandleCharts):

    def get_pie_chart_data(self):
        data = read_document_from_elastic_search("pie", self.file_name)

        pie_chart_data = []
        for obj in data:
            pie_chart_data.append({"name": obj[self.x_axis], "y": obj[self.y_axis]})

        data = {"name": self.y_axis, "colorByPoint": True, "data": pie_chart_data}
        return data


class BarChart(HandleCharts):

    def get_bar_chart_data(self):
        data = read_document_from_elastic_search("bar", self.file_name)
        bar_chart_data = []

        for obj in data:
            bar_chart_data.append({"name": obj[self.x_axis], "y": obj[self.y_axis]})

        data = {"name": self.y_axis, "colorByPoint": True, "data": bar_chart_data}
        return data


class LineChart(HandleCharts):

    def get_line_chart_data(self):
        return_data = []
        data = read_document_from_elastic_search("line", self.file_name)

        for item in data:
            for cat in self.y_axis:
                if cat == item.get("name"):
                    return_data.append(item)
        return return_data


def get_data_sources(chart_type: str):
    es = ElasticSearchConnection(
            settings.ELASTICSEARCH_HOST, settings.ELASTICSEARCH_PORT
        )
    if chart_type == "line":
        data = es.list_index_docs("line_charets")
        return data
    elif chart_type in ("pie", "bar",):
        data = es.list_index_docs("pie_bar_charts")
        return data


def read_document_from_elastic_search(chart_type: str, id: str):
    es = ElasticSearchConnection(
            settings.ELASTICSEARCH_HOST, settings.ELASTICSEARCH_PORT
        )
    
    if chart_type == "line":
        data = es.read_document("line_charets", id=id)
        data = data.get("_source").get("line")
    elif chart_type in ("pie", "bar",):
        data = es.read_document("pie_bar_charts", id=id)
        data = data.get("_source").get("pie_bar")
    return data