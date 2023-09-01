from ninja import NinjaAPI
from .models import Chart, ChartType
from .handlers import get_dashboard_charts
from .schema import ChartsOutSchema

chart_api = NinjaAPI()

@chart_api.get("/healthcheck")
def health_check(request):
    return "Hello"

@chart_api.get("/dashboard/{id}/charts", response=ChartsOutSchema)
async def list_dashboard_charts(request, id: int):
    charts = await get_dashboard_charts(Chart, "dashboard", id)
    return charts

@chart_api.post("/dashboard/{id}/charts", response=ChartsOutSchema)
def create_chart():
    return