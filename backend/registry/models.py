from django.db import models

from core.base_models import BaseModel


# Create your models here.
class Dashboard(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)


class ChartType(BaseModel):
    chart_type = models.CharField(max_length=100, null=False, blank=False)
    chart_image = models.TextField(null=True, blank=True)


class Chart(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    order = models.IntegerField(null=False, blank=False)
    chart_type = models.ForeignKey(
        ChartType,
        null=False,
        blank=False,
        related_name="chart_chart_type",
        on_delete=models.CASCADE,
    )
    dashboard = models.ForeignKey(
        Dashboard, related_name="dashboard_charts", on_delete=models.CASCADE
    )
    chart_config = models.JSONField(null=True, blank=True)
    chart_height = models.IntegerField(null=True, blank=True)
    chart_width = models.IntegerField(null=True, blank=True)
