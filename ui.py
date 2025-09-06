"""
UI Components Module - Improved and Shortened
Contains all custom UI components with better visibility and prominent risk display
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
from typing import Callable


class ModernTextInput(TextInput):
    """Styled text input with better visibility"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Better visibility styling
        self.background_color = (1, 1, 1, 0.95)
        self.foreground_color = (0.1, 0.1, 0.1, 1)
        self.cursor_color = (0.1, 0.3, 0.7, 1)
        self.font_size = '20sp'  # Larger for better visibility
        self.padding = [15, 12]
        self.multiline = False


class ModernButton(Button):
    """Styled button with better visibility"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.font_size = '20sp'  # Larger for visibility
        self.bold = True
        self.color = (1, 1, 1, 1)
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        """Update button graphics"""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.1, 0.4, 0.8, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.05, 0.2, 0.4, 0.3)
            Rectangle(pos=(self.x + 2, self.y - 2), size=self.size)
    
    def animate_press(self):
        """Simple press animation"""
        anim = Animation(size=(self.width * 0.95, self.height * 0.95), duration=0.05)
        anim += Animation(size=(self.width, self.height), duration=0.05)
        anim.start(self)


class ModernLabel(Label):
    """Styled label with better visibility"""
    
    def __init__(self, text_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.color = text_color
        self.font_size = '18sp'  # Larger for better visibility
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=self._update_text_size)
    
    def _update_text_size(self, *args):
        if self.width > 0:
            self.text_size = (self.width * 0.9, None)


class TitleLabel(ModernLabel):
    """Large title label"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '28sp'
        self.bold = True

class SubtitleLabel(ModernLabel):
    """Subtitle label with better contrast"""
    def __init__(self, **kwargs):
        super().__init__(text_color=(0.9, 0.95, 1, 0.9), **kwargs)
        self.font_size = '16sp'


