
import requests
import json
import functools
import logging

logger = logging.getLogger(__name__).addHandler(logging.NullHandler()) # Uncomment this to see errors.

OSRMKEY = "5b3ce3597851110001cf62488dd14a1df3a24e80a7289a189b60edf0"
OSRMrequestendpoint = "https://api.openrouteservice.org/matrix"

requestparams = {
'api_key': OSRMKEY,
'profile': 'driving-car'}

def addDrivingTime(restaurants, srcLon, srcLat):
    if  len(restaurants) == 0:
        logger.warning("Attempted to retrieve the driving distance of an empty list of restaurants, are you okay?")
        # I'm following the design recipe here wow.
        return restaurants
    elif (len(restaurants) > 49):
        # The osrm has a limit of 50 locations. We add one location for ourself.
        logger.warning("Warning you are creating more than one request by asking for more than 49 restaurants.")
        return addDrivingTime(restaurants[0:49], srcLon, srcLat) + addDrivingTime(restaurants[49:], srcLon, srcLat)
    else:
        params = requestparams.copy()
        # We must make the first location our street address to request
        # distances to it.
        locations = "{},{}|".format(srcLon, srcLat)
        # Ugly code to make restaurants appear in the shape {lon},{lat}|... etc.
        otherlocations = "|".join(list(map(
            lambda i: "{},{}".format(i["longitude"],i["latitude"]), restaurants)))
        # We add the weird code to our street address location. Note that now
        # the index of each restaurant is its index in restaurants + 1. The
        # offset is from our current location.
        params["locations"] = locations + otherlocations
        # Destinations specifies that we wish to only distances from each location
        # to the first location.
        params["destinations"] = '0'
        try:
            r = requests.get(OSRMrequestendpoint, params=params)
            success = r.raise_for_status()
            data = r.json()

        except requests.exceptions.RequestException as requesterr:
            if requesterr is requests.exceptions.HTTPerror:
                if requesterr.response.status_code == 403:
                    logger.error("Key is not authorized for openrouteservice!" +
                    " This could mean that a daily quota has been reached.")
                elif requesterr.response.status_code == 413 or requesterr.response.status_code == 6004:
                    logger.error("Hit capacity of openrouteservice! This should" +
                        "of not happened! This is because we limit requests to" +
                        "49 of them.")
                else:
                    logger.error("There was a non-distinct http error. Error {}".format())
            else:
                logger.error("There was a non-descript error oh no!")
        if success == False:
            for i, restaurant in enumerate(restaurants):
                # We fall back to a min wait time for the restaurant.
                restaurant["drivingTime"] = restaurant["minWaitTime"]
                restaurants[i] = restaurant # Not really sure how mutation
                # works here in for loops and stuff so I'm trying to be safe.
        else:
            # We depend on the same order of restaurants being conserved.
            for i, restaurant in enumerate(restaurants):
                drivingTime = data.get("durations")[i + 1][0]
                if drivingTime is None:
                    # If JSON returns that the route is null, signifying that no
                    # route could be found. Then we will return a high time to avoid
                    # picking from it.
                    logger.error("Received null route from openrouteservice, from " +
                        "(lat,lng) {},{} to {},{}".format(srcLat,srcLon,restaurant['latitude'],restaurant['longitude']))
                    restaurant["drivingTime"] = restaurant["minWaitTime"]
                else:
                    restaurant["drivingTime"] = data.get("durations")[i + 1][0]
                    restaurants[i] = restaurant
        return restaurants
