from datetime import datetime
from ninja import Schema
from typing import Optional

def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))

class DashboardSchema(Schema):
    id: Optional[int]
    name: str
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    isDeleted: Optional[datetime]

    # class Config(Schema.Config):
    #     alias_generator = to_camel


class ChartsOutSchema(Schema):
    id: int
    name: str
    order: int
    chart_type: str