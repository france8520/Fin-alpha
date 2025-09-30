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
        self.layout = BoxLayout(orientation='vertical', padding=[20, 20])
        
        # Back button
        self.back_button = SimpleButton(
            text="Back",
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={'x': 0}
        )
        
        # Chart card - Increased height
        chart_card = SimpleCard(
            orientation='vertical',
            size_hint=(1, None),
            height=400,  # Increased from 260
            padding=[15, 12, 15, 12]
        )
        chart_title = Label(
            text="1Y Price History",
            size_hint=(1, None),
            height=24,
            color=(1, 1, 1, 0.9),
            halign="left",
            valign="middle",
            text_size=(None, None)
        )
        self.chart = HistoryChartGarden(
            size_hint=(1, 1),
            line_color=(0.2, 0.8, 1.0, 1)
        )
        chart_card.add_widget(chart_title)
        chart_card.add_widget(self.chart)
        # Ensure the chart expands inside the card
        self.chart.size_hint = (1, 1)

        # Detailed results
        self.detail_scroll = ScrollView(
            size_hint=(1, 1),
            bar_width=12,
            do_scroll_x=False
        )
        self.detail_label = Label(
            text="",
            size_hint_y=None,
            halign="left",
            valign="top",
            markup=True,
            padding=(10, 10),
            text_size=(None, None)
        )
        self.detail_label.bind(texture_size=lambda *x: setattr(self.detail_label, 'height', self.detail_label.texture_size[1]))
        # Make label wrap to ScrollView width
        self.detail_label.bind(width=lambda instance, w: setattr(instance, 'text_size', (w - 20, None)))
        
        self.detail_scroll.add_widget(self.detail_label)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(chart_card)
        self.layout.add_widget(self.detail_scroll)
        self.add_widget(self.layout)

    def show_ticker_details(self, ticker: str, detailed_text: str):
        """Set detailed text and load chart for a ticker"""
        self.detail_label.text = detailed_text
        try:
            # Surface loading state visibly
            if hasattr(self.chart, 'status'):
                self.chart.status.text = f"Loading {ticker}..."
            self.chart.load_data(ticker)
        except Exception as e:
            # Fail silently for chart; keep details visible
            if hasattr(self.chart, 'status'):
                self.chart.status.text = "Chart failed to load"
            print(f"Chart load error (prep): {e}")

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
        # Increase the size of chart container
        self.chart_container = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.add_widget(self.chart_container)
        self.status = Label(text="", color=(1, 1, 1, 0.7), font_size='12sp', 
                          size_hint=(1, None), height=20)
        self.add_widget(self.status)

    def load_data(self, ticker: str):
        self.status.text = "Loading..."
        try:
            import yfinance as yf
            import numpy as np
            import matplotlib.pyplot as plt
            from matplotlib.ticker import FuncFormatter, MultipleLocator

            # Fetch data
            data = yf.download(ticker, period=self.period, interval='1d', progress=False)
            if data.empty:
                raise ValueError("No data available")

            closes = data['Close'].dropna()
            values = np.asarray(closes, dtype=float).reshape(-1)
            x = np.arange(len(values))

            # Create larger figure
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
            
            # Set background colors
            fig.patch.set_facecolor((0.05, 0.10, 0.25, 0.95))
            ax.set_facecolor((0.05, 0.10, 0.25, 0.95))

            # Add prominent grid
            ax.grid(True, which='both', axis='both', alpha=0.2, color='white')
            ax.set_axisbelow(True)

            # Plot main line with enhanced visibility
            line = ax.plot(x, values, color=self.line_color[:3], 
                         linewidth=2.5, zorder=5)[0]

            # Add gradient fill
            ax.fill_between(x, values, values.min(), 
                          color=self.line_color[:3], 
                          alpha=0.2)

            # Format prices with dollar signs and commas
            def price_formatter(x, p):
                return f'${x:,.2f}'
            ax.yaxis.set_major_formatter(FuncFormatter(price_formatter))

            # Add more y-axis ticks
            y_range = values.max() - values.min()
            ax.yaxis.set_major_locator(MultipleLocator(y_range/8))

            # Enhance tick labels
            ax.tick_params(axis='both', colors='white', labelsize=10)

            # Add price labels at key points
            start_price = values[0]
            end_price = values[-1]
            max_price = values.max()
            min_price = values.min()

            # Current price point and label
            ax.scatter([x[-1]], [end_price], color='white', s=100, zorder=6)
            ax.annotate(f'${end_price:,.2f}',
                       xy=(x[-1], end_price),
                       xytext=(10, 10),
                       textcoords='offset points',
                       color='white',
                       fontsize=12,
                       fontweight='bold',
                       bbox=dict(
                           boxstyle='round,pad=0.5',
                           fc=(0.1, 0.2, 0.5, 0.9),
                           ec='none'
                       ))

            # Add min/max labels
            ax.annotate(f'High: ${max_price:,.2f}',
                       xy=(x[np.argmax(values)], max_price),
                       xytext=(0, 15),
                       textcoords='offset points',
                       color='lightgreen',
                       fontsize=10,
                       ha='center')

            ax.annotate(f'Low: ${min_price:,.2f}',
                       xy=(x[np.argmin(values)], min_price),
                       xytext=(0, -15),
                       textcoords='offset points',
                       color='pink',
                       fontsize=10,
                       ha='center')

            # Remove spines
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Add title
            ax.set_title(f'{ticker} - 1 Year Price History',
                        color='white',
                        fontsize=14,
                        pad=20)

            plt.tight_layout(pad=2.0)

            # Update canvas
            if self.canvas_widget and self.canvas_widget in self.chart_container.children:
                self.chart_container.remove_widget(self.canvas_widget)
            
            from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
            self.canvas_widget = FigureCanvasKivyAgg(fig)
            self.chart_container.add_widget(self.canvas_widget)
            self.status.text = ""

        except Exception as e:
            print(f"Chart error: {e}")
            self.status.text = "Unable to load chart data"

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
