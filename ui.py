"""
UI Components Module - Fixed Version
Contains all custom UI components with improved output scaling and formatting
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.core.window import Window
from typing import Callable, Optional


class ModernTextInput(TextInput):
    """Styled text input with modern appearance"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_styling()
    
    def _setup_styling(self):
        """Apply modern styling to text input"""
        self.background_color = (1, 1, 1, 0.9)
        self.foreground_color = (0.1, 0.1, 0.1, 1)
        self.cursor_color = (0.1, 0.3, 0.7, 1)
        self.selection_color = (0.2, 0.4, 0.8, 0.3)
        self.font_size = '18sp'  # Increased font size
        self.padding = [15, 12]
        self.multiline = False


class ModernButton(Button):
    """Styled button with custom graphics and animations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_styling()
        self._setup_graphics()
    
    def _setup_styling(self):
        """Apply modern styling to button"""
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.font_size = '18sp'  # Increased font size
        self.bold = True
        self.color = (1, 1, 1, 1)
    
    def _setup_graphics(self):
        """Setup custom button graphics"""
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        """Update button graphics"""
        self.canvas.before.clear()
        with self.canvas.before:
            # Main button background
            Color(0.1, 0.4, 0.8, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
            # Shadow effect
            Color(0.05, 0.2, 0.4, 0.5)
            Rectangle(pos=(self.x + 2, self.y - 2), size=self.size)
    
    def animate_press(self):
        """Animate button press effect"""
        # Scale animation
        original_size = (self.width, self.height)
        pressed_size = (self.width * 0.95, self.height * 0.95)
        
        anim_press = Animation(size=pressed_size, duration=0.1)
        anim_release = Animation(size=original_size, duration=0.1)
        
        anim_press.bind(on_complete=lambda *args: anim_release.start(self))
        anim_press.start(self)


class ModernLabel(Label):
    """Styled label with improved typography"""
    
    def __init__(self, text_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self._setup_styling(text_color)
        self.bind(size=self._update_text_size)
    
    def _setup_styling(self, text_color):
        """Apply modern styling to label"""
        self.color = text_color
        self.font_size = '16sp'  # Increased base font size
        self.text_size = (None, None)
        self.halign = 'center'
        self.valign = 'middle'
    
    def _update_text_size(self, *args):
        """Update text size for proper wrapping"""
        if self.width > 0:
            self.text_size = (self.width * 0.9, None)


class TitleLabel(ModernLabel):
    """Large title label"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '32sp'  # Larger title
        self.bold = True


class SubtitleLabel(ModernLabel):
    """Subtitle label with muted color"""
    
    def __init__(self, **kwargs):
        super().__init__(text_color=(0.8, 0.9, 1, 0.8), **kwargs)
        self.font_size = '16sp'  # Increased subtitle size


