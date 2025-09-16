from typing import Dict, Any, List
import xml.etree.ElementTree as ET


class MandalaSVGGenerator:
    """
    Converts mandala data structures into SVG format.
    Handles all geometric elements and styling for beautiful mandala output.
    """
    
    def __init__(self):
        self.svg_namespace = "http://www.w3.org/2000/svg"
        
    def generate_svg(self, mandala_data: Dict[str, Any]) -> str:
        """
        Generate SVG string from mandala data.
        
        Args:
            mandala_data: Dictionary containing mandala elements and metadata
            
        Returns:
            Complete SVG markup as string
        """
        size = mandala_data["size"]
        elements = mandala_data["elements"]
        
        # Create root SVG element
        svg = ET.Element("svg")
        svg.set("width", str(size))
        svg.set("height", str(size))
        svg.set("xmlns", self.svg_namespace)
        svg.set("viewBox", f"0 0 {size} {size}")
        
        # Add background
        background = ET.SubElement(svg, "rect")
        background.set("width", str(size))
        background.set("height", str(size))
        background.set("fill", "#000011")  # Dark background for contrast
        
        # Add gradient definitions
        defs = ET.SubElement(svg, "defs")
        self._add_gradients(defs)
        
        # Add all mandala elements
        for element in elements:
            self._add_element(svg, element)
            
        # Convert to string
        return self._prettify_xml(svg)
    
    def _add_element(self, parent: ET.Element, element_data: Dict[str, Any]) -> None:
        """Add a single element to the SVG."""
        element_type = element_data["type"]
        
        if element_type == "circle":
            self._add_circle(parent, element_data)
        elif element_type == "ellipse":
            self._add_ellipse(parent, element_data)
        elif element_type == "polygon":
            self._add_polygon(parent, element_data)
        elif element_type == "line":
            self._add_line(parent, element_data)
        elif element_type == "path":
            self._add_path(parent, element_data)
    
    def _add_circle(self, parent: ET.Element, data: Dict[str, Any]) -> None:
        """Add a circle element."""
        circle = ET.SubElement(parent, "circle")
        circle.set("cx", str(data["cx"]))
        circle.set("cy", str(data["cy"]))
        circle.set("r", str(data["r"]))
        
        self._apply_styling(circle, data)
    
    def _add_ellipse(self, parent: ET.Element, data: Dict[str, Any]) -> None:
        """Add an ellipse element."""
        ellipse = ET.SubElement(parent, "ellipse")
        ellipse.set("cx", str(data["cx"]))
        ellipse.set("cy", str(data["cy"]))
        ellipse.set("rx", str(data["rx"]))
        ellipse.set("ry", str(data["ry"]))
        
        self._apply_styling(ellipse, data)
    
    def _add_polygon(self, parent: ET.Element, data: Dict[str, Any]) -> None:
        """Add a polygon element."""
        polygon = ET.SubElement(parent, "polygon")
        polygon.set("points", data["points"])
        
        self._apply_styling(polygon, data)
    
    def _add_line(self, parent: ET.Element, data: Dict[str, Any]) -> None:
        """Add a line element."""
        line = ET.SubElement(parent, "line")
        line.set("x1", str(data["x1"]))
        line.set("y1", str(data["y1"]))
        line.set("x2", str(data["x2"]))
        line.set("y2", str(data["y2"]))
        
        self._apply_styling(line, data)
    
    def _add_path(self, parent: ET.Element, data: Dict[str, Any]) -> None:
        """Add a path element."""
        path = ET.SubElement(parent, "path")
        path.set("d", data["d"])
        
        self._apply_styling(path, data)
    
    def _apply_styling(self, element: ET.Element, data: Dict[str, Any]) -> None:
        """Apply styling attributes to an element."""
        # Standard attributes
        if "fill" in data:
            element.set("fill", data["fill"])
        if "stroke" in data:
            element.set("stroke", data["stroke"])
        if "stroke-width" in data:
            element.set("stroke-width", str(data["stroke-width"]))
        if "opacity" in data:
            element.set("opacity", str(data["opacity"]))
        if "transform" in data:
            element.set("transform", data["transform"])
            
        # Add glow effect for enhanced beauty
        if data.get("fill") and data["fill"] != "none":
            element.set("filter", "url(#glow)")
    
    def _add_gradients(self, defs: ET.Element) -> None:
        """Add gradient definitions for enhanced visual effects."""
        # Radial gradient for glow effects
        radial_grad = ET.SubElement(defs, "radialGradient")
        radial_grad.set("id", "radialGlow")
        
        stop1 = ET.SubElement(radial_grad, "stop")
        stop1.set("offset", "0%")
        stop1.set("stop-color", "#ffffff")
        stop1.set("stop-opacity", "0.8")
        
        stop2 = ET.SubElement(radial_grad, "stop")
        stop2.set("offset", "100%")
        stop2.set("stop-color", "#ffffff")
        stop2.set("stop-opacity", "0")
        
        # Glow filter
        filter_elem = ET.SubElement(defs, "filter")
        filter_elem.set("id", "glow")
        filter_elem.set("x", "-50%")
        filter_elem.set("y", "-50%")
        filter_elem.set("width", "200%")
        filter_elem.set("height", "200%")
        
        gaussian_blur = ET.SubElement(filter_elem, "feGaussianBlur")
        gaussian_blur.set("stdDeviation", "2")
        gaussian_blur.set("result", "coloredBlur")
        
        merge = ET.SubElement(filter_elem, "feMerge")
        merge_node1 = ET.SubElement(merge, "feMergeNode")
        merge_node1.set("in", "coloredBlur")
        merge_node2 = ET.SubElement(merge, "feMergeNode")
        merge_node2.set("in", "SourceGraphic")
    
    def _prettify_xml(self, element: ET.Element) -> str:
        """Convert XML element to pretty-printed string."""
        from xml.dom import minidom
        
        rough_string = ET.tostring(element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


def save_mandala_svg(mandala_data: Dict[str, Any], filename: str) -> None:
    """
    Save mandala data as SVG file.
    
    Args:
        mandala_data: Dictionary containing mandala elements
        filename: Output filename (should end with .svg)
    """
    generator = MandalaSVGGenerator()
    svg_content = generator.generate_svg(mandala_data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_content)


def mandala_to_svg_string(mandala_data: Dict[str, Any]) -> str:
    """
    Convert mandala data to SVG string.
    
    Args:
        mandala_data: Dictionary containing mandala elements
        
    Returns:
        SVG markup as string
    """
    generator = MandalaSVGGenerator()
    return generator.generate_svg(mandala_data)
