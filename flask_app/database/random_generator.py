

import random


def random_location():
    #return random location
    city = [
            "Zürich",
            "Bern",
            "Basel",
            "Luzern",
            "St. Gallen",
            "Genf",
            "Lausanne",
            "Lugano",
            "Zug",
            "Winterthur",
            "Chur",
            "Schaffhausen",
            "Aarau",
    ]
    #retrurns a random city 
    return random.choice(city)

def random_size():
    #return a random number between 50 and 200 in steps of 10
    return random.randrange(5, 50)*10

def random_rooms():
    #return a random number between 1 and 5 in steps of 0.5
    return random.randrange(2, 10)/2

def random_bool():
    #return a random 1 or 0
    return random.randrange(0, 2)

def random_year():
    #return a random year between 1950 and 2020
    return random.randrange(1950, 2020)

