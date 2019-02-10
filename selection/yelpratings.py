from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from fuzzywuzzy import fuzz
from multiprocessing import Pool
import logging

logger = logging.getLogger(__name__)

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

# Generate and gather gql query results for a given restaurant list.
# This may time out, so please use addYelpRatings which will split up
# the work in a safer ... arbitrary way ...
# This function will take a list of restaurants to produce
# a list of ratings. The point of this strategy is that it will
# become easier to collect all of the mapped slices together at the
# end to calculate for example ... an average.
def _getRestaurantsRatings(restaurants):
    if len(restaurants) == 0:
        # Don't continue! We don't want to craft an empty gql query that will
        # just be stupid.
        return []
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
                }}
            """.format(i, restaurant["name"], restaurant["streetAddress"],
            restaurant["latitude"], restaurant["longitude"])
        graphqlquery+= "\n }"
        data = client.execute(gql(graphqlquery))
        restaurantmapped = []
        for i, restaurant in enumerate(restaurants):
            if "restaurant{}".format(i) in data and int(data["restaurant{}".format(i)]["total"]) > 0:
                matchedRestaurant = max(data["restaurant{}".format(i)]["business"],
                    key=lambda r: (fuzz.ratio(restaurant["name"], r["name"])))
                restaurantmapped.append(matchedRestaurant["rating"])
            else:
                # We just have to skip if it's not there!
                restaurantmapped.append(None)
        return restaurantmapped

# This function adds yelp ratings through manageable slices.
def addYelpRatings(restaurants):
    slices = []
    if len(restaurants) == 0:
        logger.error("We don't want to fetch restaurant ratings for an empty list!" +
            " then we get an empty slice.")
        return []
    else:
        for i in range(0,len(restaurants),10):
            slices.append(restaurants[i: max(i+10,len(restaurants))])
        with Pool(5) as p:
            restaurantRatings = p.map(_getRestaurantsRatings, slices)
            N = 0
            total = 0
            for i, slice in enumerate(restaurantRatings):
                for rating in slice:
                    if rating is None:
                        pass
                    else:
                        N += 1
                        total += rating
            average = total / N if N > 1 else 0
            print(average)
            for i, slice in enumerate(restaurantRatings):
                for i2, rating in enumerate(slice):
                    restaurants[i*10 + i2]["rating"] = average if restaurantRatings[i][i2] is None else restaurantRatings[i][i2]
        return restaurants