class ScrollableResultLabel(ScrollView):
    """Scrollable container with better visibility"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.bar_width = 8
        
        # Better visibility settings
        self.result_label = Label(
            text="Results will appear here after analysis...",
            halign='left',
            valign='top',
            color=(1, 1, 1, 0.95),  # Higher contrast
            font_size='18sp',  # Larger for better visibility
            markup=True
        )
        
        self.add_widget(self.result_label)
        self.bind(size=self._update_text_size)
    
    def _update_text_size(self, *args):
        if self.width > 0:
            self.result_label.text_size = (self.width - 16, None)
            self.result_label.height = max(self.result_label.texture_size[1], self.height)
            self.result_label.size_hint_y = None
    
    def set_text(self, text: str, color: tuple = (1, 1, 1, 0.95)):
        self.result_label.text = text
        self.result_label.color = color
        self._update_text_size()


class ResultDisplayPanel(BoxLayout):
    """Results panel with prominent risk display"""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # Risk Level Display (most prominent)
        self.risk_label = Label(
            text="",
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height='60dp',
            markup=True
        )
        
        # Results area
        self.results_scroll = ScrollableResultLabel(size_hint=(1, 1))
        
        self.add_widget(self.risk_label)
        self.add_widget(self.results_scroll)
    
    def set_results(self, text: str, result_type: str = "info"):
        """Set results with prominent risk display"""
        colors = {
            'success': (1, 1, 1, 1),
            'warning': (1, 0.9, 0.5, 1),
            'error': (1, 0.7, 0.7, 1),
            'info': (1, 1, 1, 0.9)
        }
        
        # Extract and display risk level prominently
        risk_level = self._extract_risk_level(text)
        if risk_level:
            self._set_risk_display(risk_level)
        else:
            self.risk_label.text = ""
        
        # Format and display main results
        formatted_text = self._format_text(text)
        self.results_scroll.set_text(formatted_text, colors.get(result_type, colors['info']))
    
    def _extract_risk_level(self, text: str) -> str:
        """Extract risk level from analysis text"""
        if "Risk Level:" in text:
            for line in text.split('\n'):
                if "Risk Level:" in line:
                    return line.split(":")[-1].strip()
        return ""
    
    def _set_risk_display(self, risk_level: str):
        """Set prominent risk level display"""
        colors = {
            "HIGH": "ff4444",    # Bright red
            "MEDIUM": "ffaa00",  # Orange
            "LOW": "44ff44"      # Bright green
        }
        
        color = colors.get(risk_level, "ffffff")
        self.risk_label.text = f"[color={color}][size=28sp]RISK: {risk_level}[/size][/color]"
    
    def _format_text(self, text: str) -> str:
        """Format text for better visibility"""
        if "ANALYSIS RESULTS FOR" in text:
            lines = text.split('\n')
            formatted = []
            
            for line in lines:
                line = line.strip()
                if "ANALYSIS RESULTS FOR" in line:
                    ticker = line.split("FOR ")[-1]
                    formatted.append(f"[size=22sp][b]{ticker} ANALYSIS[/b][/size]")
                elif "Current Price:" in line:
                    price = line.split(": ")[-1]
                    formatted.append(f"[size=20sp][b]Price: [color=90ff90]{price}[/color][/b][/size]")
                elif "RISK METRICS:" in line:
                    formatted.append(f"[size=18sp][b]METRICS:[/b][/size]")
                elif line.startswith("• ") and ":" in line:
                    name, value = line[2:].split(":", 1)
                    formatted.append(f"[size=16sp]• [b]{name}:[/b]{value}[/size]")
                elif line and "Risk Level:" not in line:  # Skip risk level (shown above)
                    formatted.append(f"[size=16sp]{line}[/size]")
            
            return "\n".join(formatted)
        return f"[size=18sp]{text}[/size]"


class StockAnalyzerLayout(FloatLayout):
    """Main application layout with better windowed mode support"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main content container - better proportions for windowed mode
        self.content_layout = BoxLayout(
            orientation="vertical",
            padding=[20, 40, 20, 60],  # Reduced padding
            spacing=15,
            size_hint=(0.95, 0.85),  # Use more screen space
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.add_widget(self.content_layout)
        self._create_components()
    
    def _create_components(self):
        """Create all UI components"""
        # Header (smaller)
        header_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height='80dp',
            spacing=5
        )
        
        self.title = TitleLabel(
            text="FIN-ALPHA",
            size_hint=(1, None),
            height='40dp'
        )
        
        self.subtitle = SubtitleLabel(
            text="Enter ticker to analyze risk",
            size_hint=(1, None),
            height='30dp'
        )
        
        header_box.add_widget(self.title)
        header_box.add_widget(self.subtitle)
        
        # Input section (compact)
        input_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height='100dp',
            spacing=10
        )
        
        self.ticker_input = ModernTextInput(
            hint_text="Enter ticker (e.g. AAPL, TSLA)",
            size_hint=(1, None),
            height='45dp'
        )
        
        self.analyze_button = ModernButton(
            text="ANALYZE STOCK",
            size_hint=(1, None),
            height='45dp'
        )
        
        input_box.add_widget(self.ticker_input)
        input_box.add_widget(self.analyze_button)
        
        # Results panel (takes remaining space)
        self.result_panel = ResultDisplayPanel(size_hint=(1, 1))
        
        # Add all components
        self.content_layout.add_widget(header_box)
        self.content_layout.add_widget(input_box)
        self.content_layout.add_widget(self.result_panel)
    
    def set_result_text(self, text: str, result_type: str = "info"):
        self.result_panel.set_results(text, result_type)
    
    def set_loading_state(self, is_loading: bool = True):
        if is_loading:
            self.set_result_text("Analyzing stock data...\n\nPlease wait.", "info")
            self.analyze_button.text = "ANALYZING..."
            self.analyze_button.disabled = True
        else:
            self.analyze_button.text = "ANALYZE STOCK"
            self.analyze_button.disabled = False
    
    def get_ticker_input(self) -> str:
        return self.ticker_input.text.strip().upper()
    
    def bind_analyze_button(self, callback: Callable):
        def on_press(instance):
            instance.animate_press()
            callback(instance)
        self.analyze_button.bind(on_press=on_press)


# Factory function
def create_main_ui() -> StockAnalyzerLayout:
    """Create the main UI layout"""
    return StockAnalyzerLayout()
