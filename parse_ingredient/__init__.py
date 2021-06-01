from parse_ingredient.internal import client as zestful_client


def parse(ingredient):
    """Parses a single ingredient.

    Args:
        ingredient: A string ingredient, such as '2 cups finely chopped beets'.

    Returns:
        ParsedIngredient object containing the ingredient as structured data.
    """
    return client().parse_ingredient(ingredient)


def parse_multiple(ingredients):
    """Parses a list of ingredients.

    Args:
        ingredients: A list of ingredient strings to parse.

    Returns:
        ParsedIngredients object containing the list of parsed ingredients as
        structured data.
    """
    return client().parse_ingredients(ingredients)


def client(endpoint_url=None, rapid_api_key=None):
    """Create a new Zestful client instance for parsing ingredients.

    Args:
        endpoint_url: (optional) URL of Zestful server to use for parsing. If
            not specified, defaults to the Zestful demo server.
        rapid_api_key: API key from RapidAPI to make queries on a paid RapidAPI
            subscription to Zestful.

    Returns:
        A Client instance with the methods parse_ingredient and
        parse_ingredients, whose semantics are identical to the methods above.
    """
    return zestful_client.Client(endpoint_url=endpoint_url,
                                 rapid_api_key=rapid_api_key)
