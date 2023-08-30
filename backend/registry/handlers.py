from asgiref.sync import sync_to_async
from .models import Chart

@sync_to_async
def get_all(model):
    return list(model.objects.all())

@sync_to_async
def get_dashboard_charts(id: str):
    return list(Chart.objects.filter(dashboard=id).all())