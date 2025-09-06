"""
Background and Wave Animation Module
Creates beautiful smooth filled wave animations like React Sine Wave
"""

import math
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate, Mesh
from kivy.graphics.texture import Texture
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
        
        # Animation properties for smooth ocean movement
        self.time = 0
        self.speed = 0.015  # Slower, more gentle ocean movement
        
        # Ocean-like wave configuration with smooth blue gradient
        self.waves = [
            SmoothWave((0.05, 0.2, 0.5), 80, 0.006, 0, 0.9),      # Deep ocean wave (dark blue)
            SmoothWave((0.1, 0.3, 0.65), 65, 0.008, 1.2, 0.7),    # Mid ocean wave
            SmoothWave((0.2, 0.45, 0.8), 50, 0.01, 2.5, 0.5),     # Surface wave
            SmoothWave((0.35, 0.6, 0.9), 35, 0.012, 3.8, 0.3),    # Light wave
            SmoothWave((0.5, 0.75, 0.95), 20, 0.014, 5.1, 0.2)    # Foam wave (lightest blue)
        ]
        
        # Start animation with better performance
        self.bind(size=self._update_waves, pos=self._update_waves)
        Clock.schedule_interval(self._animate, 1/30.0)  # 30 FPS for performance
    
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
            
            # Position wave in bottom area with more natural distribution
            # Lower waves are deeper in the ocean
            base_height = self.height * (0.2 + (wave.amplitude / 100) * 0.3)
            y = self.y + base_height + wave_y
            
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
        
        # Ocean night gradient colors (smooth light to dark blue)
        self.bg_colors = {
            'deep_night': (0.02, 0.08, 0.25, 1),     # Deep ocean night (darkest)
            'night': (0.03, 0.12, 0.32, 1),          # Night ocean
            'twilight': (0.05, 0.18, 0.42, 1),       # Twilight ocean
            'dusk': (0.08, 0.25, 0.52, 1),           # Dusk ocean
            'evening': (0.12, 0.35, 0.65, 1),        # Evening ocean
            'surface': (0.18, 0.45, 0.75, 1),        # Surface ocean
            'light': (0.25, 0.55, 0.85, 1)           # Light ocean (lightest)
        }
        
        Window.bind(size=self._update_background)
        self.bind(size=self._update_background)
        self._update_background()
    
    def _update_background(self, *args):
        """Create smooth ocean-like gradient background"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Create smooth ocean gradient with multiple layers
            # Start from deepest ocean (bottom/darkest)
            Color(*self.bg_colors['deep_night'])
            Rectangle(pos=(0, 0), size=Window.size)
            
            # Layer 1: Night ocean (covers bottom 85%)
            Color(*self.bg_colors['night'])
            Rectangle(pos=(0, Window.height * 0.15), size=(Window.width, Window.height * 0.85))
            
            # Layer 2: Twilight ocean (covers bottom 70%)
            Color(*self.bg_colors['twilight'])
            Rectangle(pos=(0, Window.height * 0.30), size=(Window.width, Window.height * 0.70))
            
            # Layer 3: Dusk ocean (covers bottom 55%)
            Color(*self.bg_colors['dusk'])
            Rectangle(pos=(0, Window.height * 0.45), size=(Window.width, Window.height * 0.55))
            
            # Layer 4: Evening ocean (covers bottom 40%)
            Color(*self.bg_colors['evening'])
            Rectangle(pos=(0, Window.height * 0.60), size=(Window.width, Window.height * 0.40))
            
            # Layer 5: Surface ocean (covers bottom 25%)
            Color(*self.bg_colors['surface'])
            Rectangle(pos=(0, Window.height * 0.75), size=(Window.width, Window.height * 0.25))
            
            # Layer 6: Light ocean (covers bottom 10% - lightest at top)
            Color(*self.bg_colors['light'])
            Rectangle(pos=(0, Window.height * 0.90), size=(Window.width, Window.height * 0.10))


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


class SmoothOceanGradient(FloatLayout):
    """Smooth ocean gradient using texture-based approach like your reference image"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Ocean gradient colors (bottom to top) - ultra-smooth like your reference
        self.gradient_colors = [
            (0.008, 0.055, 0.20),   # Deepest ocean (bottom) - almost black blue
            (0.012, 0.075, 0.24),   # Abyssal
            (0.018, 0.095, 0.28),   # Deep night
            (0.025, 0.120, 0.32),   # Night
            (0.035, 0.150, 0.37),   # Late night 
            (0.048, 0.185, 0.42),   # Midnight
            (0.065, 0.225, 0.47),   # Twilight
            (0.085, 0.270, 0.52),   # Early twilight
            (0.110, 0.320, 0.58),   # Dusk
            (0.140, 0.375, 0.64),   # Evening
            (0.175, 0.435, 0.70),   # Surface evening
            (0.215, 0.500, 0.76),   # Surface
            (0.260, 0.570, 0.82),   # Light surface (top) - lighter blue
        ]
        
        self.gradient_texture = None
        
        Window.bind(size=self._create_smooth_gradient)
        self.bind(size=self._create_smooth_gradient)
        self._create_smooth_gradient()
    
    def _create_gradient_texture(self, width, height):
        """Create ultra-smooth gradient texture like your reference image"""
        # Use high resolution for ultra-smooth gradient
        gradient_height = max(height * 2, 1024)  # Higher resolution for smoother effect
        gradient_data = []
        
        num_colors = len(self.gradient_colors)
        
        for y in range(gradient_height):
            # Calculate position in gradient (0 = bottom/dark, 1 = top/light)
            t = y / (gradient_height - 1)
            
            # Apply smooth curve for more natural transition
            # Use smoothstep function for even smoother transitions
            t = t * t * (3.0 - 2.0 * t)  # Smoothstep function
            
            # Find which color segment we're in
            segment = t * (num_colors - 1)
            segment_index = int(segment)
            local_t = segment - segment_index
            
            # Apply another smoothstep to local interpolation
            local_t = local_t * local_t * (3.0 - 2.0 * local_t)
            
            # Clamp to valid range
            if segment_index >= num_colors - 1:
                segment_index = num_colors - 2
                local_t = 1.0
            
            # Interpolate between colors with smooth blending
            color1 = self.gradient_colors[segment_index]
            color2 = self.gradient_colors[segment_index + 1]
            
            # Ultra-smooth interpolation
            r = color1[0] + (color2[0] - color1[0]) * local_t
            g = color1[1] + (color2[1] - color1[1]) * local_t
            b = color1[2] + (color2[2] - color1[2]) * local_t
            
            # Convert to 0-255 and add to data (RGBA format)
            gradient_data.extend([
                min(255, max(0, int(r * 255))),
                min(255, max(0, int(g * 255))), 
                min(255, max(0, int(b * 255))),
                255
            ])
        
        # Create texture with high quality filtering
        texture = Texture.create(size=(1, gradient_height))
        texture.mag_filter = 'linear'  # Linear filtering for smoothness
        texture.min_filter = 'linear'
        texture.blit_buffer(bytes(gradient_data), colorfmt='rgba', bufferfmt='ubyte')
        return texture
    
    def _create_smooth_gradient(self, *args):
        """Create smooth ocean gradient using texture"""
        if Window.width <= 0 or Window.height <= 0:
            return
            
        self.canvas.before.clear()
        
        # Create gradient texture
        self.gradient_texture = self._create_gradient_texture(Window.width, Window.height)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White color to not tint the texture
            Rectangle(
                texture=self.gradient_texture,
                pos=(0, 0),
                size=(Window.width, Window.height)
            )


def create_ocean_background() -> FloatLayout:
    """Create enhanced ocean background with ultra-smooth gradients"""
    background = SmoothOceanGradient()
    
    # Add beautiful wave animation
    wave_widget = BeautifulWaveWidget(
        size_hint=(1, 0.75),  # Cover more of the screen for better effect
        pos_hint={'x': 0, 'y': 0}
    )
    
    background.add_widget(wave_widget)
    return background


# Factory function for main app
def create_animated_background() -> FloatLayout:
    """Create the main animated background for the app"""
    return create_ocean_background()
