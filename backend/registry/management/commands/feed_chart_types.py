from typing import Any, Optional
from django.core.management.base import BaseCommand
from registry.models import ChartType

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:

        chart_types = [ChartType(chart_type="pie"), ChartType(name="bar"), ChartType(name="line")]
        ChartType.objects.bulk_create(chart_types)