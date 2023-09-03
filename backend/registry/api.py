from ninja import NinjaAPI
from .schema import DashboardSchema, ChartsOutSchema, ChartCreateSchema, ChartTypeCreateSchemaOut, ChartTypeCreateSchema, ChartUpdatePayload
from .models import Dashboard
from django.db.utils import IntegrityError
from rest_framework import status
from typing import List
from asgiref.sync import sync_to_async
from .handlers import get_all, get_dashboard_charts
from datetime import datetime
from .models import Chart, ChartType
from django.http import JsonResponse
from utils.elasticsearch import ElasticSearchConnection
from utils.chart_handlers import PieChart

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
    charts = await sync_to_async(get_dashboard_charts)(id)
    if not charts:
        return JsonResponse({
            "msg": "No charts available",
        }, status=status.HTTP_404_NOT_FOUND)

    temp_charts = []
    for chart in charts:
        temp_charts.append(
            {
                "id": chart.id,
                "name": chart.name,
                "order": chart.order,
                "chart_type": chart.chart_type_id,
                "chart_config": chart.chart_config
            }
        )
    return temp_charts

@api.post("/dashboard/{id}/charts", response=ChartsOutSchema)
async def create_chart(request, id: int, payload: ChartCreateSchema):
    dashboard = await Dashboard.objects.aget(id=id)
    chart_type = await ChartType.objects.aget(id=payload.chart_type)
    chart_payload = {
        "name": payload.name,
        "order": payload.order,
        "chart_type": chart_type,
        "dashboard": dashboard,
        "chart_config": payload.chart_config
    }
    chart = await Chart.objects.acreate(**chart_payload)
    chart = {
        "id": chart.id,
        "name": chart.name,
        "order": chart.order,
        "chart_type": chart.chart_type_id,
        "chart_config": chart.chart_config
    }
    return chart

@api.post("/chart_type", response=ChartTypeCreateSchemaOut)
async def create_chart_type(request, palyload: ChartTypeCreateSchema):
    chart_type = await ChartType.objects.acreate(chart_type=palyload.chart_type)
    return chart_type

@api.get("/chart_type", response=List[ChartTypeCreateSchemaOut])
async def get_chart_types(request):
    chart_types = await get_all(ChartType)
    return chart_types

@api.put("/dashboard/{dashboard_id}/chart/{chart_id}/data", response=ChartsOutSchema)
async def process_chart_data(request, dashboard_id: int, chart_id: int, payload: ChartUpdatePayload):
    chart = await Chart.objects.aget(dashboard=dashboard_id, id=chart_id)
    if chart:
        chart_type = await ChartType.objects.aget(id=chart.chart_type_id)
        if chart_type.chart_type == 'pie':
            pie = PieChart("file_1", "name", "salary")
            series = await sync_to_async(pie.get_pie_chart_data)()
            chart.chart_config["series"] = [series]
            chart.chart_config["title"] = payload.title
        
        await chart.asave()
        return {
            "id": chart.id,
            "name": chart.name,
            "order": chart.order,
            "chart_type": chart.chart_type_id,
            "chart_config": chart.chart_config
        }
    else:
        print("unable to find the chart")
    
    return JsonResponse({}, status=status.HTTP_200_OK)