#!/usr/bin/env python3
"""
Demo script for Mandala Art Generator
Creates sample mandala patterns and saves them as SVG files.
"""

import os
from mandala_generator import MandalaGenerator, create_preset_mandala
from svg_generator import save_mandala_svg

def create_sample_mandalas():
    """Create various sample mandala patterns."""
    print("🎨 Generating sample mandala patterns...")
    
    # Create output directory
    output_dir = "sample_mandalas"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate preset mandalas
    presets = ["classic", "complex", "simple", "floral", "geometric"]
    
    for preset in presets:
        print(f"  Creating {preset} mandala...")
        mandala_data = create_preset_mandala(preset)
        filename = os.path.join(output_dir, f"mandala_{preset}.svg")
        save_mandala_svg(mandala_data, filename)
        print(f"  ✅ Saved: {filename}")
    
    # Generate custom mandalas with different parameters
    generator = MandalaGenerator(size=600)
    
    custom_configs = [
        {
            "name": "rainbow_burst",
            "layers": 8,
            "symmetry": 12,
            "pattern_types": ["circles", "stars", "dots"],
            "color_scheme": "rainbow",
            "complexity": 0.9
        },
        {
            "name": "earth_tones",
            "layers": 5,
            "symmetry": 6,
            "pattern_types": ["geometric", "triangles"],
            "color_scheme": "earth",
            "complexity": 0.6
        },
        {
            "name": "cool_waves",
            "layers": 7,
            "symmetry": 10,
            "pattern_types": ["lines", "petals", "circles"],
            "color_scheme": "cool",
            "complexity": 0.8
        }
    ]
    
    for config in custom_configs:
        name = config.pop("name")
        print(f"  Creating {name} mandala...")
        mandala_data = generator.generate_mandala(**config)
        filename = os.path.join(output_dir, f"mandala_{name}.svg")
        save_mandala_svg(mandala_data, filename)
        print(f"  ✅ Saved: {filename}")
    
    print(f"\n🎉 Generated {len(presets) + len(custom_configs)} mandala patterns!")
    print(f"📁 Check the '{output_dir}' folder for SVG files")
    print("💡 Open the SVG files in a web browser or vector graphics editor to view them")

def demonstrate_api_usage():
    """Show how to use the mandala generator programmatically."""
    print("\n🔧 Demonstrating API usage...")
    
    # Create a simple mandala
    generator = MandalaGenerator(size=400)
    mandala = generator.generate_mandala(
        layers=4,
        symmetry=8,
        pattern_types=["circles", "petals"],
        color_scheme="warm",
        complexity=0.5
    )
    
    print(f"Generated mandala with {len(mandala['elements'])} elements")
    print(f"Canvas size: {mandala['size']}x{mandala['size']}")
    print(f"Layers: {mandala['layers']}")
    print(f"Symmetry: {mandala['symmetry']}")
    print(f"Colors used: {len(mandala['colors'])}")

if __name__ == "__main__":
    print("🎨 Mandala Art Generator Demo")
    print("=" * 40)
    
    create_sample_mandalas()
    demonstrate_api_usage()
    
    print("\n🚀 To start the API server, run:")
    print("   python main.py")
    print("\n📖 Then visit http://localhost:8001/docs for interactive API documentation")
