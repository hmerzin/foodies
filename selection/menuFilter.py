from random import randrange


def menuFilter(menuCollection, pricePref, menuPreferences):
    priceHigh = pricePref
    priceLow = pricePref - pricePref * .2
    newMenu = []

    size = len(menuCollection)

    for food in menuCollection:
        basePrice = food.get("basePrice")
        if (basePrice <= priceHigh and basePrice >= priceLow):
            newMenu.append(food)
            menuCollection.remove(food)


    return spendRest(newMenu, pricePref, menuCollection, size)



def spendRest(entrees, priceLeft, menu, size):
    items = []

    if len(entrees) == 1:
        entree = entrees[0]
        items.append(entree.get("apiKey"))
        priceLeft -= entree.get("basePrice")
    elif len(entrees) > 1:
        entree = entrees[randrange(len(entrees) - 1)]
        items.append(entree.get("apiKey"))
        priceLeft -= entree.get("basePrice")

    menu = sorted(menu, key=lambda i: i['basePrice'], reverse=True)

    for food in menu:
        if priceLeft - food.get("basePrice") >= 0:
            items.append(food.get("apiKey"))
            priceLeft -= food.get("basePrice")

    return items