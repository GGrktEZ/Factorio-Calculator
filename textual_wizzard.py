"""
Textual-based wizard for interactive recipe selection and calculation.
Provides a tree-based recipe browser with configuration options.
"""
from __future__ import annotations
import logging
from typing import Dict
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Button, Tree, Select, Static, Header, Footer, Checkbox
from textual.widgets.tree import TreeNode

from loader import DataLoader
from calculator import RecipeCalculator
from file_output import FileOutput
from models import FactorioData
from utils import format_name
import settings


logger = logging.getLogger('FactorioCalculator')


class RecipeTree(Tree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recipe_nodes: Dict[str, TreeNode] = {}


class TextualWizard(App):
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #main-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    #title {
        width: 100%;
        height: 3;
        content-align: center middle;
        text-style: bold;
        background: $primary;
        color: $text;
        margin-bottom: 1;
    }
    
    #content {
        width: 100%;
        height: auto;
        layout: horizontal;
    }
    
    #tree-container {
        width: 2fr;
        height: 100%;
        border: solid $primary;
        padding: 1;
    }
    
    #config-container {
        width: 1fr;
        height: auto;
        border: solid $primary;
        padding: 1;
        margin-left: 1;
    }
    
    .config-label {
        margin-top: 1;
        margin-bottom: 1;
        text-style: bold;
    }
    
    Select {
        margin-bottom: 1;
    }
    
    Checkbox {
        margin-bottom: 1;
    }
    
    Button {
        width: 100%;
        margin-top: 1;
    }
    
    #status {
        width: 100%;
        height: 3;
        background: $surface-darken-1;
        content-align: center middle;
        margin-top: 1;
    }
    
    #error-message {
        width: 100%;
        height: auto;
        background: red;
        color: white;
        content-align: center middle;
        text-style: bold;
        padding: 1;
        margin-bottom: 1;
        display: none;
    }
    
    #error-message.visible {
        display: block;
    }
    
    RecipeTree {
        height: 100%;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "calculate", "Calculate"),
    ]
    
    def __init__(self):
        super().__init__()
        self.game_data: FactorioData | None = None
        self.selected_recipe: str | None = None
        self.selected_belt: str = settings.DEFAULT_BELT
        self.verbose: bool = settings.DEFAULT_VERBOSE
        logger.debug("TextualWizard initialized")
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(id="main-container"):
            yield Static("Factorio Production Calculator", id="title")
            yield Static("", id="error-message")
            
            with Horizontal(id="content"):
                # Left side: Recipe tree
                with Vertical(id="tree-container"):
                    yield Static("Select Recipe:", classes="config-label")
                    yield RecipeTree("Recipes", id="recipe-tree")
                
                with Vertical(id="config-container"):
                    yield Static("Configuration", classes="config-label")
                    
                    yield Static("Belt Color:", classes="config-label")
                    yield Select(
                        [
                            ("Yellow Belt (15/s)", "yellow"),
                            ("Red Belt (30/s)", "red"),
                            ("Blue Belt (45/s)", "blue"),
                            ("Green Belt (60/s)", "green"),
                        ],
                        value=self.selected_belt,
                        id="belt-select"
                    )
                    
                    yield Checkbox("Verbose Output", id="verbose-checkbox", value=self.verbose)
                    
                    yield Button("Calculate", variant="primary", id="calculate-btn")
            
            yield Static("Select a recipe and click Calculate", id="status")
        
        yield Footer()
    
    def on_mount(self) -> None:
        logger.info("Loading wizard interface")
        
        try:
            current_dir = DataLoader.get_current_directory()
            loader = DataLoader(current_dir)
            self.game_data = loader.load_base_data()
            
            self._populate_recipe_tree()
            
            self.query_one("#status", Static).update(
                f"Loaded {len(self.game_data.recipes)} recipes. Select one to calculate."
            )
            logger.info("Wizard interface loaded successfully")
            
        except Exception as e:
            logger.exception(f"Error loading wizard: {e}")
            self.query_one("#status", Static).update(f"Error: {e}")
    
    def _populate_recipe_tree(self) -> None:
        tree = self.query_one("#recipe-tree", RecipeTree)
        tree.show_root = False
        
        category_nodes: Dict[str, TreeNode] = {}
        
        sorted_recipes = sorted(self.game_data.recipes.items(), key=lambda x: x[0])
        
        for recipe_name, recipe in sorted_recipes:
            categories = recipe.category if recipe.category else ["Uncategorized"]
            
            # Build nested category tree
            current_path = []
            current_parent = tree.root

            for category in categories:
                current_path.append(category)
                path_key = " > ".join(current_path)

                if path_key not in category_nodes:
                    category_node = current_parent.add(
                        category,
                        expand=True
                    )
                    category_nodes[path_key] = category_node
                    current_parent = category_node
                else:
                    current_parent = category_nodes[path_key]

            recipe_display = recipe_name.replace('_', ' ').title()
            recipe_node = current_parent.add_leaf(recipe_display)
            tree.recipe_nodes[recipe_node.id] = recipe_name
        
        logger.debug(f"Populated tree with {len(sorted_recipes)} recipes")
    
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        tree = self.query_one("#recipe-tree", RecipeTree)

        if event.node.id in tree.recipe_nodes:
            self.selected_recipe = tree.recipe_nodes[event.node.id]
            recipe_display = self.selected_recipe.replace('_', ' ').title()
            self.query_one("#status", Static).update(
                f"Selected: {recipe_display}. Click Calculate to compute production plan."
            )
            logger.debug(f"Recipe selected: {self.selected_recipe}")
    
    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "belt-select":
            self.selected_belt = event.value
            logger.debug(f"Belt color changed to: {self.selected_belt}")
    
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if event.checkbox.id == "verbose-checkbox":
            self.verbose = event.value
            logger.debug(f"Verbose output set to: {self.verbose}")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "calculate-btn":
            self.action_calculate()
    
    def action_calculate(self) -> None:
        if not self.selected_recipe:
            error_widget = self.query_one("#error-message", Static)
            error_widget.update("⚠ ERROR: Please select a recipe first!")
            error_widget.add_class("visible")
            logger.warning("Calculate attempted without recipe selection")
            return
        
        # Clear any previous errors
        error_widget = self.query_one("#error-message", Static)
        error_widget.remove_class("visible")
        
        logger.info(f"Starting calculation for {self.selected_recipe}")
        self.query_one("#status", Static).update("Calculating...")

        try:
            belt_speed = self.game_data.belt_speeds.get_speed(self.selected_belt)

            if belt_speed is None:
                error_msg = f"Belt color '{self.selected_belt}' not found!"
                logger.warning(error_msg)
                error_widget.update(f"⚠ ERROR: {error_msg}")
                error_widget.add_class("visible")
                return

            calculator = RecipeCalculator(self.game_data)
            plan = calculator.calculate_machine_plan(self.selected_recipe, belt_speed)

            if plan.has_error:
                logger.warning(f"Calculation aborted: {plan.error}")
                error_widget.update(f"⚠ ERROR: {plan.error}")
                error_widget.add_class("visible")
                return

            output_path = FileOutput.save_calculation(
                plan, 
                self.selected_belt, 
                belt_speed,
                self.verbose
            )

            self.exit()

            print()
            print("═" * 80)
            print(f"  Calculation Complete!")
            print("═" * 80)
            print(f"  Recipe:  {format_name(self.selected_recipe)}")
            print(f"  Belt:    {format_name(self.selected_belt)} ({belt_speed} items/s)")
            print(f"  Mode:    {'Verbose' if self.verbose else 'Compact'}")
            print()
            print(f"  📄 Results saved to:")
            print(f"     {output_path}")
            print("═" * 80)
            print()
            
            logger.info("Calculation completed and saved to file")
            
        except Exception as e:
            logger.exception(f"Calculation error: {e}")
            error_widget.update(f"⚠ ERROR: {e}")
            error_widget.add_class("visible")
