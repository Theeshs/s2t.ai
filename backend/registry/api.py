from ninja import NinjaAPI
from .schema import DashboardSchema
from .models import Dashboard
from django.db.utils import IntegrityError
from rest_framework import status
from typing import List
from asgiref.sync import sync_to_async
from .handlers import get_all
from datetime import datetime

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