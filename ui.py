"""
Simple, Clean UI Components
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.widget import Widget
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
import io
import matplotlib
matplotlib.use('module://kivy_garden.matplotlib.backend_kivy')
import matplotlib.pyplot as plt
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import yfinance as yf

class SimpleCard(BoxLayout):
    """Simple card with background"""
    
    def __init__(self, bg_color=(1, 1, 1, 0.15), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.bind(pos=self._update_bg, size=self._update_bg)
    
    def _update_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15])


class SimpleTextInput(TextInput):
    """Simple styled text input"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.9)
        self.foreground_color = (0.1, 0.1, 0.1, 1)
        self.cursor_color = (0.2, 0.4, 0.8, 1)
        self.font_size = '16sp'
        self.padding = [15, 10]
        self.multiline = False


class SimpleButton(Button):
    """Modern button with rounded corners and effects"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent
        self.color = (1, 1, 1, 1)
        self.font_size = '16sp'
        self.bold = True
        self.normal_color = (0.2, 0.4, 0.9, 1)
        self.pressed_color = (0.15, 0.3, 0.7, 1)
        self.disabled_color = (0.5, 0.5, 0.5, 0.6)
        self.current_color = self.normal_color
        
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.bind(state=self._on_state_change)
        self.bind(disabled=self._on_disabled_change)
    
    def _update_bg(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.current_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
    
    def _on_state_change(self, instance, state):
        if not self.disabled:
            if state == 'down':
                self.current_color = self.pressed_color
            else:
                self.current_color = self.normal_color
            self._update_bg()
    
    def _on_disabled_change(self, instance, disabled):
        if disabled:
            self.current_color = self.disabled_color
        else:
            self.current_color = self.normal_color
        self._update_bg()


class DetailScreen(Screen):
    """Detailed information screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main layout with padding
        self.layout = BoxLayout(orientation='vertical', padding=[10, 5])
        
        # Back button at top
        self.back_button = SimpleButton(
            text="Back",
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={'x': 0}
        )
        
        # Scrollable content
        scroll_content = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=10,
            bar_color=(0.7, 0.7, 0.7, 0.9),
            bar_inactive_color=(0.7, 0.7, 0.7, 0.2),
            scroll_type=['bars', 'content']
        )
        
        # Content layout inside scroll view
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=[5, 5]
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Chart card with fixed height
        self.chart_card = SimpleCard(
            orientation='vertical',
            size_hint=(1, None),
            height=400,  # Fixed height for chart
            padding=[10, 10]
        )
        
        # Risk metrics card with auto height
        self.metrics_card = SimpleCard(
            orientation='vertical',
            size_hint=(1, None),
            height=200,  # Initial height for metrics
            padding=[15, 15]
        )
        
        # Risk metrics label
        self.detail_label = Label(
            text="",
            size_hint=(1, 1),
            halign='center',
            valign='middle',
            markup=True,
            font_size='16sp'
        )
        self.detail_label.bind(size=self._update_label_text_size)
        
        # Add widgets to cards
        self.chart = HistoryChartGarden(size_hint=(1, 1))
        self.chart_card.add_widget(self.chart)
        self.metrics_card.add_widget(self.detail_label)
        
        # Add cards to content layout
        content_layout.add_widget(self.chart_card)
        content_layout.add_widget(self.metrics_card)
        
        # Add everything to scroll view and main layout
        scroll_content.add_widget(content_layout)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(scroll_content)
        
        self.add_widget(self.layout)

    def _update_label_text_size(self, instance, value):
        instance.text_size = (value[0], None)
        
    def show_ticker_details(self, ticker: str, detailed_text: str):
        try:
            self.chart.load_data(ticker)
            self.detail_label.text = detailed_text
        except Exception as e:
            print(f"Error showing details: {e}")
            self.detail_label.text = f"Error loading data: {str(e)}"


