import dataclasses


@dataclasses.dataclass
class UsdaInfo:
    category: str
    description: str
    fdc_id: str
    match_method: str

    def as_dict(self):
        return {
            'category': self.category,
            'description': self.description,
            'fdcId': self.fdc_id,
            'matchMethod': self.match_method,
        }


@dataclasses.dataclass
class ParsedIngredient:
    confidence: float
    product: str
    product_size_modifier: str
    quantity: float
    unit: str
    preparation_notes: str
    usda_info: UsdaInfo

    def as_dict(self):
        return {
            'confidence': self.confidence,
            'product': self.product,
            'productSizeModifier': self.product_size_modifier,
            'quantity': self.quantity,
            'unit': self.unit,
            'preparationNotes': self.preparation_notes,
            'usda_info': self.usda_info.as_dict(),
        }


@dataclasses.dataclass
class ParsedIngredientEntry:
    error: str
    raw: str
    parsed: ParsedIngredient

    def as_dict(self):
        return {
            'error': self.error,
            'raw': self.raw,
            'parsed': self.parsed.as_dict()
        }


@dataclasses.dataclass
class ParsedIngredients:
    ingredients: list

    def as_dict(self):
        return [d.as_dict() for d in self.ingredients]
