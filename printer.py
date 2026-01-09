"""
Output formatting module for displaying machine plans.
Handles all printing and formatting of production plans.
"""
from __future__ import annotations
import logging
from models import MachinePlan
from utils import format_name

logger = logging.getLogger('FactorioCalculator')


class PlanPrinter:
    """Handles formatting and printing of machine plans."""

    @classmethod
    def print_plan(cls, plan: MachinePlan, verbose: bool = True, prefix: str = "", is_last: bool = True) -> None:
        branch = "└─" if is_last else "├─"
        pipe = "   " if is_last else "│  "
        indent = prefix

        if plan.has_error:
            print(f"{indent}{plan.error}")
            return

        print(f"{indent}{branch} Product: {format_name(plan.recipe)}")
        indent2 = indent + pipe

        if verbose:
            cls._print_verbose_info(plan, indent2)
        else:
            cls._print_compact_info(plan, indent2)

        if plan.ingredients:
            print(f"{indent2}Ingredients:")
            cls._print_ingredients(plan.ingredients, indent2, verbose)

    @staticmethod
    def _print_verbose_info(plan: MachinePlan, indent: str) -> None:
        print(f"{indent}Machine: {format_name(plan.machine_type)} "
              f"(Speed: {plan.machine_speed}, Productivity: {plan.base_productivity*100:.0f}%)")
        print(f"{indent}Target rate: {plan.target_rate:.2f} items/s")
        print(f"{indent}Each machine produces {plan.output_per_machine:.2f} items/s")
        print(f"{indent}Machines needed: {plan.machines_needed:.2f}")

    @staticmethod
    def _print_compact_info(plan: MachinePlan, indent: str) -> None:
        print(f"{indent}Machine: {format_name(plan.machine_type)}")
        print(f"{indent}Target rate: {plan.target_rate:.2f} items/s")
        print(f"{indent}Machines needed: {plan.machines_needed:.2f}")

    @classmethod
    def _print_ingredients(cls, ingredients: list, base_indent: str, verbose: bool) -> None:
        for idx, ingredient in enumerate(ingredients):
            is_last = idx == len(ingredients) - 1
            ing_branch = "└─" if is_last else "├─"
            ing_prefix = base_indent + ("   " if is_last else "│  ")

            ing_display = f"{base_indent}{ing_branch} {format_name(ingredient.name)} ({ingredient.rate:.2f}/s)"
            print(ing_display)

            if ingredient.sub_plan:
                cls.print_plan(ingredient.sub_plan, verbose, ing_prefix, is_last)

    @classmethod
    def print_header(cls, belt_color: str, belt_speed: float) -> None:
        print(f"\n=== Machine Calculation with {format_name(belt_color)} Belt ({belt_speed} items/s) ===")