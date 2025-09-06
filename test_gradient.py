"""
Test script to visualize the ocean gradient colors
"""

def print_ocean_gradient():
    """Print the ocean gradient color values for visualization"""
    
    print("🌊 ULTRA-SMOOTH Ocean Gradient - Like Your Reference Image 🌊\n")
    
    ocean_layers = [
        # Ultra-smooth ocean gradient (darkest to lighter)
        (0.008, 0.055, 0.20, "Deepest Ocean (bottom)"),
        (0.012, 0.075, 0.24, "Abyssal"),
        (0.018, 0.095, 0.28, "Deep Night"),
        (0.025, 0.120, 0.32, "Night"),
        (0.035, 0.150, 0.37, "Late Night"),
        (0.048, 0.185, 0.42, "Midnight"),
        (0.065, 0.225, 0.47, "Twilight"),
        (0.085, 0.270, 0.52, "Early Twilight"),
        (0.110, 0.320, 0.58, "Dusk"),
        (0.140, 0.375, 0.64, "Evening"),
        (0.175, 0.435, 0.70, "Surface Evening"),
        (0.215, 0.500, 0.76, "Surface"),
        (0.260, 0.570, 0.82, "Light Surface (top)"),
    ]
    
    print("Ultra-Smooth Gradient Colors (Bottom to Top):")
    print("===============================================")
    
    for r, g, b, name in ocean_layers:
        # Convert to 0-255 for easier visualization
        r255 = int(r * 255)
        g255 = int(g * 255)
        b255 = int(b * 255)
        
        print(f"{name:20} | RGB({r255:3}, {g255:3}, {b255:3})")
    
    print("\n✨ IMPROVEMENTS:")
    print("- Texture-based rendering (no more brick effect!)")
    print("- Higher resolution (1024px+ gradient)")
    print("- Smoothstep interpolation function")
    print("- Linear texture filtering")
    print("- 13 color stops for ultra-smooth transitions")
    
    print("\nWave Colors:")
    print("=============")
    
    wave_colors = [
        (0.05, 0.2, 0.5, "Deep Ocean Wave"),
        (0.1, 0.3, 0.65, "Mid Ocean Wave"),
        (0.2, 0.45, 0.8, "Surface Wave"),
        (0.35, 0.6, 0.9, "Light Wave"),
        (0.5, 0.75, 0.95, "Foam Wave")
    ]
    
    for r, g, b, name in wave_colors:
        r255 = int(r * 255)
        g255 = int(g * 255)
        b255 = int(b * 255)
        
        print(f"{name:15} | RGB({r255:3}, {g255:3}, {b255:3})")

if __name__ == "__main__":
    print_ocean_gradient()
