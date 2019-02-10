from random import randrange


def menuFilter(menuCollection, pricePref, menuPreferences):
    priceHigh = pricePref + pricePref * .2
    priceLow = pricePref - pricePref * .2
    newMenu = []

    for food in menuCollection:
        basePrice = food.get("basePrice")
        if (basePrice <= priceHigh and basePrice >= priceLow):
            newMenu.append(food)

    if len(newMenu) == 0:
        return evasiveManeuvers(menuCollection, pricePref)
    elif len(newMenu) == 1:
        return [newMenu[0].get("apiKey")]
    else:
        return [newMenu[randrange(len(newMenu) - 1)].get("apiKey")]


def evasiveManeuvers(menu, pricePref):

    items = []
    priceLeft = pricePref
    while priceLeft > 0:
        item = menu[randrange(len(menu) - 1)]
        items.append(item.get("apiKey"))

        priceLeft -= item.get("basePrice")
    if len(items) < 1:
        return None
    return items
