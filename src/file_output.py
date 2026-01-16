"""
File output module for saving calculation trees to files.
Creates nicely formatted ASCII tree files in a configurable folder.
"""
from __future__ import annotations
import os
import logging
from datetime import datetime
from models import MachinePlan
from utils import format_name
import settings

logger = logging.getLogger('FactorioCalculator')


class FileOutput:
    """Handles creating and writing calculation trees to files."""

    @classmethod
    def ensure_output_folder(cls) -> str:
        """Ensure the output folder exists, creating it if necessary.
        
        Returns:
            The absolute path to the output folder.
        """
        output_path = os.path.join(str(settings.ROOT_DIR), settings.OUTPUT_FOLDER_NAME)
        os.makedirs(output_path, exist_ok=True)
        return output_path

    @classmethod
    def generate_filename(cls, recipe_name: str, belt_color: str, verbose: bool = True) -> str:
        """Generate a timestamped filename for a calculation output file.
        
        Args:
            recipe_name: The recipe name to include in filename.
            belt_color: The belt color to include in filename.
            verbose: Whether verbose or compact mode was used.
            
        Returns:
            A formatted filename string: {recipe}_{belt}_belt_{mode}_{timestamp}.txt
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = recipe_name.replace(' ', '_').replace('/', '_')
        mode = "verbose" if verbose else "compact"
        return f"{safe_name}_{belt_color}_belt_{mode}_{timestamp}.txt"

    @classmethod
    def save_calculation(cls, plan: MachinePlan, belt_color: str, belt_speed: float, verbose: bool = True) -> str:
        """Save a calculation plan to a formatted text file.
        
        Writes the production plan with all machines, rates, and ingredients to a
        nicely formatted ASCII tree file in the output folder.
        
        Args:
            plan: The MachinePlan to save.
            belt_color: The belt color used in calculation.
            belt_speed: The belt speed in items/second.
            verbose: Whether to use detailed verbose output format.
            
        Returns:
            The absolute filepath where the calculation was saved.
            
        Logs:
            Info: File save location and completion status.
        """
        output_folder = cls.ensure_output_folder()
        filename = cls.generate_filename(plan.recipe, belt_color, verbose)
        filepath = os.path.join(output_folder, filename)

        logger.info(f"Saving calculation to: {filepath}")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("═" * 80 + "\n")
            f.write(f"  FACTORIO PRODUCTION CALCULATOR\n")
            f.write("═" * 80 + "\n\n")
            
            f.write(f"Recipe:      {format_name(plan.recipe)}\n")
            f.write(f"Belt:        {format_name(belt_color)} Belt ({belt_speed} items/s)\n")
            f.write(f"Generated:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Mode:        {'Verbose' if verbose else 'Compact'}\n")
            f.write("\n" + "═" * 80 + "\n\n")

            cls._write_plan_tree(f, plan, verbose)

            f.write("\n" + "═" * 80 + "\n")
            f.write("  End of calculation\n")
            f.write("═" * 80 + "\n")

        logger.info(f"Calculation saved successfully to: {filename}")
        return filepath

    @classmethod
    def _write_plan_tree(cls, file, plan: MachinePlan, verbose: bool, prefix: str = "", is_last: bool = True) -> None:
        """Recursively write a plan tree to file in ASCII format.
        
        Formats the machine plan and all ingredient trees into a nicely indented
        ASCII tree structure with pipe characters and branch characters.
        
        Args:
            file: File object to write to.
            plan: The MachinePlan to write.
            verbose: Whether to use verbose or compact output format.
            prefix: Current indentation prefix for proper tree alignment.
            is_last: Whether this is the last item at current level (affects pipe characters).
        """
        branch = "└── " if is_last else "├── "
        pipe = "    " if is_last else "│   "

        if plan.has_error:
            file.write(f"{prefix}{branch}[ERROR] {plan.error}\n")
            return

        product_name = format_name(plan.recipe)
        file.write(f"{prefix}{branch}[Product] {product_name}\n")
        
        indent = prefix + pipe

        machine_name = format_name(plan.machine_type)
        
        if verbose:
            file.write(f"{indent}┌─ Machine Configuration\n")
            file.write(f"{indent}│  Type:         {machine_name}\n")
            file.write(f"{indent}│  Speed:        {plan.machine_speed}x\n")
            file.write(f"{indent}│  Productivity: {plan.base_productivity * 100:.0f}%\n")
            file.write(f"{indent}│\n")
            file.write(f"{indent}├─ Production Details\n")
            file.write(f"{indent}│  Target Rate:  {plan.target_rate:.2f} items/s\n")
            file.write(f"{indent}│  Per Machine:  {plan.output_per_machine:.2f} items/s\n")
            file.write(f"{indent}│  Machines:     {plan.machines_needed:.2f}\n")
        else:
            file.write(f"{indent}Machine: {machine_name} x{plan.machines_needed:.2f}\n")
            file.write(f"{indent}Target:  {plan.target_rate:.2f} items/s\n")

        if plan.ingredients:
            if verbose:
                file.write(f"{indent}│\n")
                file.write(f"{indent}└─ Required Ingredients ({len(plan.ingredients)})\n")
            else:
                file.write(f"{indent}\n")
                file.write(f"{indent}Ingredients:\n")

            for idx, ingredient in enumerate(plan.ingredients):
                is_last_ing = idx == len(plan.ingredients) - 1
                ing_branch = "   └── " if is_last_ing else "   ├── "
                ing_prefix = indent + ("       " if is_last_ing else "   │   ")

                ing_name = format_name(ingredient.name)
                
                if ingredient.sub_plan:
                    file.write(f"{indent}{ing_branch}[Crafted] {ing_name} ({ingredient.rate:.2f}/s)\n")
                    cls._write_plan_tree(file, ingredient.sub_plan, verbose, ing_prefix, is_last_ing)
                else:
                    file.write(f"{indent}{ing_branch}[Raw] {ing_name} ({ingredient.rate:.2f}/s)\n")

    @classmethod
    def save_calculation_simple(cls, plan: MachinePlan, belt_color: str, belt_speed: float) -> str:
        """Save a calculation plan using compact output format.
        
        Convenience method that saves the calculation with verbose=False.
        
        Args:
            plan: The MachinePlan to save.
            belt_color: The belt color used in calculation.
            belt_speed: The belt speed in items/second.
            
        Returns:
            The absolute filepath where the calculation was saved.
        """
        return cls.save_calculation(plan, belt_color, belt_speed, verbose=False)