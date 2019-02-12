# Assumes restaurants given are open adn can deliver
from random import randrange
from yelpratings import addYelpRatings
from openstreetmaps import addDrivingTime


def restaurantFilter(dictionary):
    restaurantCollection = dictionary["restaurants"]
    foodPreference = dictionary["preferences"]
    address = dictionary["address"]

    newRestaurants = foodTimeDict(restaurantCollection, foodPreference)

    if len(newRestaurants) > 2:
        ratingSorted = ratingSort(addYelpRatings(newRestaurants))[:len(newRestaurants)//2]

    timeSorted = timeSort(addDrivingTime(
            newRestaurants, address.get("longitude"), address.get("latitude")))

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
    restaurants = list(filter(lambda i: i['open'], restaurants))
    numOpen = len(restaurants)

    # if more than 15 are open, be picky
    if numOpen > 15:
        for restaurant in restaurants:
            myints = len(set(foodPreferences).intersection(set(restaurant["foodTypes"])))
            if (myints >= 1):
                newRestaurants.append(restaurant)

        return newRestaurants

    # if less than 15 are open, don't be picky
    elif numOpen <= 15 and numOpen > 0:
        for restaurant in restaurants:
            newRestaurants.append(restaurant)

        return newRestaurants

    # if 0 are open, throw an error
    # WILL CHANGE LATER. GRABBING CLOSED RESTAURANTS FOR TESTS
    else:
        return newRestaurants



def ratingSort(restaurants):
    return sorted(restaurants, key=lambda i: i['rating'], reverse=True)


def timeSort(restaurants):
    return sorted(restaurants, key=lambda i: i['drivingTime'])
