# Assumes restaurants given are open adn can deliver
from random import randrange
from yelpratings import addYelpRatings
from openstreetmaps import addDrivingTime
import sys


def restaurantFilter(dictionary):
    restaurantCollection = dictionary["restaurants"]
    foodPreference = dictionary["preferences"]
    address = dictionary["address"]

    openNewRestaurants = list(filter(lambda i: i['open'], restaurantCollection))
    newRestaurants = foodTimeDict(openNewRestaurants, foodPreference)

    timeSorted = timeSort(addDrivingTime(
            newRestaurants, address.get("longitude"), address.get("latitude")))

    ratingSorted = newRestaurants
    if len(newRestaurants) > 2:
        ratingSorted = ratingSort(addYelpRatings(timeSorted))[:len(timeSorted)//2]

    if len(timeSorted) < 1:
        return None
    elif len(timeSorted) == 1:
        return timeSorted[0]
    elif len(timeSorted) < 10:
        return timeSorted[randrange(len(timeSorted) - 1)]
    else:
        return timeSorted[randrange(10)]


def foodTimeDict(restaurants, foodPreferences):
    newRestaurants = []
    for restaurant in restaurants:
        myints = set(foodPreferences).intersection(set(restaurant["foodTypes"]))
        if restaurant["open"] and (len(myints) > 0):
            newRestaurants.append(restaurant)
    if len(newRestaurants) < 1:
        # Screw it we will add food that we don't like. :(
        for restaurant in restaurants:        
            if restaurant["open"]:
                newRestaurants.append(restaurant)

    return newRestaurants


def ratingSort(restaurants):
    return sorted(restaurants, key=lambda i: i['rating'], reverse=True)


def timeSort(restaurants):
    return sorted(restaurants, key=lambda i: i['drivingTime'])

'''if(len(set(foodPreferences).intersection(restaurant.get("foodTypes"))) >= len(foodPreferences) / 2
           and restaurant["open"]):'''
