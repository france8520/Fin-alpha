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
        # Set window properties
        Window.clearcolor = (0.05, 0.15, 0.35, 1)
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
        """Handle analyze button press with improved validation"""
        # Get ticker from input
        ticker = self.ui_layout.get_ticker_input()
        
        # Enhanced validation
        if not ticker:
            self.ui_layout.set_result_text(
                "Please enter a ticker symbol\n\nExample: AAPL, GOOGL, TSLA", 
                "warning"
            )
            return
        
        # Basic ticker format validation
        if len(ticker) < 1 or len(ticker) > 10:
            self.ui_layout.set_result_text(
                f"Invalid ticker format: {ticker}\n\nTicker symbols should be 1-10 characters long.", 
                "warning"
            )
            return
        
        # Set loading state
        self.ui_layout.set_loading_state(True)
        
        # Schedule the analysis to run after UI update
        Clock.schedule_once(lambda dt: self._perform_analysis(ticker), 0.1)
    
    def _perform_analysis(self, ticker: str):
        """Perform the actual stock analysis with enhanced error handling"""
        try:
            # Show progress
            self.ui_layout.set_result_text(
                f"Fetching data for {ticker}...\n\nThis may take a few seconds.", 
                "info"
            )
            
            # Analyze the stock
            metrics = self.risk_analyzer.analyze_stock(ticker)
            
            if metrics:
                # Format and display results
                result_text = self.risk_analyzer.format_results(metrics)
                self.ui_layout.set_result_text(result_text, "success")
            else:
                self.ui_layout.set_result_text(
                    f"Unable to analyze {ticker}\n\nThe ticker may not exist or data is unavailable.\nPlease try a different symbol.",
                    "error"
                )
                
        except ValueError as ve:
            # Handle specific validation errors
            error_message = f"VALIDATION ERROR\n\nTicker: {ticker}\nIssue: {str(ve)}\n\nSuggestions:\n• Check if ticker symbol is correct\n• Try a more popular stock (e.g., AAPL, GOOGL)\n• Ensure the company is publicly traded"
            self.ui_layout.set_result_text(error_message, "error")
            
        except Exception as e:
            # Handle general analysis errors
            error_type = type(e).__name__
            error_message = f"ERROR ANALYZING {ticker}\n\nError Type: {error_type}\nDetails: {str(e)}\n\nTroubleshooting:\n• Check your internet connection\n• Verify the ticker symbol\n• Try again in a few moments"
            self.ui_layout.set_result_text(error_message, "error")
        
        finally:
            # Always reset loading state
            self.ui_layout.set_loading_state(False)
    
    def on_start(self):
        """Called when the app starts"""
        # Show welcome message
        welcome_text = """Welcome to Stock Risk Analyzer!

How to use:
1. Enter a stock ticker symbol (e.g., AAPL, GOOGL, TSLA)
2. Click "ANALYZE STOCK" 
3. View detailed risk metrics and analysis

Tips:
• Use official ticker symbols
• Most US stocks work well
• Analysis uses 1 year of historical data

Ready to analyze your first stock? Enter a ticker above!"""
        
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