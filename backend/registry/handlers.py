from asgiref.sync import sync_to_async
from .models import Chart

@sync_to_async
def get_all(model):
    return list(model.objects.all())


def get_dashboard_charts(id: str):
    charts = Chart.objects.filter(dashboard=id).all()
    if not charts.exists():
        return None
    return list(charts)