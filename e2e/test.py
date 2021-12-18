#!/usr/bin/env python3

import json
import logging
import os

import parse_ingredient

logger = logging.getLogger(__name__)


def configure_logging():

    class ShutdownHandler(logging.StreamHandler):

        def emit(self, record):
            super().emit(record)
            if record.levelno >= logging.CRITICAL:
                raise SystemExit(255)

    root_logger = logging.getLogger()
    handler = ShutdownHandler()
    formatter = logging.Formatter('%(levelname)-4s %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)


configure_logging()

ENDPOINT_URL = os.environ.get('ZESTFUL_SERVER', None)
if not ENDPOINT_URL:
    logger.fatal('must specify ZESTFUL_SERVER environment variable')
client = parse_ingredient.client(endpoint_url=ENDPOINT_URL)

# Test single ingredient

SINGLE_INGREDIENT = '2 1/2 tablespoons finely chopped parsley'

SINGLE_RESULT_EXPECTED = parse_ingredient.ingredient.ParsedIngredient(
    product='parsley',
    product_size_modifier=None,
    quantity=2.5,
    unit='tablespoon',
    preparation_notes='finely chopped',
    usda_info=parse_ingredient.ingredient.UsdaInfo(
        description='Parsley, fresh',
        category='Vegetables and Vegetable Products',
        fdc_id='170416',
        match_method='exact'),
    confidence=0.9858154)

logger.info('testing single ingredient %s', SINGLE_INGREDIENT)
SINGLE_RESULT_ACTUAL = client.parse_ingredient(SINGLE_INGREDIENT)
if SINGLE_RESULT_EXPECTED != SINGLE_RESULT_ACTUAL:
    logger.fatal('\n\texpected result %s\n\tactual result %s',
                 SINGLE_RESULT_EXPECTED, SINGLE_RESULT_ACTUAL)

logger.info(
    'result=%s',
    json.dumps(SINGLE_RESULT_ACTUAL.as_dict(), sort_keys=True, indent=2))

# Test multiple ingredients

MULTI_INGREDIENT = [
    '3 large Granny Smith apples',
    '½ tsp brown sugar',
    'Balduferus Cherries',  # Ensure no USDA match
]

MULTI_RESULT_EXPECTED = parse_ingredient.ingredient.ParsedIngredients(
    ingredients=[
        parse_ingredient.ingredient.ParsedIngredientEntry(
            error=None,
            raw='3 large Granny Smith apples',
            parsed=parse_ingredient.ingredient.ParsedIngredient(
                confidence=0.9741028,
                product='Granny Smith apples',
                product_size_modifier='large',
                quantity=3.0,
                unit=None,
                preparation_notes=None,
                usda_info=parse_ingredient.ingredient.UsdaInfo(
                    description=
                    'Apples, raw, granny smith, with skin (Includes foods for USDA\'s Food Distribution Program)',
                    category='Fruits and Fruit Juices',
                    fdc_id='168203',
                    match_method='exact'))),
        parse_ingredient.ingredient.ParsedIngredientEntry(
            error=None,
            raw='½ tsp brown sugar',
            parsed=parse_ingredient.ingredient.ParsedIngredient(
                confidence=0.9857134,
                product='brown sugar',
                product_size_modifier=None,
                quantity=0.5,
                unit='teaspoon',
                preparation_notes=None,
                usda_info=parse_ingredient.ingredient.UsdaInfo(
                    description='Sugars, brown',
                    category='Sweets',
                    fdc_id='168833',
                    match_method='exact'))),
        parse_ingredient.ingredient.ParsedIngredientEntry(
            error=None,
            raw='Balduferus Cherries',
            parsed=parse_ingredient.ingredient.ParsedIngredient(
                confidence=0.9857134,
                product='Balduferus Cherries',
                product_size_modifier=None,
                quantity=None,
                unit=None,
                preparation_notes=None,
                usda_info=None)),
    ])

logger.info('testing multiple ingredients %s', MULTI_INGREDIENT)
MULTI_RESULT_ACTUAL = client.parse_ingredients(MULTI_INGREDIENT)
if MULTI_RESULT_EXPECTED != MULTI_RESULT_ACTUAL:
    logger.fatal('\n\texpected result %s\n\tactual result %s',
                 MULTI_RESULT_EXPECTED, MULTI_RESULT_ACTUAL)

logger.info('result=%s',
            json.dumps(MULTI_RESULT_ACTUAL.as_dict(), sort_keys=True, indent=2))

logger.info('all tests pass!')
