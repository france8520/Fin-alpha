"""
Main Application File
Orchestrates the Stock Risk Analyzer app using modular components
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
        # Set window background color
        Window.clearcolor = (0.05, 0.15, 0.35, 1)
        
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
        """Handle analyze button press"""
        # Get ticker from input
        ticker = self.ui_layout.get_ticker_input()
        
        # Validate input
        if not ticker:
            self.ui_layout.set_result_text(
                "Please enter a ticker symbol", 
                "warning"
            )
            return
        
        # Set loading state
        self.ui_layout.set_loading_state(True)
        
        # Schedule the analysis to run after UI update
        Clock.schedule_once(lambda dt: self._perform_analysis(ticker), 0.1)
    
    def _perform_analysis(self, ticker: str):
        """Perform the actual stock analysis"""
        try:
            # Analyze the stock
            metrics = self.risk_analyzer.analyze_stock(ticker)
            
            if metrics:
                # Format and display results
                result_text = self.risk_analyzer.format_results(metrics)
                self.ui_layout.set_result_text(result_text, "success")
            else:
                self.ui_layout.set_result_text(
                    f"Unable to analyze {ticker}. Please try again.",
                    "error"
                )
                
        except Exception as e:
            # Handle analysis errors
            error_message = f"ERROR ANALYZING {ticker}\n\n{str(e)}\n\nPlease check the ticker symbol and try again."
            self.ui_layout.set_result_text(error_message, "error")
        
        finally:
            # Always reset loading state
            self.ui_layout.set_loading_state(False)
    
    def on_stop(self):
        """Clean up when app is closing"""
        # Stop any background animations to free resources
        for child in self.main_layout.children:
            if hasattr(child, 'stop_animation'):
                child.stop_animation()
    
    def on_pause(self):
        """Handle app pause (mobile)"""
        return True
    
    def on_resume(self):
        """Handle app resume (mobile)"""
        # Restart animations when resuming
        for child in self.main_layout.children:
            if hasattr(child, 'start_animation'):
                child.start_animation()


def main():
    """Main entry point for the application"""
    try:
        app = StockRiskApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()