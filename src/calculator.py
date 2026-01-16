"""Calculator module for computing production plans.
Handles recipe lookups, machine selection, and production calculations.
"""
import logging
from typing import Optional
from models import FactorioData, Recipe, MachinePlan, IngredientPlan

logger = logging.getLogger('FactorioCalculator')


class RecipeCalculator:
    """Handles recipe-related calculations and machine selection."""

    def __init__(self, data: FactorioData):
        self.data = data
        logger.debug("RecipeCalculator initialized")

    def get_recipe(self, recipe_name: str) -> Optional[Recipe]:
        """Retrieve a recipe by name.
        
        Args:
            recipe_name: The name of the recipe to retrieve.
            
        Returns:
            Recipe object if found, None otherwise.
        """
        return self.data.recipes.get(recipe_name)

    def select_best_machine(self, recipe_category: str) -> str:
        """Select the best machine for a given recipe category.
        
        Selects the machine with the highest base productivity that supports
        the recipe category. Falls back to first available machine if no match found.
        
        Args:
            recipe_category: The recipe category (e.g., 'crafting', 'smelting').
            
        Returns:
            The name of the best machine for this category.
            
        Logs:
            Debug: Machine selection and fallback decisions.
        """
        logger.debug(f"Selecting best machine for category: {recipe_category}")
        machines = self.data.machines
        best_machine = None
        best_productivity = -1

        for machine_name, machine in machines.items():
            if recipe_category in machine.categories:
                if machine.base_productivity > best_productivity:
                    best_machine = machine_name
                    best_productivity = machine.base_productivity

        if best_machine is None:
            if 'assembling_machine' in machines:
                logger.debug(f"No machine found for category '{recipe_category}', "
                            "using fallback: assembling_machine")
            fallback = list(machines.keys())[0]
            logger.debug(f"No machine found for category '{recipe_category}', "
                        f"using fallback: {fallback}")
            return fallback

        logger.debug(f"Selected machine: {best_machine} (productivity: {best_productivity})")
        return best_machine

    def calculate_machine_plan(
        self,
        recipe_name: str,
        target_rate: float,
        depth: int = 0
    ) -> MachinePlan:
        """Calculate the machine plan for a recipe at a target production rate.
        
        Recursively calculates production requirements including the optimal machine,
        quantity needed, and ingredient requirements. Handles ingredient recipes
        by recursively planning their production.
        
        Args:
            recipe_name: The name of the recipe to calculate.
            target_rate: Target production rate in items/second.
            depth: Current recursion depth (internal use for logging indentation).
            
        Returns:
            MachinePlan object containing all calculation details and ingredient plans.
            
        Logs:
            Debug: Detailed calculation steps and ingredient processing.
            Warning: Missing recipes.
        """
        indent = "  " * depth
        logger.debug(f"{indent}Calculating plan for recipe: {recipe_name} "
                     f"at rate: {target_rate:.2f} items/s")

        recipe = self.get_recipe(recipe_name)

        if recipe is None:
            logger.warning(f"{indent}Recipe '{recipe_name}' not found!")
            return MachinePlan(
                recipe=recipe_name,
                target_rate=target_rate,
                machine_type="",
                machine_speed=0,
                base_productivity=0,
                time_per_craft=0,
                product_amount=0,
                output_per_machine=0,
                machines_needed=0,
                ingredients=[],
                depth=depth,
                error=f"Recipe '{recipe_name}' not found!"
            )

        category = recipe.preferred_machine
        machine_type = self.select_best_machine(category)
        machine = self.data.machines[machine_type]
        machine_speed = machine.crafting_speed
        base_productivity = machine.base_productivity
        time_per_craft = recipe.time

        main_product = recipe.products[0]
        product_amount = main_product.amount

        output_per_machine = (product_amount * machine_speed * (1 + base_productivity)) / time_per_craft

        machines_needed = target_rate / output_per_machine if output_per_machine > 0 else 0

        ingredient_plans = []
        for ingredient in recipe.ingredients:
            ing_name = ingredient.name
            ing_amount = ingredient.amount
            ing_rate = (ing_amount * target_rate) / product_amount

            sub_plan = None
            if self.get_recipe(ing_name) is not None:
                sub_plan = self.calculate_machine_plan(ing_name, ing_rate, depth + 1)

            ingredient_plans.append(IngredientPlan(name=ing_name, rate=ing_rate, sub_plan=sub_plan))

        return MachinePlan(
            recipe=recipe_name,
            target_rate=target_rate,
            machine_type=machine_type,
            machine_speed=machine_speed,
            base_productivity=base_productivity,
            time_per_craft=time_per_craft,
            product_amount=product_amount,
            output_per_machine=output_per_machine,
            machines_needed=machines_needed,
            ingredients=ingredient_plans,
            depth=depth
        )
