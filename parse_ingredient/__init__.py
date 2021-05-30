from parse_ingredient.internal import client as zestful_client


def parse(ingredient):
    return client().parse_ingredient(ingredient)


def parse_multiple(ingredients):
    return client().parse_ingredients(ingredients)


def client(endpoint_url=None, rapid_api_key=None):
    return zestful_client.Client(endpoint_url=endpoint_url,
                                 rapid_api_key=rapid_api_key)
