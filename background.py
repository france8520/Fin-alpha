"""
Optimized Background and Wave Animation Module
Major performance improvements for fullscreen usage
"""

import math
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Mesh
from kivy.graphics.texture import Texture
from kivy.graphics.instructions import InstructionGroup
from kivy.clock import Clock
from kivy.core.window import Window
from typing import List


class OptimizedWaveWidget(Widget):
    """Highly optimized wave animation using mesh and reduced updates"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.time = 0
        self.speed = 0.015
        self.update_interval = 1/15.0  # Reduced to 15 FPS for better performance
        
        # Simplified wave configuration (fewer waves = better performance)
        self.waves = [
            {'color': (0.05, 0.2, 0.5, 0.8), 'amp': 60, 'freq': 0.006, 'phase': 0},
            {'color': (0.15, 0.4, 0.7, 0.6), 'amp': 40, 'freq': 0.008, 'phase': 2},
            {'color': (0.3, 0.6, 0.85, 0.4), 'amp': 25, 'freq': 0.01, 'phase': 4}
        ]
        
        # Pre-calculate segments based on window width once
        self.segments = 0
        self.wave_instructions = []
        
        self.bind(size=self._setup_waves, pos=self._setup_waves)
        self._animation_event = None
        self.start_animation()
    
    def _setup_waves(self, *args):
        """Setup wave meshes - only called on resize"""
        if self.width <= 0 or self.height <= 0:
            return
        
        # Adaptive segment count based on width (fewer segments = better performance)
        self.segments = min(max(int(self.width / 8), 30), 100)
        self._update_waves()
    
    def start_animation(self):
        """Start the animation loop"""
        if self._animation_event:
            self._animation_event.cancel()
        self._animation_event = Clock.schedule_interval(self._animate, self.update_interval)
    
    def stop_animation(self):
        """Stop the animation loop to save resources"""
        if self._animation_event:
            self._animation_event.cancel()
            self._animation_event = None
    
    def _animate(self, dt):
        """Update animation time and redraw"""
        self.time += self.speed
        self._update_waves()
    
    def _update_waves(self, *args):
        """Draw all waves using optimized rectangle strips"""
        if self.width <= 0 or self.height <= 0 or self.segments == 0:
            return
        
        self.canvas.clear()
        
        segment_width = self.width / self.segments
        
        with self.canvas:
            for wave in self.waves:
                Color(*wave['color'])
                
                # Draw wave using vertical strips (much faster than individual rectangles)
                for i in range(self.segments):
                    x = i * segment_width
                    wave_y = math.sin(x * wave['freq'] + self.time + wave['phase']) * wave['amp']
                    base_y = self.height * 0.25
                    y = self.y + base_y + wave_y
                    
                    height = max(0, y - self.y)
                    if height > 0:
                        Rectangle(
                            pos=(x + self.x, self.y),
                            size=(segment_width + 1, height)
                        )


class OptimizedGradient(FloatLayout):
    """Optimized gradient that only creates texture once"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Simplified gradient colors
        self.gradient_colors = [
            (0.01, 0.06, 0.20),
            (0.03, 0.12, 0.30),
            (0.06, 0.20, 0.42),
            (0.12, 0.35, 0.60),
            (0.20, 0.50, 0.75),
            (0.30, 0.65, 0.85)
        ]
        
        self.gradient_texture = None
        self.gradient_instruction = None
        
        Window.bind(size=self._schedule_update)
        self.bind(size=self._schedule_update)
        self._update_scheduled = False
        
        self._create_gradient()
    
    def _schedule_update(self, *args):
        """Debounce resize events to avoid recreating texture too often"""
        if not self._update_scheduled:
            self._update_scheduled = True
            Clock.schedule_once(self._delayed_update, 0.3)
    
    def _delayed_update(self, dt):
        """Actually update after debounce delay"""
        self._update_scheduled = False
        self._create_gradient()
    
    def _create_gradient_texture(self):
        """Create gradient texture with reasonable resolution"""
        # Use fixed reasonable resolution instead of scaling with window
        gradient_height = 512  # Fixed size for better performance
        gradient_data = []
        
        num_colors = len(self.gradient_colors)
        
        for y in range(gradient_height):
            t = y / (gradient_height - 1)
            t = t * t * (3.0 - 2.0 * t)  # Smoothstep
            
            segment = t * (num_colors - 1)
            segment_index = min(int(segment), num_colors - 2)
            local_t = segment - segment_index
            local_t = local_t * local_t * (3.0 - 2.0 * local_t)
            
            color1 = self.gradient_colors[segment_index]
            color2 = self.gradient_colors[segment_index + 1]
            
            r = int((color1[0] + (color2[0] - color1[0]) * local_t) * 255)
            g = int((color1[1] + (color2[1] - color1[1]) * local_t) * 255)
            b = int((color1[2] + (color2[2] - color1[2]) * local_t) * 255)
            
            gradient_data.extend([r, g, b, 255])
        
        texture = Texture.create(size=(1, gradient_height))
        texture.mag_filter = 'linear'
        texture.min_filter = 'linear'
        texture.blit_buffer(bytes(gradient_data), colorfmt='rgba', bufferfmt='ubyte')
        return texture
    
    def _create_gradient(self, *args):
        """Create gradient background"""
        if Window.width <= 0 or Window.height <= 0:
            return
        
        self.canvas.before.clear()
        
        if not self.gradient_texture:
            self.gradient_texture = self._create_gradient_texture()
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(
                texture=self.gradient_texture,
                pos=(0, 0),
                size=(Window.width, Window.height)
            )


def create_animated_background() -> FloatLayout:
    """Create optimized animated background"""
    background = OptimizedGradient()
    
    wave_widget = OptimizedWaveWidget(
        size_hint=(1, 0.6),
        pos_hint={'x': 0, 'y': 0}
    )
    
    background.add_widget(wave_widget)
    background.wave_widget = wave_widget  # Store reference for stopping animation
    return background