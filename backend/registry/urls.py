from django.urls import path

from registry.api import api

# from registry.charts_api import chart_api

urlpatterns = [
    path("", api.urls),
    # path("", chart_api.urls)
]
