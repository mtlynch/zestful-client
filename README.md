# Ingredient Parser (Zestful Client)

[![PyPI](https://img.shields.io/pypi/v/zestful-parse-ingredient)](https://pypi.org/project/zestful-parse-ingredient/)
[![CircleCI](https://circleci.com/gh/mtlynch/zestful-client.svg?style=svg)](https://circleci.com/gh/mtlynch/zestful-client)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](LICENSE)

## Overview

Parse recipe ingredient strings into structured data.

## Examples

### Parse a single ingredient

```python
import json
import parse_ingredient

ingredient = parse_ingredient.parse('2 1/2 tablespoons finely chopped parsley')
print(json.dumps(ingredient.as_dict()))
```

```json
{
  "quantity": 2.5,
  "unit": "tablespoon",
  "product": "parsley",
  "productSizeModifier": null,
  "preparationNotes": "finely chopped",
  "usdaInfo": {
      "category": "Vegetables and Vegetable Products",
      "description": "Parsley, fresh",
      "fdcId": "170416",
      "matchMethod": "exact"
  },
  "confidence": 0.9858154,
}
```


### Parse multiple ingredients

```python
import json
import parse_ingredient

ingredients = parse_ingredient.parse_multiple([
  '2 1/2 tablespoons finely chopped parsley',
  '3 large Granny Smith apples'
  )
print(json.dumps(ingredients.as_dict()))
```

```json
[
  {
    "ingredientRaw": "3 large Granny Smith apples",
    "ingredientParsed": {
        "preparationNotes": "finely chopped",
        "product": "parsley",
        "productSizeModifier": null,
        "quantity": 2.5,
        "unit": "tablespoon",
        "usdaInfo": {
            "category": "Vegetables and Vegetable Products",
            "description": "Parsley, fresh",
            "fdcId": "170416",
            "matchMethod": "exact"
        },
        "confidence": 0.9858154,
    },
    "error": null,
  },
  {
      "ingredientRaw": "3 large Granny Smith apples",
      "ingredientParsed": {
          "preparationNotes": null,
          "product": "Granny Smith apples",
          "productSizeModifier": "large",
          "quantity": 3.0,
          "unit": null,
          "usdaInfo": {
              "category": "Fruits and Fruit Juices",
              "description": "Apples, raw, granny smith, with skin (Includes foods for USDA's Food Distribution Program)",
              "fdcId": "168203",
              "matchMethod": "exact"
          },
          "confidence": 0.9741028,
      },
      "error": null,
  }
]
```

### Parse ingredients using RapidAPI

If you have a [RapidAPI subscription](https://rapidapi.com/zestfuldata/api/recipe-and-ingredient-analysis) to Zestful, you can use your API key as follows:

```python
import json
import parse_ingredient

# Replace this with your key from RapidAPI
# https://rapidapi.com/zestfuldata/api/recipe-and-ingredient-analysis
RAPID_API_KEY = 'your-rapid-api-key'

client = parse_ingredient.client(rapid_api_key=RAPID_API_KEY)

ingredient = client.parse_ingredient('2 1/2 tablespoons finely chopped parsley')
print(json.dumps(ingredient.as_dict()))
```

### Use private Zestful server

If you have a private Zestful ingredient parsing server as part of an Enterprise plan, you can use the library as follows:

```python
import parse_ingredient

ENDPOINT_URL = 'https://zestful.yourdomain.com'

client = parse_ingredient.client(endpoint_url=ENDPOINT_URL)

ingredient = client.parse_ingredient('2 1/2 tablespoons finely chopped parsley')
print(json.dumps(ingredient.as_dict()))
```

## Installation

### From pip

```bash
pip install parse-ingredient
```

### From source

```bash
git clone https://github.com/mtlynch/zestful-client.git
cd zestful-client
pip install .
```

## Full documentation

For full documentation of each result field, see the official [Zestful API documentation](https://zestfuldata.com/docs).
