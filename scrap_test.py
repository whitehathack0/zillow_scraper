import json
from datetime import datetime

import psycopg2
import googlemaps
import requests
from celery import shared_task
from app.app import create_celery_app
import logging


celery = create_celery_app()
gmaps = googlemaps.Client(key='AIzaSyB6UC_ftwdvmQHWOx2BZA5PEbHidflYkbc')
api_key = "215f50cb-7886-4f70-ba0e-0d69959a789a"


if __name__ == "__main__":
    address = "92 Brandywine Rd Franklin MA 02038"
    now = datetime.now()
    directions_result = gmaps.directions(address,
                                         "Government center, boston, MA",
                                         mode="transit",
                                         departure_time=now)

    # print(directions_result)
    print(type(directions_result[0]))

    # # Serializing json
    json_object = json.dumps(directions_result[0])

    print(directions_result[0]["legs"][0]["distance"]["value"]) # meters
    print(directions_result[0]["legs"][0]["duration"]["value"]) # minutes
    #
    # decoded = json.loads(json_object)
    #
    # print(json.loads(directions_result[0]))