class MainScreen(Screen):
    """Main screen with basic risk analysis"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = StockAnalyzerLayout()
        self.add_widget(self.layout)

class StockAnalyzerLayout(BoxLayout):
    """Modified layout with screen management"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [50, 20, 50, 20]
        self.spacing = 15
        
        # Create UI elements
        Window.bind(on_resize=self.on_window_resize)
        self.create_ui()
        
        # Initially hide More Info button
        self.more_info_button.opacity = 0
        self.more_info_button.disabled = True

    def create_ui(self):
        # Logo Image - Using FloatLayout for better positioning
        from kivy.uix.floatlayout import FloatLayout
        
        self.logo_container = FloatLayout(
            size_hint=(1, None),
            height=120
        )
        
        self.logo_image = Image(
            source='Fin.png',
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.logo_container.add_widget(self.logo_image)
        
        # Title
        title = Label(
            text="Fin Alpha",
            font_size='30sp',  # Increased font size
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=40,  # Reduced height
            pos_hint={'center_x': 0.5}  # Center alignment
        )
        
        # Subtitle
        subtitle = Label(
            text="Smart investment risk analysis",
            font_size='16sp',
            color=(1, 1, 1, 0.8),
            size_hint=(1, None),
            height=25,  # Reduced height
            pos_hint={'center_x': 0.5}  # Center alignment
        )
        
        # Input card
        input_card = SimpleCard(
            orientation='vertical',
            size_hint=(1, None),
            height=110,  # Slightly reduced height
            padding=[20, 10, 20, 10],  # Reduced padding
            spacing=8,  # Reduced spacing
            pos_hint={'center_x': 0.5}  # Center alignment
        )
        
        self.ticker_input = SimpleTextInput(
            hint_text="Enter ticker (e.g. AAPL, GOOGL, TSLA)",
            size_hint=(1, None),
            height=40
        )
        
        self.analyze_button = SimpleButton(
            text="ANALYZE STOCK",
            size_hint=(1, None),
            height=50
        )
        
        input_card.add_widget(self.ticker_input)
        input_card.add_widget(self.analyze_button)
        
        # Results card
        results_card = SimpleCard(
            orientation='vertical',
            size_hint=(1, 1),
            padding=[20, 20, 20, 20]
        )

        # Results scroll view
        self.results_scroll = ScrollView(
            size_hint=(1, 1),
            bar_width=8,
            do_scroll_x=False,
            scroll_y=1  # Start at top
        )

        # Basic result display
        self.result_label = Label(
            text="",
            size_hint=(1, None),
            size_hint_y=None,
            halign="center",
            valign="top",
            padding=[10, 10],
            text_size=(None, None)  # Allow wrapping
        )
        self.result_label.bind(texture_size=lambda *x: setattr(self.result_label, 'height', self.result_label.texture_size[1] + 20))  # + padding

        self.results_scroll.add_widget(self.result_label)

        # More Info button
        self.more_info_button = SimpleButton(
            text="More Information",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5},
            opacity=0,  # Start hidden
            disabled=True  # Start disabled
        )
        self.more_info_button.bind(on_press=self.show_details)
        
        results_card.add_widget(self.results_scroll)
        results_card.add_widget(self.more_info_button)
        
        # Add everything
        self.add_widget(self.logo_container)
        self.add_widget(title)
        self.add_widget(subtitle)
        self.add_widget(input_card)
        self.add_widget(results_card)
        
        # Initial scaling of the logo
        self.scale_logo()
    
    def on_window_resize(self, instance, width, height):
        """Handle window resize events to scale the logo appropriately"""
        self.scale_logo()
        
    def scale_logo(self):
        """Scale the logo based on window size"""
        window_width = Window.width
        
        # Scale logo based on window width
        if window_width <= 400:  # Minimal screen
            logo_size = 80
            self.logo_container.height = 80
        elif window_width >= 1200:  # Full screen
            logo_size = 150
            self.logo_container.height = 150
        else:  # Proportional scaling for sizes in between
            scale_factor = (window_width - 400) / 800  # 0 to 1 for width 400 to 1200
            logo_size = 80 + (70 * scale_factor)  # Scale from 80 to 150
            self.logo_container.height = logo_size
            
        self.logo_image.size = (logo_size, logo_size)

    def set_result_text(self, text, style="info"):
        """Modified to show simplified results and handle More Info button"""
        self.detailed_results = text  # Store full results
        
        # Show/hide More Info button based on style
        show_more_info = style not in ["error", "warning", "info"]
        self.more_info_button.opacity = 1 if show_more_info else 0
        self.more_info_button.disabled = not show_more_info
        
        # Simplified result display
        if "Risk Level: HIGH" in text:
            simple_text = "Risk Level: HIGH"
            self.result_label.color = (1, 0.1, 0.1, 1)
        elif "Risk Level: MEDIUM" in text:
            simple_text = "Risk Level: MEDIUM"
            self.result_label.color = (1, 0.8, 0.2, 1)
        elif "Risk Level: LOW" in text:
            simple_text = "Risk Level: LOW"
            self.result_label.color = (0.1, 1, 0.1, 1)
        else:
            simple_text = text
            self.result_label.color = (1, 1, 1, 1)
        
        self.result_label.text = simple_text

    def set_loading_state(self, is_loading: bool = True):
        if is_loading:
            self.analyze_button.text = "ANALYZING..."
            self.analyze_button.disabled = True
            self.set_result_text("Analyzing stock data...\n\nFetching market data and calculating risk metrics.")
        else:
            self.analyze_button.text = "ANALYZE STOCK"
            self.analyze_button.disabled = False
    
    def bind_analyze_button(self, callback):
        """Bind the analyze button to a callback function"""
        self.analyze_button.bind(on_press=callback)
    
    def get_ticker_input(self) -> str:
        return self.ticker_input.text.strip().upper()
    
    def bind_analyze_button(self, callback):
        self.analyze_button.bind(on_press=callback)

    def show_details(self, instance):
        """Show detailed analysis screen"""
        # Get reference to screen manager
        app = App.get_running_app()
        screen_manager = app.screen_manager
        
        # Set detailed text, load chart, and switch screens
        detail_screen = screen_manager.get_screen('detail')
        ticker = self.get_ticker_input()
        detail_screen.show_ticker_details(ticker, self.detailed_results)
        screen_manager.current = 'detail'

