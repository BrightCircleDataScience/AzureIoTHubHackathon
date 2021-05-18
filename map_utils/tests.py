from django.test import TestCase
from django.urls import reverse
import requests
import json
import urllib
import geojson
from datetime import datetime, timedelta

# Create your tests here.
from .models import MapData
from .models import DataPoint
from .models import jsonFeature


class ModelTestCase(TestCase):
    """
    This class defines the test suite for the MapData
    """

    def setUp(self):
        """
        create an example
        """
        self.map_name = "Test Name of Maps"
        self.map = MapData(name=self.map_name)

    def test_model_can_create_a_map(self):
        """
        Test the model can create properly
        """
        old_count = MapData.objects.count()
        self.map.save()
        new_count = MapData.objects.count()
        self.assertNotEqual(old_count, new_count)


class ApiTestCase(TestCase):
    """
    This class defines the test suite for MapData
    """

    def setUp(self):
        self.bingAuthKey = "Avq87EKSQtov6dqWm4E8-h4UvjHKsmaNIZMW36SigisVYPBhm7jLv3-QECsD74PG"
        self.url = reverse("map_endpoint")
        self.convertUrl = reverse("converter_endpoint")
        self.jsonUrl = reverse("geojson_endpoint")
        # create some test DataPoints two unprocessed and one processed
        DataPoint.objects.create(
            # in degrees celsius
            temperature=25.5,
            # This is a percentage
            humidity=52,
            # micrograms per cubic meter
            particulates=25.55,
            # 10-500 ppm
            volatile_organic_compounds=300,
            longitude=52.334,
            latitude=50.445,
            altitude=55.666,
            # time stamp
            time_taken=datetime.now(),
            # processed boolean
            processed=False)
        DataPoint.objects.create(
            # in degrees celsius
            temperature=25.7,
            # This is a percentage
            humidity=52,
            # micrograms per cubic meter
            particulates=25.55,
            # 10-500 ppm
            volatile_organic_compounds=300,
            longitude=32.334,
            latitude=30.445,
            altitude=15.666,
            # time stamp
            time_taken=datetime.now(),
            # processed boolean
            processed=False)
        DataPoint.objects.create(
            # in degrees celsius
            temperature=35.5,
            # This is a percentage
            humidity=82,
            # micrograms per cubic meter
            particulates=125.55,
            # 10-500 ppm
            volatile_organic_compounds=300,
            longitude=92.334,
            latitude=30.445,
            altitude=25.666,
            # time stamp
            time_taken=datetime.now(),
            # processed boolean
            processed=True)
        jsonFeature.objects.create(
            processed_time=datetime.now(),
            time_taken=datetime.now()-timedelta(days=1),
            jsonString="{\"geometry\": {\"coordinates\": [50.445, 52.334], \"type\": \"Point\"}, \"properties\": {\"Altitude\": 55.666, \"Humidity\": 52, \"Particle\": 25.55, \"Temperature\": 25.5, \"Time\": \"2021-05-12 01:30:23.189641+00:00\", \"VOC\": 300}, \"type\": \"Feature\"}")
        jsonFeature.objects.create(
            processed_time=datetime.now(),
            time_taken=datetime.now()-timedelta(days=3),
            jsonString="{\"geometry\": {\"coordinates\": [50.445, 52.334], \"type\": \"Point\"}, \"properties\": {\"Altitude\": 55.666, \"Humidity\": 52, \"Particle\": 25.55, \"Temperature\": 25.5, \"Time\": \"2021-05-12 01:30:23.189641+00:00\", \"VOC\": 300}, \"type\": \"Feature\"}")

    def test_check_post_call(self):
        # This endpoint should take the start and
        # end point and return the directions.
        check_endpoint = '/maps/Map?start=cranston,ri&end=providence,ri'
        response = self.client.get(check_endpoint)
        self.assertEqual(200, response.status_code)

    def test_conversion_endpoint(self):
        # Need to create telemetry data to the endpoint
        telemetry_input = [{
            "Particle": 1.0,
            "Altitude": 10,
            "Temperature": 10,
            "Temperature Unit": 'K',
            "Longitude": 10.120,
            "Latitude": 10.3939
        }, {
            "Particle": 2.0,
            "Altitude": 20,
            "Temperature": 40,
            "Temperature Unit": 'K',
            "Longitude": 40.120,
            "Latitude": 30.3939
        }]
        telemetry_input_json = json.dumps(telemetry_input)
        response = self.client.post(self.convertUrl,
                                    telemetry_input_json,
                                    content_type="application/json")
        # Should return the desired format for Bing
        # Maps consumption, which would be in GEO JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'"Processing Complete"')

    def test_json_output(self):
        time_param = 4
        response = self.client.get(
            self.jsonUrl + "?time=" + str(time_param))
        response_json = response.content.decode('utf8')
        response_data = json.loads(response_json)
        self.assertEqual(len(response_data), 2)
