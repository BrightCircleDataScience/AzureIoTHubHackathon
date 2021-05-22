import geojson
import csv
from datetime import datetime
import random
import json

# read the data from csv
with open('current_bluebikes_stations.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    next(reader)
    list_json = []
    # the data can be found in the third and fourth column
    for row in reader:
        lon = float(row[2])
        lat = float(row[3])
        geoPoint = geojson.Point((lat, lon))
        feature = geojson.Feature(geometry=geoPoint,
                                  properties={
                                    "Particle": random.uniform(1.0, 3.0),
                                    "Temperature": random.randrange(70, 80),
                                    "Humidity": random.uniform(30, 50),
                                    "VOC": random.uniform(0, 5),
                                    "Time": datetime.now().__str__()
                                  })
        list_json.append(feature)
    feature_collection = geojson.FeatureCollection(list_json)
    with open('bikes.geojson', 'w') as outfile:
        json.dump(feature_collection, outfile)

# lat = point.latitude
#             lon = point.longitude
#             geoPoint = geojson.Point((lat, lon))
#             feature = geojson.Feature(geometry=geoPoint,
#                                       properties={
#                                           "Particle": point.particulates,
#                                           "Temperature": point.temperature,
#                                           "Humidity": point.humidity,
#                                           "VOC": point.volatile_organic_compounds,
#                                           "Altitude": point.altitude,
#                                           "Time": point.time_taken.__str__()
#                                       })