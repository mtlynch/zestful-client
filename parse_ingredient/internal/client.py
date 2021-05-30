import json
from urllib import request

import parse_ingredient.ingredient


class Error(Exception):
    pass


class IngredientParserApiError(Error):
    pass


_DEMO_ENDPOINT_URL = 'https://sandbox.zestfuldata.com'
_RAPID_API_DOMAIN = 'zestful.p.rapidapi.com'
_RAPID_API_URL = 'https://' + _RAPID_API_DOMAIN


class Client:

    def __init__(self, endpoint_url=None, rapid_api_key=None):
        self._rapid_api_key = rapid_api_key
        if endpoint_url:
            self._endpoint_url = endpoint_url
        elif self._rapid_api_key:
            self._endpoint_url = _RAPID_API_URL
        else:
            self._endpoint_url = _DEMO_ENDPOINT_URL

    def parse_ingredient(self, ingredient):
        results = self._send_request([ingredient])
        if results['error']:
            raise ValueError('TODO')
        if len(results['results']) != 1:
            raise ValueError('Expected only one result')
        result = results['results'][0]

        if result['error']:
            raise ValueError('TODO')

        return parse_ingredient.ingredient.ParsedIngredient(
            confidence=result['confidence'],
            product=result['ingredientParsed']['product'],
            product_size_modifier=result['ingredientParsed']
            ['productSizeModifier'],
            quantity=result['ingredientParsed']['quantity'],
            unit=result['ingredientParsed']['unit'],
            preparation_notes=result['ingredientParsed']['preparationNotes'],
            usda_info=parse_ingredient.ingredient.UsdaInfo(
                category=result['ingredientParsed']['usdaInfo']['category'],
                description=result['ingredientParsed']['usdaInfo']
                ['description'],
                fdc_id=result['ingredientParsed']['usdaInfo']['fdcId'],
                match_method=result['ingredientParsed']['usdaInfo']
                ['matchMethod']))

    def parse_ingredients(self, ingredients):
        results_raw = self._send_request(ingredients)
        if results_raw['error']:
            raise ValueError('TODO')

        results = []
        for result_raw in results_raw['results']:
            results.append(
                parse_ingredient.ingredient.ParsedIngredientEntry(
                    error=result_raw['error'],
                    raw=result_raw['ingredientRaw'],
                    parsed=parse_ingredient.ingredient.ParsedIngredient(
                        confidence=result_raw['confidence'],
                        product=result_raw['ingredientParsed']['product'],
                        product_size_modifier=result_raw['ingredientParsed']
                        ['productSizeModifier'],
                        quantity=result_raw['ingredientParsed']['quantity'],
                        unit=result_raw['ingredientParsed']['unit'],
                        preparation_notes=result_raw['ingredientParsed']
                        ['preparationNotes'],
                        usda_info=parse_ingredient.ingredient.UsdaInfo(
                            category=result_raw['ingredientParsed']['usdaInfo']
                            ['category'],
                            description=result_raw['ingredientParsed']
                            ['usdaInfo']['description'],
                            fdc_id=result_raw['ingredientParsed']['usdaInfo']
                            ['fdcId'],
                            match_method=result_raw['ingredientParsed']
                            ['usdaInfo']['matchMethod']))))
        return parse_ingredient.ingredient.ParsedIngredients(
            ingredients=results)

    def _send_request(self, ingredients):
        req = request.Request(self._endpoint_url + '/parseIngredients',
                              method='POST')

        body = json.dumps({'ingredients': ingredients}).encode('utf-8')

        req.add_header('Content-Type', 'application/json')
        req.add_header('Content-Length', len(body))

        if self._rapid_api_key:
            req.add_header('x-rapidapi-key', self._rapid_api_key)
            req.add_header('x-rapidapi-host', _RAPID_API_DOMAIN)

        with request.urlopen(req, data=body) as response:
            return json.loads(response.read().decode('utf-8'))
