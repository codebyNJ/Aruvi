import math
import random
from typing import List, Tuple, Optional, Dict, Any
import colorsys


class MandalaGenerator:
    """
    Advanced Mandala Art Generator with geometric patterns, symmetry, and customizable designs.
    Creates beautiful mandala patterns with various geometric elements and color schemes.
    """
    
    def __init__(self, size: int = 800, center: Optional[Tuple[int, int]] = None):
        """
        Initialize the mandala generator.
        
        Args:
            size: Canvas size (width and height)
            center: Center point of the mandala (defaults to canvas center)
        """
        self.size = size
        self.center = center or (size // 2, size // 2)
        self.cx, self.cy = self.center
        self.max_radius = min(self.cx, self.cy) * 0.9
        
    def generate_mandala(self, 
                        layers: int = 6,
                        symmetry: int = 8,
                        pattern_types: Optional[List[str]] = None,
                        color_scheme: str = "rainbow",
                        complexity: float = 0.7) -> Dict[str, Any]:
        """
        Generate a complete mandala with multiple layers and patterns.
        
        Args:
            layers: Number of concentric layers
            symmetry: Rotational symmetry (number of repetitions)
            pattern_types: List of pattern types to use
            color_scheme: Color scheme name
            complexity: Pattern complexity (0.0 to 1.0)
            
        Returns:
            Dictionary containing mandala data and SVG elements
        """
        if pattern_types is None:
            pattern_types = ["circles", "petals", "geometric", "dots", "lines"]
            
        colors = self._generate_color_palette(color_scheme, layers * 2)
        mandala_elements = []
        
        # Generate layers from outside to inside
        for layer in range(layers):
            radius = self.max_radius * (1 - layer / layers)
            pattern_type = random.choice(pattern_types)
            color = colors[layer % len(colors)]
            
            layer_elements = self._generate_layer(
                radius=radius,
                symmetry=symmetry,
                pattern_type=pattern_type,
                color=color,
                complexity=complexity,
                layer_index=layer
            )
            mandala_elements.extend(layer_elements)
            
        # Add center element
        center_elements = self._generate_center_element(colors[0], symmetry)
        mandala_elements.extend(center_elements)
        
        return {
            "elements": mandala_elements,
            "size": self.size,
            "center": self.center,
            "layers": layers,
            "symmetry": symmetry,
            "colors": colors
        }
    
    def _generate_layer(self, radius: float, symmetry: int, pattern_type: str, 
                       color: str, complexity: float, layer_index: int) -> List[Dict[str, Any]]:
        """Generate elements for a single mandala layer."""
        elements = []
        angle_step = 2 * math.pi / symmetry
        
        if pattern_type == "circles":
            elements.extend(self._create_circle_pattern(radius, symmetry, color, complexity))
        elif pattern_type == "petals":
            elements.extend(self._create_petal_pattern(radius, symmetry, color, complexity))
        elif pattern_type == "geometric":
            elements.extend(self._create_geometric_pattern(radius, symmetry, color, complexity))
        elif pattern_type == "dots":
            elements.extend(self._create_dot_pattern(radius, symmetry, color, complexity))
        elif pattern_type == "lines":
            elements.extend(self._create_line_pattern(radius, symmetry, color, complexity))
        elif pattern_type == "triangles":
            elements.extend(self._create_triangle_pattern(radius, symmetry, color, complexity))
        elif pattern_type == "stars":
            elements.extend(self._create_star_pattern(radius, symmetry, color, complexity))
            
        return elements
    
    def _create_circle_pattern(self, radius: float, symmetry: int, color: str, complexity: float) -> List[Dict[str, Any]]:
        """Create circular patterns around the mandala."""
        elements = []
        angle_step = 2 * math.pi / symmetry
        circle_radius = radius * 0.1 * complexity
        
        for i in range(symmetry):
            angle = i * angle_step
            x = self.cx + radius * math.cos(angle)
            y = self.cy + radius * math.sin(angle)
            
            elements.append({
                "type": "circle",
                "cx": x,
                "cy": y,
                "r": circle_radius,
                "fill": color,
                "stroke": self._darken_color(color),
                "stroke-width": 1
            })
            
            # Add smaller circles for complexity
            if complexity > 0.5:
                for j in range(3):
                    small_angle = angle + (j - 1) * 0.3
                    small_radius = radius * 0.8
                    sx = self.cx + small_radius * math.cos(small_angle)
                    sy = self.cy + small_radius * math.sin(small_angle)
                    
                    elements.append({
                        "type": "circle",
                        "cx": sx,
                        "cy": sy,
                        "r": circle_radius * 0.3,
                        "fill": "none",
                        "stroke": color,
                        "stroke-width": 1
                    })
                    
        return elements
    
    def _create_petal_pattern(self, radius: float, symmetry: int, color: str, complexity: float) -> List[Dict[str, Any]]:
        """Create petal-like patterns using ellipses."""
        elements = []
        angle_step = 2 * math.pi / symmetry
        petal_width = radius * 0.15 * complexity
        petal_height = radius * 0.3 * complexity
        
        for i in range(symmetry):
            angle = i * angle_step
            x = self.cx + radius * 0.7 * math.cos(angle)
            y = self.cy + radius * 0.7 * math.sin(angle)
            
            elements.append({
                "type": "ellipse",
                "cx": x,
                "cy": y,
                "rx": petal_width,
                "ry": petal_height,
                "fill": color,
                "stroke": self._darken_color(color),
                "stroke-width": 1,
                "transform": f"rotate({math.degrees(angle)} {x} {y})"
            })
            
        return elements
    
    def _create_geometric_pattern(self, radius: float, symmetry: int, color: str, complexity: float) -> List[Dict[str, Any]]:
        """Create geometric patterns using polygons."""
        elements = []
        angle_step = 2 * math.pi / symmetry
        
        for i in range(symmetry):
            angle = i * angle_step
            
            # Create triangular or diamond shapes
            points = []
            shape_radius = radius * 0.2 * complexity
            
            for j in range(4):  # Diamond shape
                point_angle = angle + j * math.pi / 2
                px = self.cx + radius * math.cos(angle) + shape_radius * math.cos(point_angle)
                py = self.cy + radius * math.sin(angle) + shape_radius * math.sin(point_angle)
                points.append(f"{px},{py}")
                
            elements.append({
                "type": "polygon",
                "points": " ".join(points),
                "fill": color,
                "stroke": self._darken_color(color),
                "stroke-width": 1,
                "opacity": 0.8
            })
            
        return elements
    
    def _create_dot_pattern(self, radius: float, symmetry: int, color: str, complexity: float) -> List[Dict[str, Any]]:
        """Create dot patterns in concentric arrangements."""
        elements = []
        angle_step = 2 * math.pi / symmetry
        
        # Multiple rings of dots
        rings = int(3 * complexity) + 1
        
        for ring in range(rings):
            ring_radius = radius * (0.8 + ring * 0.1)
            dot_size = (3 - ring) * complexity + 1
            
            for i in range(symmetry * (ring + 1)):
                angle = i * (2 * math.pi / (symmetry * (ring + 1)))
                x = self.cx + ring_radius * math.cos(angle)
                y = self.cy + ring_radius * math.sin(angle)
                
                elements.append({
                    "type": "circle",
                    "cx": x,
                    "cy": y,
                    "r": dot_size,
                    "fill": color,
                    "opacity": 0.7
                })
                
        return elements
    
    def _create_line_pattern(self, radius: float, symmetry: int, color: str, complexity: float) -> List[Dict[str, Any]]:
        """Create radial and curved line patterns."""
        elements = []
        angle_step = 2 * math.pi / symmetry
        
        for i in range(symmetry):
            angle = i * angle_step
            
            # Radial lines
            x1 = self.cx + radius * 0.5 * math.cos(angle)
            y1 = self.cy + radius * 0.5 * math.sin(angle)
            x2 = self.cx + radius * math.cos(angle)
            y2 = self.cy + radius * math.sin(angle)
            
            elements.append({
                "type": "line",
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "stroke": color,
                "stroke-width": 2 * complexity,
                "opacity": 0.8
            })
            
            # Curved connecting lines
            if complexity > 0.5:
                next_angle = (i + 1) * angle_step
                x3 = self.cx + radius * math.cos(next_angle)
                y3 = self.cy + radius * math.sin(next_angle)
                
                # Create curved path
                mid_x = (x2 + x3) / 2
                mid_y = (y2 + y3) / 2
                control_x = self.cx + radius * 1.2 * math.cos(angle + angle_step / 2)
                control_y = self.cy + radius * 1.2 * math.sin(angle + angle_step / 2)
                
                path = f"M {x2} {y2} Q {control_x} {control_y} {x3} {y3}"
                
                elements.append({
                    "type": "path",
                    "d": path,
                    "fill": "none",
                    "stroke": color,
                    "stroke-width": 1,
                    "opacity": 0.6
                })
                
        return elements
    
    def _create_triangle_pattern(self, radius: float, symmetry: int, color: str, complexity: float) -> List[Dict[str, Any]]:
        """Create triangular patterns."""
        elements = []
        angle_step = 2 * math.pi / symmetry
        triangle_size = radius * 0.15 * complexity
        
        for i in range(symmetry):
            angle = i * angle_step
            center_x = self.cx + radius * math.cos(angle)
            center_y = self.cy + radius * math.sin(angle)
            
            # Create equilateral triangle
            points = []
            for j in range(3):
                point_angle = angle + j * 2 * math.pi / 3
                px = center_x + triangle_size * math.cos(point_angle)
                py = center_y + triangle_size * math.sin(point_angle)
                points.append(f"{px},{py}")
                
            elements.append({
                "type": "polygon",
                "points": " ".join(points),
                "fill": color,
                "stroke": self._darken_color(color),
                "stroke-width": 1,
                "opacity": 0.7
            })
            
        return elements
    
    def _create_star_pattern(self, radius: float, symmetry: int, color: str, complexity: float) -> List[Dict[str, Any]]:
        """Create star patterns."""
        elements = []
        angle_step = 2 * math.pi / symmetry
        star_radius = radius * 0.2 * complexity
        
        for i in range(symmetry):
            angle = i * angle_step
            center_x = self.cx + radius * math.cos(angle)
            center_y = self.cy + radius * math.sin(angle)
            
            # Create 5-pointed star
            points = []
            for j in range(10):  # 5 outer + 5 inner points
                point_angle = angle + j * math.pi / 5
                if j % 2 == 0:  # Outer points
                    px = center_x + star_radius * math.cos(point_angle)
                    py = center_y + star_radius * math.sin(point_angle)
                else:  # Inner points
                    px = center_x + star_radius * 0.4 * math.cos(point_angle)
                    py = center_y + star_radius * 0.4 * math.sin(point_angle)
                points.append(f"{px},{py}")
                
            elements.append({
                "type": "polygon",
                "points": " ".join(points),
                "fill": color,
                "stroke": self._darken_color(color),
                "stroke-width": 1,
                "opacity": 0.8
            })
            
        return elements
    
    def _generate_center_element(self, color: str, symmetry: int) -> List[Dict[str, Any]]:
        """Generate the central element of the mandala."""
        elements = []
        
        # Central circle
        elements.append({
            "type": "circle",
            "cx": self.cx,
            "cy": self.cy,
            "r": self.max_radius * 0.1,
            "fill": color,
            "stroke": self._darken_color(color),
            "stroke-width": 2
        })
        
        # Small decorative elements around center
        for i in range(symmetry):
            angle = i * 2 * math.pi / symmetry
            x = self.cx + self.max_radius * 0.05 * math.cos(angle)
            y = self.cy + self.max_radius * 0.05 * math.sin(angle)
            
            elements.append({
                "type": "circle",
                "cx": x,
                "cy": y,
                "r": 2,
                "fill": self._lighten_color(color),
                "opacity": 0.8
            })
            
        return elements
    
    def _generate_color_palette(self, scheme: str, count: int) -> List[str]:
        """Generate a color palette based on the specified scheme."""
        colors = []
        
        if scheme == "rainbow":
            for i in range(count):
                hue = i / count
                rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
                colors.append(f"rgb({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)})")
                
        elif scheme == "warm":
            base_hues = [0, 0.08, 0.17]  # Red, orange, yellow
            for i in range(count):
                hue = base_hues[i % len(base_hues)]
                saturation = 0.7 + (i % 3) * 0.1
                value = 0.8 + (i % 2) * 0.1
                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                colors.append(f"rgb({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)})")
                
        elif scheme == "cool":
            base_hues = [0.5, 0.67, 0.75]  # Cyan, blue, purple
            for i in range(count):
                hue = base_hues[i % len(base_hues)]
                saturation = 0.7 + (i % 3) * 0.1
                value = 0.8 + (i % 2) * 0.1
                rgb = colorsys.hsv_to_rgb(hue, saturation, value)
                colors.append(f"rgb({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)})")
                
        elif scheme == "monochrome":
            base_color = (0.6, 0.8, 0.9)  # Blue base
            for i in range(count):
                intensity = 0.3 + (i / count) * 0.6
                rgb = tuple(c * intensity for c in base_color)
                colors.append(f"rgb({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)})")
                
        elif scheme == "earth":
            earth_colors = ["#8B4513", "#D2691E", "#CD853F", "#DEB887", "#F4A460", "#DAA520"]
            colors = (earth_colors * ((count // len(earth_colors)) + 1))[:count]
            
        else:  # Default to rainbow
            return self._generate_color_palette("rainbow", count)
            
        return colors
    
    def _darken_color(self, color: str, factor: float = 0.7) -> str:
        """Darken a color by the specified factor."""
        if color.startswith("rgb("):
            # Extract RGB values
            rgb_str = color[4:-1]
            r, g, b = map(int, rgb_str.split(","))
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            return f"rgb({r},{g},{b})"
        return color
    
    def _lighten_color(self, color: str, factor: float = 1.3) -> str:
        """Lighten a color by the specified factor."""
        if color.startswith("rgb("):
            # Extract RGB values
            rgb_str = color[4:-1]
            r, g, b = map(int, rgb_str.split(","))
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            return f"rgb({r},{g},{b})"
        return color


def create_preset_mandala(preset: str = "classic") -> Dict[str, Any]:
    """
    Create a mandala using predefined presets.
    
    Args:
        preset: Preset name ("classic", "complex", "simple", "floral", "geometric")
        
    Returns:
        Mandala configuration dictionary
    """
    presets = {
        "classic": {
            "layers": 6,
            "symmetry": 8,
            "pattern_types": ["circles", "petals", "geometric"],
            "color_scheme": "rainbow",
            "complexity": 0.7
        },
        "complex": {
            "layers": 10,
            "symmetry": 12,
            "pattern_types": ["circles", "petals", "geometric", "dots", "lines", "stars"],
            "color_scheme": "cool",
            "complexity": 0.9
        },
        "simple": {
            "layers": 4,
            "symmetry": 6,
            "pattern_types": ["circles", "dots"],
            "color_scheme": "monochrome",
            "complexity": 0.4
        },
        "floral": {
            "layers": 7,
            "symmetry": 8,
            "pattern_types": ["petals", "circles", "dots"],
            "color_scheme": "warm",
            "complexity": 0.8
        },
        "geometric": {
            "layers": 5,
            "symmetry": 6,
            "pattern_types": ["geometric", "triangles", "lines"],
            "color_scheme": "earth",
            "complexity": 0.6
        }
    }
    
    config = presets.get(preset, presets["classic"])
    generator = MandalaGenerator()
    return generator.generate_mandala(**config)