"""
Main Application File - Fixed Version
Orchestrates the Stock Risk Analyzer app using modular components with improved error handling
"""

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

# Import our custom modules
from risk import StockRiskAnalyzer
from ui import StockAnalyzerLayout
from background import create_animated_background


class StockRiskApp(App):
    """Main application class that coordinates all modules"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize the risk analyzer
        self.risk_analyzer = StockRiskAnalyzer()
        
        # UI components (will be set in build method)
        self.main_layout = None
        self.ui_layout = None
        
    def build(self):
        """Build and return the main application widget"""
        # Set window properties - deep ocean night color
        Window.clearcolor = (0.02, 0.08, 0.25, 1)
        Window.minimum_width = 400
        Window.minimum_height = 600
        
        # Set title
        self.title = "Stock Risk Analyzer"
        
        # Create animated background
        self.main_layout = create_animated_background()
        
        # Create main UI layout
        self.ui_layout = StockAnalyzerLayout()
        
        # Bind the analyze button to our callback
        self.ui_layout.bind_analyze_button(self.on_analyze_button_pressed)
        
        # Add UI to main layout
        self.main_layout.add_widget(self.ui_layout)
        
        return self.main_layout
    
    def on_analyze_button_pressed(self, instance):
        """Handle analyze button press with validation"""
        ticker = self.ui_layout.get_ticker_input()
        
        # Validation
        if not ticker:
            self.ui_layout.set_result_text("Please enter a ticker symbol\n\nExample: AAPL, GOOGL, TSLA", "warning")
            return
        
        if len(ticker) < 1 or len(ticker) > 10:
            self.ui_layout.set_result_text(f"Invalid ticker: {ticker}\n\nShould be 1-10 characters.", "warning")
            return
        
        # Start analysis
        self.ui_layout.set_loading_state(True)
        Clock.schedule_once(lambda dt: self._perform_analysis(ticker), 0.1)
    
    def _perform_analysis(self, ticker: str):
        """Perform stock analysis with error handling"""
        try:
            self.ui_layout.set_result_text(f"Fetching data for {ticker}...\n\nPlease wait.", "info")
            
            # Analyze the stock
            metrics = self.risk_analyzer.analyze_stock(ticker)
            
            if metrics:
                result_text = self.risk_analyzer.format_results(metrics)
                self.ui_layout.set_result_text(result_text, "success")
            else:
                self.ui_layout.set_result_text(
                    f"Unable to analyze {ticker}\n\nTicker may not exist. Try a different symbol.",
                    "error"
                )
                
        except ValueError as ve:
            error_msg = f"ERROR: {ticker}\n\n{str(ve)}\n\nTry: AAPL, GOOGL, MSFT"
            self.ui_layout.set_result_text(error_msg, "error")
            
        except Exception as e:
            error_msg = f"ERROR: {ticker}\n\n{str(e)}\n\nCheck internet connection and try again."
            self.ui_layout.set_result_text(error_msg, "error")
        
        finally:
            self.ui_layout.set_loading_state(False)
    
    def on_start(self):
        """Called when the app starts"""
        welcome_text = """🎯 Ready to analyze stocks!

📊 How it works:
• Enter any stock ticker (AAPL, GOOGL, TSLA, etc.)
• Tap ANALYZE STOCK button
• Get comprehensive risk analysis

✨ Features:
• Real-time market data
• Advanced risk metrics
• 1-year historical analysis
• Easy-to-read results

💡 Start by entering a ticker symbol above!"""
        
        self.ui_layout.set_result_text(welcome_text, "info")
    
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