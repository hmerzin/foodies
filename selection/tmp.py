import json
import yelpratings
import openstreetmaps

text = """
[{ "name": "Alexandria Pizza",
   "streetAddress": "1252 Washington St",
   "latitude": 42.342431,
   "longitude": -71.067516 },
 { "name": "Ali Baba",
   "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
   "latitude": 42.343613,
   "longitude": -71.064816 },
{ "name": "Alexandria Pizza",
  "streetAddress": "1252 Washington St",
  "latitude": 42.342431,
  "longitude": -71.067516 },
{ "name": "Ali Baba",
  "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
  "latitude": 42.343613,
  "longitude": -71.064816 },
{ "name": "Alexandria Pizza",
     "streetAddress": "1252 Washington St",
     "latitude": 42.342431,
     "longitude": -71.067516 },
{ "name": "Ali Baba",
 "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
 "latitude": 42.343613,
 "longitude": -71.064816 },
 { "name": "Alexandria Pizza",
    "streetAddress": "1252 Washington St",
    "latitude": 42.342431,
    "longitude": -71.067516 },
  { "name": "Ali Baba",
    "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
    "latitude": 42.343613,
    "longitude": -71.064816 },
 { "name": "Alexandria Pizza",
   "streetAddress": "1252 Washington St",
   "latitude": 42.342431,
   "longitude": -71.067516 },
 { "name": "Ali Baba",
   "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
   "latitude": 42.343613,
   "longitude": -71.064816 },
 { "name": "Alexandria Pizza",
      "streetAddress": "1252 Washington St",
      "latitude": 42.342431,
      "longitude": -71.067516 },
 { "name": "Ali Baba",
  "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
  "latitude": 42.343613,
  "longitude": -71.064816 },
  { "name": "Alexandria Pizza",
     "streetAddress": "1252 Washington St",
     "latitude": 42.342431,
     "longitude": -71.067516 },
   { "name": "Ali Baba",
     "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
     "latitude": 42.343613,
     "longitude": -71.064816 },
  { "name": "Alexandria Pizza",
    "streetAddress": "1252 Washington St",
    "latitude": 42.342431,
    "longitude": -71.067516 },
  { "name": "Ali Baba",
    "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
    "latitude": 42.343613,
    "longitude": -71.064816 },
  { "name": "Alexandria Pizza",
       "streetAddress": "1252 Washington St",
       "latitude": 42.342431,
       "longitude": -71.067516 },
  { "name": "Ali Baba",
   "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
   "latitude": 42.343613,
   "longitude": -71.064816 },
   { "name": "Alexandria Pizza",
      "streetAddress": "1252 Washington St",
      "latitude": 42.342431,
      "longitude": -71.067516 },
    { "name": "Ali Baba",
      "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
      "latitude": 42.343613,
      "longitude": -71.064816 },
   { "name": "Alexandria Pizza",
     "streetAddress": "1252 Washington St",
     "latitude": 42.342431,
     "longitude": -71.067516 },
   { "name": "Ali Baba",
     "streetAddress": "145 East Berkeley St Boston, Massachusetts 02118",
     "latitude": 42.343613,
     "longitude": -71.064816 }]
"""

restaurants = yelpratings.addYelpRatings(openstreetmaps.addDrivingTime(json.loads(text), -71.0438222, 42.3545997))
print(restaurants)