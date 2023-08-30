from core.base_models import BaseModel
from django.db import models
# Create your models here.
class Dashboard(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)



class ChartType(BaseModel):
    chart_type = models.CharField(max_length=100, null=False, blank=False)
    chart_image = models.CharField(max_length=200, null=False, blank=False)

    
class Chart(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    order = models.IntegerField(null=False, blank=False)
    chart_type = models.OneToOneField(ChartType, null=False, blank=False, related_name="chart_chart_type", on_delete=models.CASCADE)
    dashboard = models.ForeignKey(Dashboard, related_name="dashboard_charts", on_delete=models.CASCADE)
