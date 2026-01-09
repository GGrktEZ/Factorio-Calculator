"""
Factorio Calculator - Main Entry Point

This module coordinates the calculation of production plans for Factorio items.
It loads configuration, calculates machine requirements, and displays results.
Can run in CLI mode (legacy) or GUI wizard mode (default).
"""
import sys
from logger_config import LoggerSetup
from loader import DataLoader
from calculator import RecipeCalculator
from printer import PlanPrinter
from file_output import FileOutput
import settings


def run_cli_mode():
    """Run calculator in CLI mode using Config.json."""
    current_dir = DataLoader.get_current_directory()
    console_logging_enabled = settings.LOG_CONSOLE

    try:
        loader_temp = DataLoader(current_dir)
        config = loader_temp.load_config()
        console_logging_enabled = str(config.get('consoleLogging', str(settings.LOG_CONSOLE))).lower() == 'true'
    except Exception:
        pass

    logger = LoggerSetup.initialize(enable_console=console_logging_enabled)

    try:
        logger.info("=" * 60)
        logger.info("Factorio Calculator starting (CLI mode)")
        logger.info("=" * 60)

        loader = DataLoader(current_dir)
        game_data = loader.load_base_data()
        config = loader.load_config()

        belt_color = config.get('belt_color', 'green')
        product = config.get('product', 'transport_belt')
        verbose = str(config.get('verbose', 'true')).lower() == 'true'

        logger.info(f"Configuration: product={product}, belt_color={belt_color}, verbose={verbose}")

        belt_speed = game_data.belt_speeds.get_speed(belt_color)
        logger.debug(f"Belt speed for {belt_color}: {belt_speed} items/s")
        
        logger.info(f"Starting calculation for {product}")
        calculator = RecipeCalculator(game_data)
        plan = calculator.calculate_machine_plan(product, belt_speed)

        PlanPrinter.print_header(belt_color, belt_speed)
        PlanPrinter.print_plan(plan, verbose)

        output_path = FileOutput.save_calculation(plan, belt_color, belt_speed, verbose)

        logger.info("Calculation completed successfully")
        logger.info("=" * 60)

        print(f"\nCalculation saved to: {output_path}")
        if LoggerSetup.get_log_file():
                print(f"Log file saved to: {LoggerSetup.get_log_file()}")

    except FileNotFoundError as e:
        logger.exception(f"File not found: {e}")
        print(f"Error: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"Error: {e}")
        raise


def run_wizard_mode():
    """Run calculator in interactive wizard mode."""
    current_dir = DataLoader.get_current_directory()
    
    try:
        loader_temp = DataLoader(current_dir)
        config = loader_temp.load_config()
        console_logging_enabled = str(config.get('consoleLogging', str(settings.LOG_CONSOLE))).lower() == 'true'
    except Exception:
        console_logging_enabled = settings.LOG_CONSOLE
    
    logger = LoggerSetup.initialize(enable_console=console_logging_enabled)
    logger.info("=" * 60)
    logger.info("Factorio Calculator starting (Wizard mode)")
    logger.info("=" * 60)
    
    try:
        from textual_wizzard import TextualWizard
        app = TextualWizard()
        app.run()
        
        logger.info("Wizard mode completed")
        logger.info("=" * 60)
        
        if LoggerSetup.get_log_file():
            print(f"\nLog file saved to: {LoggerSetup.get_log_file()}")
            
    except Exception as e:
        logger.exception(f"Error running wizard: {e}")
        print(f"Error: {e}")
        raise


def main():
    """Main entry point for the Factorio Calculator."""
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        run_cli_mode()
    else:
        run_wizard_mode()


if __name__ == "__main__":
    main()