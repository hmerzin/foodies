from restaurantFilter import restaurantFilter
import json
import sys

def getRestaurant(dictionary):
    restaurant = restaurantFilter(dictionary)
    if restaurant is None:    
        print("ERROROHCRAP")    
    else:        
        print(restaurant.get("apiKey"))

dictionary = json.loads(sys.argv[1])

getRestaurant(dictionary)
