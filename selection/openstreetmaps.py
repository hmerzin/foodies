import requests
import json
import functools

OSRMKEY = "5b3ce3597851110001cf62488dd14a1df3a24e80a7289a189b60edf0"
OSRMrequestendpoint = "https://api.openrouteservice.org/matrix"

requestparams = {
'api_key': OSRMKEY,
'profile': 'driving-car'}

def addDrivingTime(restaurants, srcLon, srcLat):
    if (len(restaurants) > 49):
        return addDrivingTime(restaurants[0:49], srcLon, srcLat) + addDrivingTime(restaurants[49:], srcLon, srcLat)
    else:
        params = requestparams.copy()
        locations = "{},{}|".format(srcLon, srcLat)
        otherlocations = "|".join(map(
            lambda i: "{},{}".format(i["longitude"],i["latitude"]), restaurants))
        params["locations"] = locations + otherlocations
        params["destinations"] = '0'
        r = requests.get(OSRMrequestendpoint, params=params)
        data = r.json()
        # We depend on the same order of restaurants being conserved.
        for i, restaurant in enumerate(restaurants):
            restaurant["drivingTime"] = data.get("durations")[i + 1][0]
            restaurants[i] = restaurant
        return restaurants
