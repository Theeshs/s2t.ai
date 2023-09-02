from ninja import NinjaAPI
from .schema import DashboardSchema, ChartsOutSchema, ChartCreateSchema, ChartTypeCreateSchemaOut, ChartTypeCreateSchema
from .models import Dashboard
from django.db.utils import IntegrityError
from rest_framework import status
from typing import List
from asgiref.sync import sync_to_async
from .handlers import get_all, get_dashboard_charts
from datetime import datetime
from .models import Chart, ChartType
from django.http import JsonResponse

api = NinjaAPI()

@api.exception_handler(IntegrityError)
def dashboard_already_available(request, exc):
    return api.create_response(
        request,
        {"message": "Dashboard alread exists"},
        status=status.HTTP_400_BAD_REQUEST

    )

@api.exception_handler(Dashboard.DoesNotExist)
def dashboard_not_available(request, exc):
    return api.create_response(
        request,
        {"message": "Dashboard does not exists"},
        status=status.HTTP_404_NOT_FOUND

    )

@api.post("/dashboard", response=DashboardSchema)
async def dashboard_create(request, dashboard_payload: DashboardSchema):
    dashboard = await Dashboard.objects.acreate(
        name=dashboard_payload.name
    )
    return dashboard

@api.get("/dashboard", response=List[DashboardSchema])
async def dashboard_list(request):
    dashboards = await get_all(Dashboard)
    return dashboards


@api.get("/dashboard/{id}", response=DashboardSchema)
async def get_dashboard(request, id: int):
    dashboard = await Dashboard.objects.aget(id=id)
    return dashboard

@api.delete("/dashboard/{id}")
async def get_dashboard(request, id: int):
    dashboard = await Dashboard.objects.aget(id=id)
    await dashboard.adelete()
    return api.create_response(
        request=request,
        data={},
        status=status.HTTP_204_NO_CONTENT
    )

@api.put("/dashboard/{id}", response=DashboardSchema)
async def update_dashboard(request, id: int, dashboard_payload: DashboardSchema):
    dashboard = await Dashboard.objects.aget(id=id)
    dashboard.name = dashboard_payload.name
    dashboard.updated_at = datetime.now()
    dashboard.created_at = dashboard_payload.createdAt
    dashboard.is_deleted = dashboard_payload.isDeleted

    return dashboard


@api.get("/healthcheck")
def health_check(request):
    return "Hello"

@api.get("/dashboard/{id}/charts", response=List[ChartsOutSchema])
async def list_dashboard_charts(request, id: int):
    charts = await get_dashboard_charts(id)
    if not charts:
        return JsonResponse({
            "msg": "No charts available",
        }, status=status.HTTP_404_NOT_FOUND)
    return charts

@api.post("/dashboard/{id}/charts", response=ChartsOutSchema)
async def create_chart(request, id: int, payload: ChartCreateSchema):
    dashboard = await Dashboard.objects.aget(id=id)
    chart_type = await ChartType.objects.aget(id=payload.chart_type)
    chart_payload = {
        "name": payload.name,
        "order": payload.order,
        "chart_type": chart_type,
        "dashboard": dashboard
    }
    chart = await Chart.objects.acreate(**chart_payload)
    chart = {
        "id": chart.id,
        "name": chart.name,
        "order": chart.order,
        "chart_type": chart.chart_type_id
    }
    return chart

@api.post("/chart_type", response=ChartTypeCreateSchemaOut)
async def create_chart_type(request, palyload: ChartTypeCreateSchema):
    chart_type = await ChartType.objects.acreate(chart_type=palyload.chart_type)
    return chart_type