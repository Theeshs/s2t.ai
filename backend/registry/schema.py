from datetime import datetime
from typing import List, Optional

from ninja import Schema


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class DashboardSchema(Schema):
    id: Optional[int]
    name: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    isDeleted: Optional[datetime]

    # class Config(Schema.Config):
    #     alias_generator = to_camel


class ChartsOutSchema(Schema):
    id: Optional[int]
    name: Optional[str]
    order: Optional[int]
    chart_type: Optional[int]
    chart_config: Optional[dict]
    height: Optional[int]
    width: Optional[int]


class ChartCreateSchema(Schema):
    name: str
    order: int
    chart_type: int
    chart_config: Optional[dict]
    height: int
    width: int


class ChartTypeCreateSchema(Schema):
    chart_type: str


class ChartTypeCreateSchemaOut(Schema):
    id: int
    chart_type: str
    chart_image: str


class ChartUpdatePayload(Schema):
    title: str
    subTitle: str
    yAxis: Optional[str]
    xAxis: Optional[str]
    dataSourceName: str
    linChartValues: Optional[List[str]]


class DataSourcesOutResponse(Schema):
    chart_type_id: int
    chart_type: str
    data_sources: list