class ScrollableResultLabel(ScrollView):
    """Scrollable container for results with proper text scaling"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.scroll_type = ['bars', 'content']
        self.bar_width = 10
        
        # Create the label inside
        self.result_label = Label(
            text="Results will appear here after analysis...",
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(0.95, 0.98, 1.0, 0.95),
            font_size='16sp',  # Good readable size
            markup=True
        )
        
        self.add_widget(self.result_label)
        self.bind(size=self._update_text_size)
    
    def _update_text_size(self, *args):
        """Update text size based on container size"""
        if self.width > 0:
            # Set text_size to container width for proper wrapping
            self.result_label.text_size = (self.width - 20, None)  # -20 for scrollbar
            # Update height based on texture size
            self.result_label.height = max(self.result_label.texture_size[1], self.height)
            self.result_label.size_hint_y = None
    
    def set_text(self, text: str, color: tuple = (0.95, 0.98, 1.0, 0.95)):
        """Set text with proper formatting"""
        self.result_label.text = text
        self.result_label.color = color
        # Force text size update
        self._update_text_size()


class ResultDisplayPanel(BoxLayout):
    """Enhanced results panel with better formatting"""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # Header for results section
        self.header_label = Label(
            text="Analysis Results",
            font_size='20sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height='40dp'
        )
        
        # Scrollable results area
        self.results_scroll = ScrollableResultLabel(
            size_hint=(1, 1)
        )
        
        self.add_widget(self.header_label)
        self.add_widget(self.results_scroll)
    
    def set_results(self, text: str, result_type: str = "info"):
        """Set results with color coding"""
        colors = {
            'success': (0.7, 1, 0.7, 1),
            'warning': (1, 0.9, 0.5, 1),
            'error': (1, 0.7, 0.7, 1),
            'info': (0.9, 0.95, 1, 1)
        }
        
        color = colors.get(result_type, colors['info'])
        
        # Format text with better spacing and structure
        formatted_text = self._format_analysis_text(text)
        self.results_scroll.set_text(formatted_text, color)
    
    def _format_analysis_text(self, text: str) -> str:
        """Format analysis text for better readability"""
        if "ANALYSIS RESULTS FOR" in text:
            # Format the analysis results
            lines = text.split('\n')
            formatted_lines = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    formatted_lines.append("")
                elif "ANALYSIS RESULTS FOR" in line:
                    # Header
                    ticker = line.split("FOR ")[-1]
                    formatted_lines.append(f"[size=24sp][b]{ticker} Analysis[/b][/size]")
                    formatted_lines.append("")
                elif "Current Price:" in line:
                    # Current price
                    price = line.split(": ")[-1]
                    formatted_lines.append(f"[size=20sp][b]Current Price: [color=90ff90]{price}[/color][/b][/size]")
                    formatted_lines.append("")
                elif "RISK METRICS:" in line:
                    formatted_lines.append(f"[size=18sp][b]Risk Metrics:[/b][/size]")
                elif line.startswith("• "):
                    # Metric line
                    metric = line[2:]  # Remove bullet
                    if ":" in metric:
                        name, value = metric.split(":", 1)
                        formatted_lines.append(f"[size=16sp]• [b]{name}:[/b] {value.strip()}[/size]")
                    else:
                        formatted_lines.append(f"[size=16sp]• {metric}[/size]")
                elif "Risk Level:" in line:
                    # Risk level with color coding
                    level = line.split(": ")[-1]
                    color = "ff9090" if level == "HIGH" else ("ffff90" if level == "MEDIUM" else "90ff90")
                    formatted_lines.append("")
                    formatted_lines.append(f"[size=20sp][b]Risk Level: [color={color}]{level}[/color][/b][/size]")
                else:
                    formatted_lines.append(f"[size=16sp]{line}[/size]")
            
            return "\n".join(formatted_lines)
        else:
            # For error messages or other text
            return f"[size=16sp]{text}[/size]"


class StockAnalyzerLayout(FloatLayout):
    """Main application layout with improved content management"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Color scheme
        self.colors = {
            'success': (0.7, 1, 0.7, 1),
            'warning': (1, 0.9, 0.5, 1),
            'error': (1, 0.7, 0.7, 1),
            'info': (0.9, 0.95, 1, 1)
        }
        
        self._setup_layout()
    
    def _setup_layout(self):
        """Setup the main content layout"""
        # Main content container
        self.content_layout = BoxLayout(
            orientation="vertical",
            padding=[30, 60, 30, 100],  # Better padding
            spacing=20,
            size_hint=(0.9, 0.8),  # Use more screen space
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        
        self.add_widget(self.content_layout)
        
        # Create sections
        self._create_header()
        self._create_input_section()
        self._create_results_section()
    
    def _create_header(self):
        """Create header section"""
        # Header container
        header_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height='100dp',
            spacing=10
        )
        
        # Main title
        self.title = TitleLabel(
            text="Stock Risk Analyzer",
            size_hint=(1, None),
            height='50dp'
        )
        
        # Subtitle
        self.subtitle = SubtitleLabel(
            text="Enter a stock ticker to analyze volatility and risk metrics",
            size_hint=(1, None),
            height='40dp'
        )
        
        header_box.add_widget(self.title)
        header_box.add_widget(self.subtitle)
        self.content_layout.add_widget(header_box)
    
    def _create_input_section(self):
        """Create input section"""
        # Input container
        input_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height='120dp',
            spacing=15
        )
        
        # Ticker input
        self.ticker_input = ModernTextInput(
            hint_text="Enter stock ticker (e.g. AAPL, TSLA, GOOGL)",
            size_hint=(1, None),
            height='50dp'
        )
        
        # Analyze button
        self.analyze_button = ModernButton(
            text="ANALYZE STOCK",
            size_hint=(1, None),
            height='55dp'
        )
        
        input_box.add_widget(self.ticker_input)
        input_box.add_widget(self.analyze_button)
        self.content_layout.add_widget(input_box)
    
    def _create_results_section(self):
        """Create results section with better display"""
        # Results take the remaining space
        self.result_panel = ResultDisplayPanel(
            size_hint=(1, 1)  # Takes remaining space
        )
        
        self.content_layout.add_widget(self.result_panel)
    
    def set_result_text(self, text: str, result_type: str = "info"):
        """Set result text with proper formatting"""
        self.result_panel.set_results(text, result_type)
    
    def set_loading_state(self, is_loading: bool = True):
        """Set loading state"""
        if is_loading:
            self.set_result_text("Analyzing stock data...\n\nPlease wait while we fetch and calculate risk metrics.", "info")
            self.analyze_button.text = "ANALYZING..."
            self.analyze_button.disabled = True
        else:
            self.analyze_button.text = "ANALYZE STOCK"
            self.analyze_button.disabled = False
    
    def get_ticker_input(self) -> str:
        """Get ticker input"""
        return self.ticker_input.text.strip().upper()
    
    def clear_ticker_input(self):
        """Clear ticker input"""
        self.ticker_input.text = ""
    
    def bind_analyze_button(self, callback: Callable):
        """Bind analyze button callback"""
        def on_button_press(instance):
            instance.animate_press()
            callback(instance)
        
        self.analyze_button.bind(on_press=on_button_press)


# Additional improvements for better mobile/desktop responsiveness
class ResponsiveLayout(BoxLayout):
    """Responsive layout that adapts to window size"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(size=self._update_layout)
        self._update_layout()
    
    def _update_layout(self, *args):
        """Update layout based on window size"""
        width, height = Window.size
        
        # Adjust font sizes and spacing based on screen size
        if width < 800:  # Mobile/small screen
            base_font_size = 14
        elif width < 1200:  # Tablet
            base_font_size = 16
        else:  # Desktop
            base_font_size = 18
        
        # You can add logic here to adjust font sizes dynamically
        # This would require updating all child widgets


# Factory functions
def create_main_ui() -> StockAnalyzerLayout:
    """Create the main UI layout"""
    return StockAnalyzerLayout()


def create_input_field(hint: str, size_hint: tuple = (1, 0.15)) -> ModernTextInput:
    """Create a styled input field"""
    return ModernTextInput(hint_text=hint, size_hint=size_hint)


def create_action_button(text: str, size_hint: tuple = (1, 0.15)) -> ModernButton:
    """Create a styled action button"""
    return ModernButton(text=text, size_hint=size_hint)