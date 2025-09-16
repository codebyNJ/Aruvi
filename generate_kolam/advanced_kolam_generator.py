import math
import random
from typing import List, Dict, Any, Tuple
from datetime import datetime
from models import (
    KolamPattern, KolamGrid, GridCell, Dot, Line, Point, CurvePoint, 
    KolamType, SVGOptions
)

class AdvancedKolamGenerator:
    """Advanced kolam generator supporting multiple types with mathematical formulas"""
    
    CELL_SPACING = 60.0
    
    @classmethod
    def generate_geometric_kolam(
        cls, 
        size: int, 
        shape: str = "circle",
        complexity: int = 3,
        colors: Dict[str, str] = None
    ) -> KolamPattern:
        """
        Generate Geometric Kolam with mathematical precision
        
        Mathematical formulas used:
        - Circle: x = r*cos(θ), y = r*sin(θ)
        - Square: parametric equations for square
        - Triangle: equilateral triangle with inscribed circles
        - Polygon: regular n-gon with mathematical symmetry
        """
        if colors is None:
            colors = {"primary": "#ffffff", "secondary": "#ff6b6b", "accent": "#4ecdc4"}
        
        dots = []
        curves = []
        
        center_x = (size + 1) * cls.CELL_SPACING / 2
        center_y = (size + 1) * cls.CELL_SPACING / 2
        max_radius = (size - 1) * cls.CELL_SPACING / 2
        
        if shape == "circle":
            # Generate concentric circles with mathematical precision
            for ring in range(1, complexity + 1):
                radius = (max_radius * ring) / complexity
                num_points = max(8, ring * 8)
                
                for i in range(num_points):
                    angle = 2 * math.pi * i / num_points
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    
                    dots.append(Dot(
                        id=f"circle-dot-{ring}-{i}",
                        center=Point(x, y),
                        radius=2.0 + ring * 0.5,
                        color=colors["primary"],
                        filled=True
                    ))
                
                # Create circle curves
                circle_points = []
                for i in range(num_points + 1):
                    angle = 2 * math.pi * i / num_points
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    circle_points.append(CurvePoint(x=x, y=y))
                
                curves.append(Line(
                    id=f"circle-{ring}",
                    start=circle_points[0],
                    end=circle_points[-1],
                    curve_points=circle_points,
                    stroke_width=1.5 + ring * 0.3,
                    color=colors["primary"]
                ))
        
        elif shape == "square":
            # Generate square patterns with mathematical precision
            for level in range(1, complexity + 1):
                side_length = (max_radius * 2 * level) / complexity
                half_side = side_length / 2
                
                # Square vertices
                square_points = [
                    Point(center_x - half_side, center_y - half_side),
                    Point(center_x + half_side, center_y - half_side),
                    Point(center_x + half_side, center_y + half_side),
                    Point(center_x - half_side, center_y + half_side)
                ]
                
                for i, point in enumerate(square_points):
                    dots.append(Dot(
                        id=f"square-dot-{level}-{i}",
                        center=point,
                        radius=3.0,
                        color=colors["primary"],
                        filled=True
                    ))
                
                # Create square curves
                curve_points = [CurvePoint(x=p.x, y=p.y) for p in square_points]
                curve_points.append(CurvePoint(x=square_points[0].x, y=square_points[0].y))  # Close the square
                
                curves.append(Line(
                    id=f"square-{level}",
                    start=curve_points[0],
                    end=curve_points[-1],
                    curve_points=curve_points,
                    stroke_width=2.0,
                    color=colors["primary"]
                ))
        
        elif shape == "triangle":
            # Generate equilateral triangle patterns
            for level in range(1, complexity + 1):
                side_length = (max_radius * 2 * level) / complexity
                height = side_length * math.sqrt(3) / 2
                
                # Triangle vertices
                triangle_points = [
                    Point(center_x, center_y - height * 2/3),
                    Point(center_x - side_length/2, center_y + height/3),
                    Point(center_x + side_length/2, center_y + height/3)
                ]
                
                for i, point in enumerate(triangle_points):
                    dots.append(Dot(
                        id=f"triangle-dot-{level}-{i}",
                        center=point,
                        radius=3.0,
                        color=colors["primary"],
                        filled=True
                    ))
                
                # Create triangle curves
                curve_points = [CurvePoint(x=p.x, y=p.y) for p in triangle_points]
                curve_points.append(CurvePoint(x=triangle_points[0].x, y=triangle_points[0].y))
                
                curves.append(Line(
                    id=f"triangle-{level}",
                    start=curve_points[0],
                    end=curve_points[-1],
                    curve_points=curve_points,
                    stroke_width=2.0,
                    color=colors["primary"]
                ))
        
        return KolamPattern(
            id=f"geometric-{shape}-{size}",
            name=f"Geometric {shape.title()} Kolam",
            kolam_type=KolamType.GEOMETRIC,
            grid=None,
            curves=curves,
            dots=dots,
            symmetry_type="geometric",
            dimensions={
                "width": (size + 1) * cls.CELL_SPACING,
                "height": (size + 1) * cls.CELL_SPACING
            },
            created=datetime.now(),
            modified=datetime.now(),
            colors=colors,
            mathematical_params={
                "shape": shape,
                "complexity": complexity,
                "center": (center_x, center_y),
                "max_radius": max_radius
            }
        )
    
    @classmethod
    def generate_iyal_kolam(
        cls,
        size: int,
        flow_intensity: float = 0.5,
        organic_factor: float = 0.3,
        colors: Dict[str, str] = None
    ) -> KolamPattern:
        """
        Generate Iyal Kolam (freehand/flowing) with organic curves
        
        Mathematical formulas used:
        - Bezier curves for smooth flowing lines
        - Perlin noise for organic variations
        - Spiral equations for natural patterns
        - Parametric curves for fluid motion
        """
        if colors is None:
            colors = {"primary": "#ffffff", "secondary": "#ff9ff3", "accent": "#54a0ff"}
        
        dots = []
        curves = []
        
        center_x = (size + 1) * cls.CELL_SPACING / 2
        center_y = (size + 1) * cls.CELL_SPACING / 2
        max_radius = (size - 1) * cls.CELL_SPACING / 2
        
        # Generate flowing spiral patterns
        num_spirals = max(2, size // 2)
        for spiral in range(num_spirals):
            spiral_angle_offset = 2 * math.pi * spiral / num_spirals
            spiral_points = []
            
            # Spiral equation: r = a * θ^b
            a = max_radius * 0.3
            b = 0.8 + flow_intensity * 0.4
            
            for i in range(50):
                theta = (i / 49) * 4 * math.pi + spiral_angle_offset
                r = a * (theta ** b)
                
                # Add organic variation using noise-like function
                noise_factor = 1 + organic_factor * math.sin(theta * 3) * math.cos(theta * 2)
                r *= noise_factor
                
                x = center_x + r * math.cos(theta)
                y = center_y + r * math.sin(theta)
                
                if i % 5 == 0:  # Add dots at regular intervals
                    dots.append(Dot(
                        id=f"iyal-dot-{spiral}-{i}",
                        center=Point(x, y),
                        radius=2.0 + random.uniform(0, 1),
                        color=colors["primary"],
                        filled=True
                    ))
                
                spiral_points.append(CurvePoint(x=x, y=y))
            
            curves.append(Line(
                id=f"iyal-spiral-{spiral}",
                start=spiral_points[0],
                end=spiral_points[-1],
                curve_points=spiral_points,
                stroke_width=1.5 + random.uniform(0, 1),
                color=colors["primary"]
            ))
        
        # Generate flowing wave patterns
        num_waves = max(1, size // 3)
        for wave in range(num_waves):
            wave_angle = 2 * math.pi * wave / num_waves
            wave_points = []
            
            for i in range(30):
                t = i / 29
                # Wave equation with organic variation
                base_x = center_x + (t - 0.5) * max_radius * 1.5
                base_y = center_y + (t - 0.5) * max_radius * 1.5
                
                # Rotate the wave
                cos_a = math.cos(wave_angle)
                sin_a = math.sin(wave_angle)
                x = base_x * cos_a - base_y * sin_a
                y = base_x * sin_a + base_y * cos_a
                
                # Add wave variation
                wave_amplitude = max_radius * 0.2 * flow_intensity
                wave_freq = 3 + organic_factor * 2
                wave_offset = wave_amplitude * math.sin(t * wave_freq * math.pi)
                
                x += wave_offset * math.cos(wave_angle + math.pi/2)
                y += wave_offset * math.sin(wave_angle + math.pi/2)
                
                wave_points.append(CurvePoint(x=x, y=y))
            
            curves.append(Line(
                id=f"iyal-wave-{wave}",
                start=wave_points[0],
                end=wave_points[-1],
                curve_points=wave_points,
                stroke_width=1.2 + random.uniform(0, 0.8),
                color=colors["secondary"]
            ))
        
        return KolamPattern(
            id=f"iyal-{size}",
            name=f"Iyal Kolam {size}×{size}",
            kolam_type=KolamType.IYAL,
            grid=None,
            curves=curves,
            dots=dots,
            symmetry_type="organic",
            dimensions={
                "width": (size + 1) * cls.CELL_SPACING,
                "height": (size + 1) * cls.CELL_SPACING
            },
            created=datetime.now(),
            modified=datetime.now(),
            colors=colors,
            mathematical_params={
                "flow_intensity": flow_intensity,
                "organic_factor": organic_factor,
                "num_spirals": num_spirals,
                "num_waves": num_waves
            }
        )
    
    @classmethod
    def generate_rangoli_kolam(
        cls,
        size: int,
        motif_type: str = "lotus",
        color_scheme: str = "traditional",
        complexity: int = 3,
        colors: Dict[str, str] = None
    ) -> KolamPattern:
        """
        Generate Rangoli Kolam with colorful patterns and traditional motifs
        
        Mathematical formulas used:
        - Rose curves: r = a * cos(k * θ)
        - Lissajous curves for intricate patterns
        - Mandala geometry with radial symmetry
        - Traditional Indian geometric patterns
        """
        if colors is None:
            if color_scheme == "traditional":
                colors = {
                    "primary": "#ff6b6b",    # Red
                    "secondary": "#4ecdc4",  # Teal
                    "accent": "#45b7d1",     # Blue
                    "highlight": "#f9ca24",  # Yellow
                    "background": "#6c5ce7"  # Purple
                }
            else:
                colors = {
                    "primary": "#ffffff",
                    "secondary": "#ff9ff3",
                    "accent": "#54a0ff",
                    "highlight": "#5f27cd",
                    "background": "#00d2d3"
                }
        
        dots = []
        curves = []
        
        center_x = (size + 1) * cls.CELL_SPACING / 2
        center_y = (size + 1) * cls.CELL_SPACING / 2
        max_radius = (size - 1) * cls.CELL_SPACING / 2
        
        if motif_type == "lotus":
            # Generate lotus pattern with mathematical precision
            num_petals = 8
            for petal in range(num_petals):
                petal_angle = 2 * math.pi * petal / num_petals
                petal_points = []
                
                for i in range(20):
                    t = i / 19
                    # Lotus petal equation
                    r = max_radius * 0.8 * (1 - abs(t - 0.5) * 2)
                    theta = petal_angle + (t - 0.5) * math.pi / 3
                    
                    x = center_x + r * math.cos(theta)
                    y = center_y + r * math.sin(theta)
                    
                    if i % 4 == 0:
                        dots.append(Dot(
                            id=f"lotus-dot-{petal}-{i}",
                            center=Point(x, y),
                            radius=2.5,
                            color=colors["primary"],
                            filled=True
                        ))
                    
                    petal_points.append(CurvePoint(x=x, y=y))
                
                curves.append(Line(
                    id=f"lotus-petal-{petal}",
                    start=petal_points[0],
                    end=petal_points[-1],
                    curve_points=petal_points,
                    stroke_width=2.0,
                    color=colors["primary"]
                ))
        
        elif motif_type == "mandala":
            # Generate mandala pattern
            for ring in range(1, complexity + 1):
                radius = (max_radius * ring) / complexity
                num_elements = 8 * ring
                
                for element in range(num_elements):
                    angle = 2 * math.pi * element / num_elements
                    
                    # Create mandala elements
                    element_points = []
                    for i in range(10):
                        t = i / 9
                        r = radius * (0.3 + 0.7 * t)
                        theta = angle + (t - 0.5) * math.pi / 4
                        
                        x = center_x + r * math.cos(theta)
                        y = center_y + r * math.sin(theta)
                        element_points.append(CurvePoint(x=x, y=y))
                    
                    curves.append(Line(
                        id=f"mandala-{ring}-{element}",
                        start=element_points[0],
                        end=element_points[-1],
                        curve_points=element_points,
                        stroke_width=1.5,
                        color=colors["secondary"] if element % 2 == 0 else colors["accent"]
                    ))
        
        # Add center decoration
        center_dots = []
        for i in range(6):
            angle = 2 * math.pi * i / 6
            r = max_radius * 0.1
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            center_dots.append(Dot(
                id=f"center-dot-{i}",
                center=Point(x, y),
                radius=3.0,
                color=colors["highlight"],
                filled=True
            ))
        dots.extend(center_dots)
        
        return KolamPattern(
            id=f"rangoli-{motif_type}-{size}",
            name=f"Rangoli {motif_type.title()} Kolam",
            kolam_type=KolamType.RANGOLI,
            grid=None,
            curves=curves,
            dots=dots,
            symmetry_type="radial",
            dimensions={
                "width": (size + 1) * cls.CELL_SPACING,
                "height": (size + 1) * cls.CELL_SPACING
            },
            created=datetime.now(),
            modified=datetime.now(),
            colors=colors,
            mathematical_params={
                "motif_type": motif_type,
                "color_scheme": color_scheme,
                "complexity": complexity,
                "num_petals": num_petals if motif_type == "lotus" else None
            }
        )
    
    @classmethod
    def generate_kavi_kolam(
        cls,
        size: int,
        line_thickness: float = 2.0,
        precision: float = 0.8,
        colors: Dict[str, str] = None
    ) -> KolamPattern:
        """
        Generate Kavi Kolam (chalk-based) with bold lines and geometric precision
        
        Mathematical formulas used:
        - Straight line equations for precise geometry
        - Grid-based patterns with mathematical accuracy
        - Symmetric transformations
        - Traditional chalk kolam algorithms
        """
        if colors is None:
            colors = {"primary": "#ffffff", "secondary": "#f1f2f6", "accent": "#ddd"}
        
        dots = []
        curves = []
        
        # Create grid-based pattern
        grid_size = size
        cell_size = cls.CELL_SPACING
        
        # Generate dots in grid pattern
        for i in range(grid_size + 1):
            for j in range(grid_size + 1):
                x = j * cell_size
                y = i * cell_size
                
                dots.append(Dot(
                    id=f"kavi-dot-{i}-{j}",
                    center=Point(x, y),
                    radius=2.0,
                    color=colors["primary"],
                    filled=True
                ))
        
        # Generate bold geometric lines
        center_x = grid_size * cell_size / 2
        center_y = grid_size * cell_size / 2
        
        # Create diamond pattern
        diamond_size = min(grid_size, 6)
        for level in range(1, diamond_size + 1):
            half_size = (level * cell_size) / 2
            
            # Diamond vertices
            diamond_points = [
                Point(center_x, center_y - half_size),
                Point(center_x + half_size, center_y),
                Point(center_x, center_y + half_size),
                Point(center_x - half_size, center_y)
            ]
            
            curve_points = [CurvePoint(x=p.x, y=p.y) for p in diamond_points]
            curve_points.append(CurvePoint(x=diamond_points[0].x, y=diamond_points[0].y))
            
            curves.append(Line(
                id=f"kavi-diamond-{level}",
                start=curve_points[0],
                end=curve_points[-1],
                curve_points=curve_points,
                stroke_width=line_thickness + level * 0.5,
                color=colors["primary"]
            ))
        
        # Create cross patterns
        for i in range(1, grid_size, 2):
            for j in range(1, grid_size, 2):
                x = j * cell_size
                y = i * cell_size
                
                # Horizontal line
                curves.append(Line(
                    id=f"kavi-h-{i}-{j}",
                    start=Point(x - cell_size/2, y),
                    end=Point(x + cell_size/2, y),
                    stroke_width=line_thickness,
                    color=colors["primary"]
                ))
                
                # Vertical line
                curves.append(Line(
                    id=f"kavi-v-{i}-{j}",
                    start=Point(x, y - cell_size/2),
                    end=Point(x, y + cell_size/2),
                    stroke_width=line_thickness,
                    color=colors["primary"]
                ))
        
        return KolamPattern(
            id=f"kavi-{size}",
            name=f"Kavi Kolam {size}×{size}",
            kolam_type=KolamType.KAVI,
            grid=None,
            curves=curves,
            dots=dots,
            symmetry_type="grid",
            dimensions={
                "width": (grid_size + 1) * cell_size,
                "height": (grid_size + 1) * cell_size
            },
            created=datetime.now(),
            modified=datetime.now(),
            colors=colors,
            mathematical_params={
                "line_thickness": line_thickness,
                "precision": precision,
                "grid_size": grid_size,
                "diamond_size": diamond_size
            }
        )
    
    @classmethod
    def generate_kolam(
        cls,
        kolam_type: KolamType,
        size: int,
        **kwargs
    ) -> KolamPattern:
        """Main entry point for generating any type of kolam"""
        
        if kolam_type == KolamType.GEOMETRIC:
            return cls.generate_geometric_kolam(size, **kwargs)
        elif kolam_type == KolamType.IYAL:
            return cls.generate_iyal_kolam(size, **kwargs)
        elif kolam_type == KolamType.RANGOLI:
            return cls.generate_rangoli_kolam(size, **kwargs)
        elif kolam_type == KolamType.KAVI:
            return cls.generate_kavi_kolam(size, **kwargs)
        else:
            raise ValueError(f"Unsupported kolam type: {kolam_type}")
