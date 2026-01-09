"""
Data models for Factorio Calculator.
Defines the structure for recipes, machines, modules, and belts.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Ingredient:
    name: str
    amount: float

@dataclass
class Product:
    name: str
    amount: float

@dataclass
class Recipe:
    name: str
    preferred_machine: str
    category: List[str]
    time: float
    ingredients: List[Ingredient]
    products: List[Product]
    allow_productivity: bool = True

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'Recipe':
        ingredients = [
            Ingredient(name=ing['name'], amount=ing['amount'])
            for ing in data.get('ingredients', [])
        ]
        products = [
            Product(name=prod['name'], amount=prod['amount'])
            for prod in data.get('products', [])
        ]

        raw_category = data.get('category')
        preferred_machine = data.get('preferred_machine')

        if preferred_machine is None and isinstance(raw_category, str):
            preferred_machine = raw_category

        display_category = []
        if isinstance(raw_category, list):
            display_category = raw_category
        elif isinstance(raw_category, str):
            display_category = ['Uncategorized']
        else:
            display_category = data.get('display_category', ['Uncategorized'])

        return cls(
            name=name,
            preferred_machine=preferred_machine or 'crafting',
            category=display_category,
            time=data['time'],
            ingredients=ingredients,
            products=products,
            allow_productivity=data.get('allow_productivity', True)
        )


@dataclass
class Module:
    name: str
    speed: float
    productivity: float

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'Module':
        return cls(name=name, speed=data['speed'], productivity=data['productivity'])

@dataclass
class Machine:
    name: str
    crafting_speed: float
    module_slots: int
    categories: List[str]
    base_productivity: float = 0.0

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'Machine':
        return cls(
            name=name,
            crafting_speed=data['crafting_speed'],
            module_slots=data['module_slots'],
            categories=data.get('categories', []),
            base_productivity=data.get('base_productivity', 0.0)
        )

@dataclass
class BeltSpeeds:
    yellow: float
    red: float
    blue: float
    green: float

    def get_speed(self, color: str) -> float:
        speeds = {
            'yellow': self.yellow,
            'red': self.red,
            'blue': self.blue,
            'green': self.green
        }
        return speeds.get(color, 0)

    @classmethod
    def from_dict(cls, data: Dict) -> 'BeltSpeeds':
        return cls(
            yellow=data['yellow'],
            red=data['red'],
            blue=data['blue'],
            green=data['green']
        )

@dataclass
class FactorioData:
    belt_speeds: BeltSpeeds
    modules: Dict[str, Module]
    machines: Dict[str, Machine]
    recipes: Dict[str, Recipe]

    @classmethod
    def from_dict(cls, data: Dict) -> 'FactorioData':
        belt_speeds = BeltSpeeds.from_dict(data['belt_speeds'])
        modules = {
            name: Module.from_dict(name, mod_data)
            for name, mod_data in data.get('modules', {}).items()
        }
        machines = {
            name: Machine.from_dict(name, mach_data)
            for name, mach_data in data.get('machines', {}).items()
        }
        recipes = {
            name: Recipe.from_dict(name, recipe_data)
            for name, recipe_data in data.get('recipes', {}).items()
        }
        return cls(
            belt_speeds=belt_speeds,
            modules=modules,
            machines=machines,
            recipes=recipes
        )

@dataclass
class MachinePlan:
    recipe: str
    target_rate: float
    machine_type: str
    machine_speed: float
    base_productivity: float
    time_per_craft: float
    product_amount: float
    output_per_machine: float
    machines_needed: float
    ingredients: List['IngredientPlan']
    depth: int
    error: Optional[str] = None

    @property
    def has_error(self) -> bool:
        return self.error is not None

@dataclass
class IngredientPlan:
    name: str
    rate: float
    sub_plan: Optional[MachinePlan] = None
    error: Optional[str] = None

    @property
    def has_error(self) -> bool:
        return self.error is not None
