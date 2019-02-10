# Assumes restaurants given are open adn can deliver
from random import randrange
from yelpratings import addYelpRatings
from openstreetmaps import addDrivingTime
import sys


def restaurantFilter(dictionary):
    restaurantCollection = dictionary["restaurants"]
    foodPreference = dictionary["preferences"]
    address = dictionary["address"]

    #newRestaurants = foodTimeDict(
    #    restaurantCollection, foodPreference, dictionary)
    with open('/tmp/somefile.txt', 'a') as the_file:
        the_file.write('Hello\n')
    newRestaurants = list(filter(lambda i: i['open'], restaurantCollection))
    with open('/tmp/somefile.txt', 'a') as the_file:
        the_file.write('checkedopen\n')
    #ratingSorted = ratingSort(addYelpRatings(newRestaurants))[
    #    :len(newRestaurants)//2]
    #print(len(ratingSorted),file=sys.stderr)
    timeSorted = timeSort(addDrivingTime(
        newRestaurants, address.get("longitude"), address.get("latitude")))
    #print(len(timeSorted),file=sys.stderr)
    if len(timeSorted) == 1:
        return timeSorted[0]
    elif len(timeSorted) < 10:
        return timeSorted[randrange(len(timeSorted) - 1)]
    else:
        return timeSorted[randrange(10)]


def foodTimeDict(restaurants, foodPreferences, dictionary):

    # TODO: FIX TOTALPRICE TO INDICATE REFERENCE TO DELIVERY MINIMUM
    totalPrice = dictionary.get("foods") * dictionary.get("price")
    newRestaurants = []

    for restaurant in restaurants:
        print(restaurant["open"],file=sys.stderr)
        newRestaurants.append(restaurant)

    return newRestaurants


def ratingSort(restaurants):
    return sorted(restaurants, key=lambda i: i['rating'], reverse=True)


def timeSort(restaurants):
    return sorted(restaurants, key=lambda i: i['drivingTime'])

'''if(len(set(foodPreferences).intersection(restaurant.get("foodTypes"))) >= len(foodPreferences) / 2
           and restaurant["open"]):'''