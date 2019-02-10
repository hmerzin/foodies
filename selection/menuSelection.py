from menuFilter import menuFilter
import json, sys


def menuSelection(menuCollection, pricePref, menuPreferences):
    print(menuFilter(menuCollection, pricePref, menuPreferences))


# will later add menuPreferences parameter to better select menu item
dictionary = json.loads(sys.argv[1])

menuSelection(dictionary.get("menu"), dictionary.get("price"), [])
