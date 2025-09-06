"""
Background and Wave Animation Module
Creates beautiful smooth filled wave animations like React Sine Wave
"""

import math
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.clock import Clock
from kivy.core.window import Window
from typing import List, Dict, Any


class SmoothWave:
    """Individual smooth wave configuration"""
    def __init__(self, color: tuple, amplitude: float, frequency: float, phase: float, opacity: float):
        self.color = color
        self.amplitude = amplitude  # Wave height
        self.frequency = frequency  # Wave length
        self.phase = phase         # Wave offset
        self.opacity = opacity     # Transparency


class BeautifulWaveWidget(Widget):
    """Creates beautiful smooth filled waves like React Sine Wave"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Animation properties
        self.time = 0
        self.speed = 0.02  # Animation speed
        
        # Wave configuration - multiple layers for depth
        self.waves = [
            SmoothWave(
                color=(0.2, 0.4, 0.9),   # Deep blue
                amplitude=80,
                frequency=0.008,
                phase=0,
                opacity=0.9
            ),
            SmoothWave(
                color=(0.3, 0.5, 0.95),  # Medium blue  
                amplitude=60,
                frequency=0.01,
                phase=1.5,
                opacity=0.7
            ),
            SmoothWave(
                color=(0.4, 0.6, 1.0),   # Light blue
                amplitude=40,
                frequency=0.012,
                phase=3,
                opacity=0.5
            ),
            SmoothWave(
                color=(0.5, 0.7, 1.0),   # Very light blue
                amplitude=25,
                frequency=0.015,
                phase=4.5,
                opacity=0.3
            )
        ]
        
        # Start animation
        self.bind(size=self._update_waves, pos=self._update_waves)
        Clock.schedule_interval(self._animate, 1/60.0)  # 60 FPS
    
    def _animate(self, dt):
        """Update animation time and redraw waves"""
        self.time += self.speed
        self._update_waves()
    
    def _update_waves(self, *args):
        """Draw all wave layers"""
        if self.width <= 0 or self.height <= 0:
            return
            
        self.canvas.clear()
        
        with self.canvas:
            # Draw waves from back to front (largest to smallest)
            for wave in reversed(self.waves):
                self._draw_filled_wave(wave)
    
    def _draw_filled_wave(self, wave: SmoothWave):
        """Draw a single smooth filled wave"""
        Color(*wave.color, wave.opacity)
        
        # Create wave points with high resolution for smoothness
        points = []
        segments = max(int(self.width / 2), 100)  # High resolution
        
        for i in range(segments + 1):
            x = (i * self.width) / segments
            
            # Calculate sine wave with time animation
            wave_y = math.sin(x * wave.frequency + self.time + wave.phase) * wave.amplitude
            
            # Position wave in bottom area
            y = self.y + self.height * 0.3 + wave_y
            
            points.extend([x + self.x, y])
        
        # Create filled wave using rectangles (most reliable method)
        self._create_wave_fill(points, wave)
    
    def _create_wave_fill(self, wave_points: List[float], wave: SmoothWave):
        """Create filled wave using vertical strips"""
        Color(*wave.color, wave.opacity)
        
        # Draw vertical strips to create filled effect
        strip_width = max(1, self.width / len(wave_points) * 2)
        
        for i in range(0, len(wave_points) - 2, 2):
            x = wave_points[i]
            y = wave_points[i + 1]
            
            # Draw rectangle from bottom to wave height
            rect_height = y - self.y
            if rect_height > 0:
                Rectangle(
                    pos=(x, self.y),
                    size=(strip_width, rect_height)
                )


class SimpleWaveWidget(Widget):
    """Simplified wave widget for better performance"""
    
    def __init__(self, wave_color=(0.2, 0.5, 1.0, 0.8), **kwargs):
        super().__init__(**kwargs)
        
        self.wave_color = wave_color
        self.time = 0
        self.amplitude = 60
        self.frequency = 0.01
        self.speed = 0.03
        
        self.bind(size=self._redraw, pos=self._redraw)
        Clock.schedule_interval(self._animate, 1/30.0)  # 30 FPS for performance
    
    def _animate(self, dt):
        self.time += self.speed
        self._redraw()
    
    def _redraw(self, *args):
        if self.width <= 0 or self.height <= 0:
            return
            
        self.canvas.clear()
        
        with self.canvas:
            Color(*self.wave_color)
            
            # Create wave using rectangles
            segments = max(int(self.width / 3), 50)
            segment_width = self.width / segments
            
            for i in range(segments):
                x = i * segment_width
                wave_y = math.sin(x * self.frequency + self.time) * self.amplitude
                y = self.y + self.height * 0.4 + wave_y
                
                height = y - self.y
                if height > 0:
                    Rectangle(
                        pos=(x + self.x, self.y),
                        size=(segment_width + 1, height)  # +1 to avoid gaps
                    )


class BackgroundWidget(FloatLayout):
    """Beautiful gradient background"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Background colors (dark blue gradient)
        self.bg_colors = {
            'dark': (0.05, 0.15, 0.35, 1),
            'medium': (0.08, 0.18, 0.38, 1),
            'light': (0.12, 0.22, 0.42, 1)
        }
        
        Window.bind(size=self._update_background)
        self.bind(size=self._update_background)
        self._update_background()
    
    def _update_background(self, *args):
        """Create gradient background"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Base dark background
            Color(*self.bg_colors['dark'])
            Rectangle(pos=(0, 0), size=Window.size)
            
            # Gradient layers
            Color(*self.bg_colors['medium'])
            Rectangle(pos=(0, Window.height * 0.6), size=(Window.width, Window.height * 0.4))
            
            Color(*self.bg_colors['light'])
            Rectangle(pos=(0, Window.height * 0.8), size=(Window.width, Window.height * 0.2))


def create_wave_background(wave_type="beautiful") -> FloatLayout:
    """
    Create animated wave background
    
    Args:
        wave_type: "beautiful" for multi-layer waves, "simple" for single wave
    """
    background = BackgroundWidget()
    
    if wave_type == "beautiful":
        wave_widget = BeautifulWaveWidget(
            size_hint=(1, 0.7),  # Cover more of the screen
            pos_hint={'x': 0, 'y': 0}
        )
    else:
        wave_widget = SimpleWaveWidget(
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'y': 0}
        )
    
    background.add_widget(wave_widget)
    return background


def create_simple_blue_waves() -> BeautifulWaveWidget:
    """Create simple blue waves like the reference"""
    return BeautifulWaveWidget(
        size_hint=(1, 0.6),
        pos_hint={'x': 0, 'y': 0}
    )


# Factory function for main app
def create_animated_background() -> FloatLayout:
    """Create the main animated background for the app"""
    return create_wave_background("beautiful")