class HistoryChartGarden(BoxLayout):
    """Matplotlib chart with improved visuals and performance"""

    def __init__(self, period: str = "1y", line_color=(0.2, 0.8, 1.0, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.period = period
        self.line_color = line_color
        self.canvas_widget = None
        self.chart_container = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.add_widget(self.chart_container)

    def load_data(self, ticker: str):
        try:
            import yfinance as yf
            import matplotlib.pyplot as plt
            import numpy as np
            from matplotlib.ticker import FuncFormatter
            from datetime import datetime
            
            # Create figure with dark theme
            plt.style.use('dark_background')
            fig = plt.figure(figsize=(10, 6), dpi=100, constrained_layout=True)
            ax = fig.add_subplot(111)
            
            # Set colors
            fig.patch.set_facecolor((0.05, 0.1, 0.2, 1))
            ax.set_facecolor((0.05, 0.1, 0.2, 1))

            # Get stock data and ensure it's properly formatted
            stock = yf.Ticker(ticker)
            hist = stock.history(period=self.period)
            
            if hist.empty:
                raise ValueError("No data available for this ticker")
                
            # Extract close prices and ensure 1D array
            prices = hist['Close'].values.flatten()
            dates = np.arange(len(prices))  # Use simple indices for x-axis
            
            # Create the line plot
            ax.plot(dates, prices, color=self.line_color[:3], linewidth=2, label='Price')
            
            # Add fill
            ax.fill_between(dates, prices, np.min(prices), alpha=0.1, color=self.line_color[:3])
            
            # Format y-axis with dollar signs
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.2f}'))
            
            # Add grid
            ax.grid(True, alpha=0.2, linestyle='--', color='white')
            
            # Add price markers
            current_price = prices[-1]
            high_price = np.max(prices)
            low_price = np.min(prices)
            
            # Annotate current price
            ax.annotate(f'${current_price:,.2f}',
                       xy=(dates[-1], current_price),
                       xytext=(10, 0),
                       textcoords='offset points',
                       color='white',
                       fontsize=10,
                       bbox=dict(
                           facecolor=(0.1, 0.2, 0.5, 0.8),
                           edgecolor='none',
                           pad=3
                       ))
            
            # Add high/low annotations
            high_idx = np.argmax(prices)
            low_idx = np.argmin(prices)
            
            ax.annotate(f'High: ${high_price:,.2f}',
                       xy=(dates[high_idx], high_price),
                       xytext=(0, 15),
                       textcoords='offset points',
                       ha='center',
                       color='lightgreen',
                       fontsize=9)
                       
            ax.annotate(f'Low: ${low_price:,.2f}',
                       xy=(dates[low_idx], low_price),
                       xytext=(0, -15),
                       textcoords='offset points',
                       ha='center',
                       color='pink',
                       fontsize=9)
            
            # Clean up the plot
            ax.set_title(f'{ticker} - 1 Year Price History', color='white', pad=10)
            
            # Remove spines
            for spine in ax.spines.values():
                spine.set_visible(False)
                
            # Update the canvas
            if self.canvas_widget:
                self.chart_container.remove_widget(self.canvas_widget)
            
            from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
            self.canvas_widget = FigureCanvasKivyAgg(fig)
            self.chart_container.add_widget(self.canvas_widget)

        except Exception as e:
            print(f"Error creating chart: {e}")
            raise e

def create_main_ui():
    """Create the main screen manager with all screens"""
    sm = ScreenManager(transition=SlideTransition())
    
    # Create screens
    main_screen = MainScreen(name='main')
    detail_screen = DetailScreen(name='detail')
    
    # Add screens to manager
    sm.add_widget(main_screen)
    sm.add_widget(detail_screen)
    
    # Set up back button binding
    detail_screen.back_button.bind(
        on_press=lambda x: setattr(sm, 'current', 'main')
    )
    
    return sm
