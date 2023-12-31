from datetime import datetime
from typing import List

from asgiref.sync import sync_to_async
from django.db.utils import IntegrityError
from django.http import HttpRequest, JsonResponse
from ninja import NinjaAPI, Query
from rest_framework import status

from utils.chart_handlers import BarChart, LineChart, PieChart, get_columns
from utils.elasticsearch import ElasticSearchConnection

from .handlers import get_all, get_dashboard_charts
from .models import Chart, ChartType, Dashboard
from .schema import (
    ChartCreateSchema,
    ChartsOutSchema,
    ChartTypeCreateSchema,
    ChartTypeCreateSchemaOut,
    ChartUpdatePayload,
    DashboardSchema,
    DataSourcesOutResponse,
)
from utils.chart_handlers import get_data_sources

api = NinjaAPI()


@api.exception_handler(IntegrityError)
def dashboard_already_available(request, exc):
    return api.create_response(
        request,
        {"message": "Dashboard alread exists"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api.exception_handler(Dashboard.DoesNotExist)
def dashboard_not_available(request, exc):
    return api.create_response(
        request,
        {"message": "Dashboard does not exists"},
        status=status.HTTP_404_NOT_FOUND,
    )


@api.post("/dashboard", response=DashboardSchema)
async def dashboard_create(request, dashboard_payload: DashboardSchema):
    dashboard = await Dashboard.objects.acreate(name=dashboard_payload.name)
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
async def delete_dashboard(request, id: int):
    dashboard = await Dashboard.objects.aget(id=id)
    await dashboard.adelete()
    return api.create_response(
        request=request, data={}, status=status.HTTP_204_NO_CONTENT
    )


@api.put("/dashboard/{id}", response=DashboardSchema)
async def update_dashboard(request, id: int, dashboard_payload: DashboardSchema):
    dashboard = await Dashboard.objects.aget(id=id)
    dashboard.name = dashboard_payload.name
    dashboard.updated_at = datetime.now()
    await dashboard.asave()
    return dashboard


@api.get("/healthcheck")
def health_check(request):
    return "Hello"


@api.get("/dashboard/{id}/charts", response=List[ChartsOutSchema])
async def list_dashboard_charts(request, id: int):
    charts = await sync_to_async(get_dashboard_charts)(id)
    if not charts:
        return JsonResponse(
            {
                "msg": "No charts available",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    temp_charts = []
    for chart in charts:
        temp_charts.append(
            {
                "id": chart.id,
                "name": chart.name,
                "order": chart.order,
                "chart_type": chart.chart_type_id,
                "chart_config": chart.chart_config,
                "height": chart.chart_height,
                "width": chart.chart_width
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
        "chart_config": payload.chart_config,
        "chart_height": payload.height,
        "chart_width": payload.width
    }
    chart = await Chart.objects.acreate(**chart_payload)
    chart = {
        "id": chart.id,
        "name": chart.name,
        "order": chart.order,
        "chart_type": chart.chart_type_id,
        "chart_config": chart.chart_config,
        "height": chart.chart_height,
        "width": chart.chart_width
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
async def process_chart_data(
    request, dashboard_id: int, chart_id: int, payload: ChartUpdatePayload
):
    chart = await Chart.objects.aget(dashboard=dashboard_id, id=chart_id)
    if chart:
        chart_type = await ChartType.objects.aget(id=chart.chart_type_id)
        if chart_type.chart_type == "pie":
            pie = PieChart(payload.dataSourceName, payload.xAxis, payload.yAxis)
            series = await sync_to_async(pie.get_pie_chart_data)()
            chart.chart_config["series"] = [series]
            chart.chart_config["title"]["text"] = payload.title
        elif chart_type.chart_type == "bar":
            bar = BarChart(payload.dataSourceName, payload.xAxis, payload.yAxis)
            series = await sync_to_async(bar.get_bar_chart_data)()
            chart.chart_config["series"] = [series]
            chart.chart_config["title"]["text"] = payload.title
            chart.chart_config["subtitle"]["text"] = payload.subTitle
            chart.chart_config["yAxis"]["title"]["text"] = payload.yAxis
        elif chart_type.chart_type == "line":
            line = LineChart(payload.dataSourceName, None, payload.linChartValues)
            series = await sync_to_async(line.get_line_chart_data)()
            chart.chart_config["series"] = series
            chart.chart_config["title"]["text"] = payload.title
            chart.chart_config["subtitle"]["text"] = payload.subTitle
            chart.chart_config["yAxis"]["title"]["text"] = payload.yAxis

        await chart.asave()
        return {
            "id": chart.id,
            "name": chart.name,
            "order": chart.order,
            "chart_type": chart.chart_type_id,
            "chart_config": chart.chart_config,
        }
    else:
        print("unable to find the chart")

    return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)


@api.get("/chart/{type_id}/datasources", response=DataSourcesOutResponse)
async def get_datasources(request, type_id: int):
    chart_type = await ChartType.objects.aget(id=type_id)
    data_sources = await sync_to_async(get_data_sources)(chart_type.chart_type)
    data = {
        "chart_type_id": chart_type.id,
        "chart_type": chart_type.chart_type,
        "data_sources": data_sources,
    }
    return data


@api.get("/chart/{data_source_name}", response=List[str])
async def get_data_source_columns(request: HttpRequest, data_source_name: str):
    chart_type = request.GET.get("chart_type", "pie")
    columns = await sync_to_async(get_columns)(data_source_name, chart_type)
    return list(columns)


@api.delete("dashboard/chart/{id}")
async def delete_chart(request, id: int):
    chart = await Chart.objects.aget(id=id)
    await chart.adelete()
    return api.create_response(
        request=request, data={}, status=status.HTTP_204_NO_CONTENT
    )
