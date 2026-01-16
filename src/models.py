"""
Data models for Factorio Calculator.
Defines the structure for recipes, machines, modules, and belts.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Ingredient:
    """Represents an ingredient in a recipe.
    
    Attributes:
        name: The item name.
        amount: Amount required per craft.
    """
    name: str
    amount: float

@dataclass
class Product:
    """Represents a product of a recipe.
    
    Attributes:
        name: The item name.
        amount: Amount produced per craft.
    """
    name: str
    amount: float

@dataclass
class Recipe:
    """Represents a Factorio recipe.
    
    Attributes:
        name: Recipe identifier.
        preferred_machine: Machine type that crafts this recipe.
        category: List of display categories for UI organization.
        time: Crafting time in seconds.
        ingredients: List of Ingredient objects required.
        products: List of Product objects produced.
        allow_productivity: Whether productivity modules affect this recipe.
    """
    name: str
    preferred_machine: str
    category: List[str]
    time: float
    ingredients: List[Ingredient]
    products: List[Product]
    allow_productivity: bool = True

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'Recipe':
        """Create a Recipe from dictionary data.
        
        Args:
            name: Recipe name/identifier.
            data: Dictionary with recipe data.
            
        Returns:
            Recipe object with parsed data.
        """
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
    """Represents a crafting module that modifies machine behavior.
    
    Attributes:
        name: Module identifier.
        speed: Speed multiplier bonus.
        productivity: Productivity bonus (as decimal, e.g., 0.1 for 10%).
    """
    name: str
    speed: float
    productivity: float

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'Module':
        """Create a Module from dictionary data.
        
        Args:
            name: Module name/identifier.
            data: Dictionary with module data.
            
        Returns:
            Module object with parsed data.
        """
        return cls(name=name, speed=data['speed'], productivity=data['productivity'])

@dataclass
class Machine:
    """Represents a Factorio crafting machine.
    
    Attributes:
        name: Machine identifier.
        crafting_speed: Speed multiplier for crafting (e.g., 1.0, 0.5).
        module_slots: Number of module slots available.
        categories: List of recipe categories this machine can craft.
        base_productivity: Base productivity bonus (as decimal).
    """
    name: str
    crafting_speed: float
    module_slots: int
    categories: List[str]
    base_productivity: float = 0.0

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'Machine':
        """Create a Machine from dictionary data.
        
        Args:
            name: Machine name/identifier.
            data: Dictionary with machine data.
            
        Returns:
            Machine object with parsed data.
        """
        return cls(
            name=name,
            crafting_speed=data['crafting_speed'],
            module_slots=data['module_slots'],
            categories=data.get('categories', []),
            base_productivity=data.get('base_productivity', 0.0)
        )

@dataclass
class BeltSpeeds:
    """Represents production rates for different belt colors.
    
    Attributes:
        yellow: Items per second on yellow belt.
        red: Items per second on red belt.
        blue: Items per second on blue belt.
        green: Items per second on green belt.
    """
    yellow: float
    red: float
    blue: float
    green: float

    def get_speed(self, color: str) -> Optional[float]:
        """Get the speed for a belt color.
        
        Args:
            color: Belt color name (yellow, red, blue, green).
            
        Returns:
            Speed in items/second, or None if color not recognized.
        """
        speeds = {
            'yellow': self.yellow,
            'red': self.red,
            'blue': self.blue,
            'green': self.green
        }
        return speeds.get(color)

    @classmethod
    def from_dict(cls, data: Dict) -> 'BeltSpeeds':
        """Create BeltSpeeds from dictionary data.
        
        Args:
            data: Dictionary with belt speeds.
            
        Returns:
            BeltSpeeds object with parsed data.
        """
        return cls(
            yellow=data['yellow'],
            red=data['red'],
            blue=data['blue'],
            green=data['green']
        )

@dataclass
class FactorioData:
    """Container for all Factorio game data.
    
    Attributes:
        belt_speeds: BeltSpeeds object with all belt speeds.
        modules: Dictionary of Module objects by name.
        machines: Dictionary of Machine objects by name.
        recipes: Dictionary of Recipe objects by name.
    """
    belt_speeds: BeltSpeeds
    modules: Dict[str, Module]
    machines: Dict[str, Machine]
    recipes: Dict[str, Recipe]

    @classmethod
    def from_dict(cls, data: Dict) -> 'FactorioData':
        """Create FactorioData from dictionary data.
        
        Args:
            data: Dictionary with all game data sections.
            
        Returns:
            FactorioData object with fully parsed data structures.
        """
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
    """Result of calculating production requirements for a recipe.
    
    Attributes:
        recipe: The recipe name.
        target_rate: Target production rate in items/second.
        machine_type: Type of machine used.
        machine_speed: Crafting speed of the machine.
        base_productivity: Base productivity bonus of the machine.
        time_per_craft: Crafting time in seconds.
        product_amount: Amount produced per craft.
        output_per_machine: Output rate per machine in items/second.
        machines_needed: Number of machines required.
        ingredients: List of IngredientPlan for required ingredients.
        depth: Recursion depth in calculation tree.
        error: Error message if calculation failed, None if successful.
    """
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
        """Check if this plan encountered an error.
        
        Returns:
            True if error is not None, False otherwise.
        """
        return self.error is not None

@dataclass
class IngredientPlan:
    """Plan for producing a required ingredient.
    
    Attributes:
        name: The ingredient name.
        rate: Required production rate in items/second.
        sub_plan: MachinePlan if ingredient is crafted, None if raw material.
        error: Error message if planning failed.
    """
    name: str
    rate: float
    sub_plan: Optional[MachinePlan] = None
    error: Optional[str] = None

    @property
    def has_error(self) -> bool:
        """Check if this ingredient plan encountered an error.
        
        Returns:
            True if error is not None, False otherwise.
        """
        return self.error is not None
