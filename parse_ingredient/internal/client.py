import json
from urllib import request

import parse_ingredient.ingredient


class Error(Exception):
    pass


class ZestfulServerError(Error):
    pass


class InsufficientQuotaError(Error):
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
        results_raw = self._send_request([ingredient])
        _check_quota(results_raw)
        if results_raw['error']:
            raise ZestfulServerError('failed to parse ingredient: %s' %
                                     results_raw['error'])
        if len(results_raw['results']) != 1:
            raise ValueError(
                'Unexpected response from server. Expected 1 result, got %d' %
                len(results_raw['results']))
        result_raw = results_raw['results'][0]

        if result_raw['error']:
            raise ZestfulServerError('failed to parse ingredient: %s' %
                                     result_raw['error'])

        return parse_ingredient.ingredient.ParsedIngredient(
            confidence=result_raw['confidence'],
            product=result_raw['ingredientParsed']['product'],
            product_size_modifier=result_raw['ingredientParsed']
            ['productSizeModifier'],
            quantity=result_raw['ingredientParsed']['quantity'],
            unit=result_raw['ingredientParsed']['unit'],
            preparation_notes=result_raw['ingredientParsed']
            ['preparationNotes'],
            usda_info=parse_ingredient.ingredient.UsdaInfo(
                category=result_raw['ingredientParsed']['usdaInfo']['category'],
                description=result_raw['ingredientParsed']['usdaInfo']
                ['description'],
                fdc_id=result_raw['ingredientParsed']['usdaInfo']['fdcId'],
                match_method=result_raw['ingredientParsed']['usdaInfo']
                ['matchMethod']))

    def parse_ingredients(self, ingredients):
        results_raw = self._send_request(ingredients)
        _check_quota(results_raw)
        if results_raw['error']:
            raise ZestfulServerError('failed to parse ingredients: %s' %
                                     results_raw['error'])

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


def _check_quota(server_response):
    if not server_response['error']:
        return
    server_error = server_response['error']
    if 'insufficient quota' in server_error.lower():
        raise InsufficientQuotaError(
            'You have insufficient quota to complete this request. '
            'To continue parsing ingredients, purchase a Zestful plan from '
            'https://zestfuldata.com')
