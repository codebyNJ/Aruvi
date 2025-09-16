from typing import List, Optional
from models import KolamPattern, SVGOptions, CurvePoint

def generate_svg_path(curve_points: Optional[List[CurvePoint]]) -> str:
    """Generate SVG path string from curve points using quadratic Bezier curves"""
    if not curve_points or len(curve_points) == 0:
        return ""
    
    path = f"M {curve_points[0].x} {curve_points[0].y}"
    
    for i in range(1, len(curve_points)):
        point = curve_points[i]
        prev_point = curve_points[i - 1]
        
        # Use quadratic Bezier curves for smooth lines
        if point.control_x is not None and point.control_y is not None:
            path += f" Q {point.control_x} {point.control_y} {point.x} {point.y}"
        else:
            # Create smooth curves using the midpoint as control
            control_x = (prev_point.x + point.x) / 2
            control_y = (prev_point.y + point.y) / 2
            path += f" Q {control_x} {control_y} {point.x} {point.y}"
    
    return path

def generate_kolam_svg(pattern: KolamPattern, options: Optional[SVGOptions] = None) -> str:
    """Generate SVG content from kolam pattern"""
    if options is None:
        options = SVGOptions()
    
    background = options.background or "#fef3c7"
    brush = options.brush or "#92400e"
    padding = options.padding or 40.0
    
    dimensions = pattern.dimensions
    dots = pattern.dots
    curves = pattern.curves
    
    # Generate SVG content
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{dimensions['width']}" height="{dimensions['height']}" viewBox="0 0 {dimensions['width']} {dimensions['height']}" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; background-color: {background};">
\t<defs>
\t\t<style>
\t\t\t.kolam-curve {{
\t\t\t\tfill: none;
\t\t\t\tstroke: {brush};
\t\t\t\tstroke-width: 3;
\t\t\t\tstroke-linecap: round;
\t\t\t\tstroke-linejoin: round;
\t\t\t}}
\t\t\t.kolam-dot {{
\t\t\t\tfill: {brush};
\t\t\t}}
\t\t</style>
\t</defs>'''
    
    # Add dots
    for dot in dots:
        svg_content += f'''
\t\t<circle class="kolam-dot"
\t\t\tcx="{dot.center.x}" 
\t\t\tcy="{dot.center.y}" 
\t\t\tr="{dot.radius or 3}" 
\t\t\tfill="{brush}" 
\t\t\tstroke="{brush}" 
\t\t\tstroke-width="1"/>'''
    
    # Add curves
    for curve in curves:
        if curve.curve_points and len(curve.curve_points) > 1:
            # Render as smooth SVG path
            path_data = generate_svg_path(curve.curve_points)
            svg_content += f'''
\t\t<path class="kolam-curve" d="{path_data}"/>'''
        else:
            # Handle simple lines (fallback)
            svg_content += f'''
\t\t<line class="kolam-curve" x1="{curve.start.x}" y1="{curve.start.y}" x2="{curve.end.x}" y2="{curve.end.y}"/>'''
    
    svg_content += '''
</svg>'''
    
    return svg_content
