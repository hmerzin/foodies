from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from fuzzywuzzy import fuzz

# TEMP
import sys

YELPKEY = 'sSzqoZa19QYvs_0zA_lFSBJQUYsfdDb0Q6vsoYDXMdGTAaCjVhmu_yX1vXKaBRbltJVUgkQECUTz_4dgqqyqu10KLfb9_3PQm4WmZZbG4ymqTa-ffMAqPjugyl1eXHYx'

_transport = RequestsHTTPTransport(
    url='https://api.yelp.com/v3/graphql',
    use_json=True,
    headers={'Authorization': "Bearer {}".format(YELPKEY)},
    timeout=20
)

client = Client(
    retries=1,
    transport=_transport,
    fetch_schema_from_transport=True,
)


def addYelpRatings(restaurants):
    if (len(restaurants) > 10):
        return addYelpRatings(restaurants[0:10]) + addYelpRatings(restaurants[10:])
    else:
        graphqlquery = '{'
        for i, restaurant in enumerate(restaurants):
            graphqlquery += """
            restaurant{}: search(term: "{}"
                location: "{}",
                latitude: {},
                longitude: {},
                limit: 3) {{
                total
                business {{
                    name
                    rating
                }}
                }},
            """.format(i, restaurant["name"], restaurant["streetAddress"],
                       restaurant["latitude"], restaurant["longitude"])
        graphqlquery += "\n }"
        data = client.execute(gql(graphqlquery))
        for i, restaurant in enumerate(restaurants):
            if "restaurant{}".format(i) in data and int(data["restaurant{}".format(i)]["total"]) > 0:
                matchedRestaurant = max(data["restaurant{}".format(i)]["business"],
                                        key=lambda r: (fuzz.ratio(restaurant["name"], r["name"])))
                restaurants[i]["rating"] = matchedRestaurant["rating"]
            else:
                # We just have to skip if it's not there!
                # We give it a 2.0 rating.
                restaurants[i]["rating"] = 2.0
        return restaurants
