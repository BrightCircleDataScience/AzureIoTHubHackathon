from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import viewsets
import requests
import json
import urllib
import geojson
from datetime import datetime, timedelta


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# Creating an API view
class MapsApiView(APIView):
    def get(self, request):
        bingAuthKey = "Avq87EKSQtov6dqWm4E8-h4UvjHKsmaNIZMW36SigisVYPBhm7jLv3-QECsD74PG"
        base_url = "http://dev.virtualearth.net/REST/V1/Routes/Driving?"
        AUTH_KEY = bingAuthKey
        start = request.GET.get('start')
        end = request.GET.get('end')
        parameters = {"wp.0": start,
                      "wp.1": end,
                      "avoid": "minimizeTolls",
                      "key": AUTH_KEY}
        r = requests.get(f"{base_url}{urllib.parse.urlencode(parameters)}")
        list_points = DataPoint.objects.all()
        print(list_points.values())
        return Response({"Message:": "Map Route Data", "Data:": r})

    def post(self, request):
        point = DataPoint.objects.create(
            # in degrees celsius
            temperature=request.data.get('temperature'),
            # This is a percentage
            humidity=request.data.get('humidity'),
            # micrograms per cubic meter
            particulates=request.data.get('particulates'),
            # 10-500 ppm
            volatile_organic_compounds=request.data.get('voc'),
            longitude=request.data.get('longitude'),
            latitude=request.data.get('latitude'),
            altitude=request.data.get('altitude'),
            # time stamp
            time_taken=request.data.get('time'),
            # processed boolean
            processed=False)
        print(point.temperature)
        return Response({"Status": "Done",
                         "Data": "point"})


class MapsConverterEndpoint(APIView):
    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def post(self, request):
        """
        Request should just look up things to process
        and then add them to the processed part of the db
        """
        # create points with Point, then Features,
        # then finally a Feature Collection
        feature_list = []
        listPoints = DataPoint.objects.filter(processed=False)
        for point in listPoints:
            lat = point.latitude
            lon = point.longitude
            geoPoint = geojson.Point((lat, lon))
            feature = geojson.Feature(geometry=geoPoint,
                                      properties={
                                          "Particle": point.particulates,
                                          "Temperature": point.temperature,
                                          "Humidity": point.humidity,
                                          "VOC": point.volatile_organic_compounds,
                                          "Altitude": point.altitude,
                                          "Time": point.time_taken.__str__()
                                      })
            jsonFeature.objects.create(jsonString=feature,
                                       processed_time=datetime.now(),
                                       time_taken=point.time_taken)
            point.processed = True
            point.save()
            feature_list.append(feature)
        
        return Response("Processing Complete")


class GeoJsonEndpoint(APIView):
    """
    This request will take a time period,
    query the json information, and
    return a collection of json
    """

    def get(self, request):
        time = request.GET.get('time')
        int_time = int(time)
        date_from = datetime.now() - timedelta(days=int_time)
        list_features = jsonFeature.objects.filter(time_taken__gte=date_from)
        print(list_features)
        list_json = []
        for feature in list_features:
            list_json.append(json.loads(feature.jsonString))

        feature_collection = geojson.FeatureCollection(list_json)
        return JsonResponse(feature_collection, safe=False)
