"""
Main Application File - Fixed Version
Orchestrates the Stock Risk Analyzer app using modular components with improved error handling
"""
import sys
import subprocess
import pkg_resources

# Auto-install required packages
def install_missing_packages():
    required = {'kivy', 'yfinance', 'numpy', 'setuptools'}
    try:
        import pkg_resources
    except ImportError:
        print("Installing setuptools for pkg_resources...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'setuptools'])
        import pkg_resources
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

install_missing_packages()

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config

# Set minimum window size
Config.set('graphics', 'minimum_width', '400')
Config.set('graphics', 'minimum_height', '600')

# Import our custom modules
from risk import StockRiskAnalyzer
from ui import StockAnalyzerLayout, create_main_ui  # Add create_main_ui to imports
from background import create_animated_background


class StockRiskApp(App):
    """Main application class that coordinates all modules"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize the risk analyzer
        self.risk_analyzer = StockRiskAnalyzer()
        
        # UI components (will be set in build method)
        self.main_layout = None
        self.screen_manager = None
    
    def build(self):
        """Build and return the main application widget"""
        # Set window properties
        Window.clearcolor = (0.02, 0.08, 0.25, 1)
        
        self.title = "Fin-Alpha"
        
        # Create animated background
        self.main_layout = create_animated_background()
        
        # Create screen manager with all screens
        self.screen_manager = create_main_ui()
        
        # Get reference to main screen's layout for button binding
        main_screen = self.screen_manager.get_screen('main')
        main_screen.layout.bind_analyze_button(self.on_analyze_button_pressed)
        
        # Add screen manager to main layout
        self.main_layout.add_widget(self.screen_manager)
        
        return self.main_layout
    
    def on_analyze_button_pressed(self, instance):
        """Handle analyze button press with validation"""
        main_screen = self.screen_manager.get_screen('main')
        ticker = main_screen.layout.get_ticker_input()
        
        # Validation
        if not ticker:
            main_screen.layout.set_result_text(
                "Please enter a ticker symbol\n\nExample: AAPL, GOOGL, TSLA",
                "warning"
            )
            return
        
        if len(ticker) < 1 or len(ticker) > 10:
            main_screen.layout.set_result_text(f"Invalid ticker: {ticker}\n\nShould be 1-10 characters.", "warning")
            return
        
        # Start analysis
        main_screen.layout.set_loading_state(True)
        Clock.schedule_once(lambda dt: self._perform_analysis(ticker), 0.1)
    
    def _perform_analysis(self, ticker: str):
        """Perform stock analysis with error handling"""
        try:
            main_screen = self.screen_manager.get_screen('main')
            main_screen.layout.set_result_text(f"Fetching data for {ticker}...\n\nPlease wait.", "info")
            
            # Analyze the stock
            metrics = self.risk_analyzer.analyze_stock(ticker)
            
            if metrics:
                result_text, risk_style = self.risk_analyzer.format_results(metrics)
                main_screen.layout.set_result_text(result_text, risk_style)
            else:
                main_screen.layout.set_result_text(
                    f"Unable to analyze {ticker}\n\nTicker may not exist. Try a different symbol.",
                    "error"
                )
                
        except ValueError as ve:
            error_msg = f"ERROR: {ticker}\n\n{str(ve)}\n\nTry: AAPL, GOOGL, MSFT"
            main_screen.layout.set_result_text(error_msg, "error")
            
        except Exception as e:
            error_msg = f"ERROR: {ticker}\n\n{str(e)}\n\nCheck internet connection and try again."
            main_screen.layout.set_result_text(error_msg, "error")
        
        finally:
            main_screen.layout.set_loading_state(False)
    
    def on_start(self):
        """Called when the app starts"""
        welcome_text = """Ready to analyze stocks!

How it works:
• Enter any stock ticker (AAPL, GOOGL, TSLA, etc.)
• Tap ANALYZE STOCK button
• Get comprehensive risk analysis

Features:
• Real-time market data
• Advanced risk metrics
• 1-year historical analysis
• Easy-to-read results

Start by entering a ticker symbol above!"""
        
        # Get reference to main screen's layout
        main_screen = self.screen_manager.get_screen('main')
        main_screen.layout.set_result_text(welcome_text, "info")
    
    def on_stop(self):
        """Clean up when app is closing"""
        try:
            # Stop any background animations to free resources
            if self.main_layout:
                for child in self.main_layout.children:
                    if hasattr(child, 'stop_animation'):
                        child.stop_animation()
        except Exception as e:
            print(f"Error during app cleanup: {e}")
    
    def on_pause(self):
        """Handle app pause (mobile)"""
        return True
    
    def on_resume(self):
        """Handle app resume (mobile)"""
        try:
            # Restart animations when resuming
            if self.main_layout:
                for child in self.main_layout.children:
                    if hasattr(child, 'start_animation'):
                        child.start_animation()
        except Exception as e:
            print(f"Error during app resume: {e}")


def main():
    """Main entry point for the application"""
    try:
        app = StockRiskApp()
        app.run()
    except KeyboardInterrupt:
        print("\n Application terminated by user")
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages: pip install kivy yfinance numpy")
    except Exception as e:
        print(f"Application error: {e}")
        print("Please check your Python environment and try again")


if __name__ == "__main__":
    main()