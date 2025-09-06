"""
UI Components Module
Contains all custom UI components and layout management
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
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
        self.font_size = '16sp'
        self.padding = [15, 10]
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
        self.font_size = '16sp'
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
        self.font_size = '14sp'
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
        self.font_size = '28sp'
        self.bold = True


class SubtitleLabel(ModernLabel):
    """Subtitle label with muted color"""
    
    def __init__(self, **kwargs):
        super().__init__(text_color=(0.8, 0.9, 1, 0.8), **kwargs)
        self.font_size = '14sp'


class ResultLabel(ModernLabel):
    """Result display label with better formatting"""
    
    def __init__(self, **kwargs):
        super().__init__(text_color=(0.95, 0.98, 1.0, 0.95), **kwargs)
        self.font_size = '15sp'
        self.markup = True  # Enable markup for formatting
        self.text_size = (None, None)
        self.halign = 'left'  # Left align for better readability
        self.valign = 'top'


class StockAnalyzerLayout(FloatLayout):
    """Main application layout with content management"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Color scheme
        self.colors = {
            'success': (0.9, 1, 0.9, 1),
            'warning': (1, 0.7, 0.3, 1),
            'error': (1, 0.7, 0.7, 1),
            'info': (0.7, 0.9, 1, 1)
        }
        
        self._setup_layout()
    
    def _setup_layout(self):
        """Setup the main content layout"""
        # Content container with proper spacing
        self.content_layout = BoxLayout(
            orientation="vertical",
            padding=[40, 80, 40, 120],  # Extra bottom padding for wave
            spacing=25,
            size_hint=(0.8, 0.7),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        
        self.add_widget(self.content_layout)
        
        # Create UI components
        self._create_header()
        self._create_input_section()
        self._create_results_section()
    
    def _create_header(self):
        """Create header section with title and subtitle"""
        # Main title with responsive sizing
        self.title = TitleLabel(
            text="Stock Risk Analyzer",
            size_hint=(1, None),
            height='40dp'  # Fixed height to prevent squashing
        )
        
        # Subtitle with responsive sizing
        self.subtitle = SubtitleLabel(
            text="Enter a stock ticker to analyze volatility and risk metrics",
            size_hint=(1, None),
            height='30dp'  # Fixed height
        )
        
        self.content_layout.add_widget(self.title)
        self.content_layout.add_widget(self.subtitle)
    
    def _create_input_section(self):
        """Create input section with ticker input and analyze button"""
        # Ticker input field with fixed height
        self.ticker_input = ModernTextInput(
            hint_text="Enter stock ticker (e.g. AAPL, PTTEP.BK)",
            size_hint=(1, None),
            height='45dp'  # Fixed height to prevent squashing
        )
        
        # Analyze button with fixed height
        self.analyze_button = ModernButton(
            text="ANALYZE STOCK",
            size_hint=(1, None),
            height='50dp'  # Fixed height
        )
        
        self.content_layout.add_widget(self.ticker_input)
        self.content_layout.add_widget(self.analyze_button)
    
    def _create_results_section(self):
        """Create results display section"""
        # Results container that takes remaining space
        result_container = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1),  # Takes all remaining space
            spacing=5
        )
        
        # Results label with scroll capability for long results
        self.result_label = ResultLabel(
            text="Results will appear here after analysis...",
            size_hint=(1, 1),
            text_size=(None, None)  # Will be updated dynamically
        )
        
        result_container.add_widget(self.result_label)
        self.content_layout.add_widget(result_container)
    
    def set_result_text(self, text: str, result_type: str = "info"):
        """
        Set result text with appropriate color coding
        
        Args:
            text (str): Text to display
            result_type (str): Type of result ('success', 'warning', 'error', 'info')
        """
        self.result_label.text = text
        
        if result_type in self.colors:
            self.result_label.color = self.colors[result_type]
        else:
            self.result_label.color = self.colors['info']
    
    def set_loading_state(self, is_loading: bool = True):
        """Set loading state for the interface"""
        if is_loading:
            self.set_result_text("📊 Analyzing stock data...", "info")
            self.analyze_button.text = "ANALYZING..."
            self.analyze_button.disabled = True
        else:
            self.analyze_button.text = "ANALYZE STOCK"
            self.analyze_button.disabled = False
    
    def get_ticker_input(self) -> str:
        """Get the current ticker input value"""
        return self.ticker_input.text.strip().upper()
    
    def clear_ticker_input(self):
        """Clear the ticker input field"""
        self.ticker_input.text = ""
    
    def bind_analyze_button(self, callback: Callable):
        """Bind callback to analyze button"""
        def on_button_press(instance):
            # Animate button press
            instance.animate_press()
            # Call the callback
            callback(instance)
        
        self.analyze_button.bind(on_press=on_button_press)


class ResponsiveLayout(BoxLayout):
    """Responsive layout that adapts to window size"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(size=self._update_layout)
        self._update_layout()
    
    def _update_layout(self, *args):
        """Update layout based on window size"""
        width, height = Window.size
        
        # Adjust spacing and padding based on screen size
        if width < 800:  # Mobile/small screen
            self.padding = [20, 40, 20, 60]
            self.spacing = 15
        else:  # Desktop/large screen
            self.padding = [40, 80, 40, 120]
            self.spacing = 25


def create_main_ui() -> StockAnalyzerLayout:
    """
    Factory function to create the main UI layout
    
    Returns:
        StockAnalyzerLayout: Complete UI layout ready for use
    """
    return StockAnalyzerLayout()


def create_input_field(hint: str, size_hint: tuple = (1, 0.15)) -> ModernTextInput:
    """
    Create a styled input field
    
    Args:
        hint (str): Hint text for the input
        size_hint (tuple): Size hint for the input
        
    Returns:
        ModernTextInput: Styled input field
    """
    return ModernTextInput(hint_text=hint, size_hint=size_hint)


def create_action_button(text: str, size_hint: tuple = (1, 0.15)) -> ModernButton:
    """
    Create a styled action button
    
    Args:
        text (str): Button text
        size_hint (tuple): Size hint for the button
        
    Returns:
        ModernButton: Styled button
    """
    return ModernButton(text=text, size_hint=size_hint)