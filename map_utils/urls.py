from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url("Map", views.MapsApiView.as_view(), name='map_endpoint'),
    url("Telemetry_Convert", views.MapsConverterEndpoint.as_view(),
        name='converter_endpoint'),
    url("Grab_GeoJSON", views.GeoJsonEndpoint.as_view(),
        name='geojson_endpoint'),
    path('', views.index, name='index'),
]
