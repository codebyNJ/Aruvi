from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from typing import Optional, Dict, Any
import uvicorn

from kolam_generator import KolamGenerator
from advanced_kolam_generator import AdvancedKolamGenerator
from svg_generator import generate_kolam_svg
from models import KolamType

app = FastAPI(
    title="Zen Kolam API",
    description="A comprehensive API for generating various types of South Indian kolam patterns as SVG images with mathematical precision",
    version="2.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Zen Kolam API v2.0",
        "description": "Generate various types of South Indian kolam patterns as SVG images with mathematical precision",
        "supported_types": {
            "geometric": "Mathematical geometric patterns (circles, squares, triangles)",
            "iyal": "Freehand flowing patterns with organic curves",
            "rangoli": "Colorful traditional motifs (lotus, mandala)",
            "kavi": "Chalk-based bold geometric patterns",
            "traditional_1d": "Classic 1D symmetric patterns"
        },
        "endpoints": {
            "kolam": "/api/kolam - Generate any type of kolam pattern as SVG",
            "geometric": "/api/kolam/geometric - Generate geometric kolam",
            "iyal": "/api/kolam/iyal - Generate iyal kolam",
            "rangoli": "/api/kolam/rangoli - Generate rangoli kolam",
            "kavi": "/api/kolam/kavi - Generate kavi kolam",
            "docs": "/docs - API documentation"
        }
    }

@app.get("/api/kolam")
async def generate_kolam(
    kolam_type: str = Query("traditional_1d", description="Type of kolam to generate"),
    size: int = Query(7, ge=3, le=15, description="Grid size for the kolam pattern (3-15)"),
    background: str = Query("#7b3306", description="Background color in hex format"),
    brush: str = Query("#ffffff", description="Pattern color in hex format"),
    **kwargs
):
    """
    Generate any type of kolam pattern as a static SVG image with customizable colors.
    
    - **kolam_type**: Type of kolam (geometric, iyal, rangoli, kavi, traditional_1d)
    - **size**: Grid size for the kolam pattern (creates an n×n grid, range: 3-15)
    - **background**: Background color of the SVG (hex color code)
    - **brush**: Color of the kolam lines and dots (hex color code)
    
    Returns an SVG image with Content-Type: image/svg+xml
    """
    try:
        # Parse kolam type
        try:
            kolam_type_enum = KolamType(kolam_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid kolam type. Supported types: {[t.value for t in KolamType]}"
            )
        
        # Generate the kolam pattern
        if kolam_type_enum == KolamType.TRADITIONAL_1D:
            pattern = KolamGenerator.generate_kolam_1d(size)
        else:
            pattern = AdvancedKolamGenerator.generate_kolam(kolam_type_enum, size, **kwargs)
        
        # Generate SVG using the utility function
        from models import SVGOptions
        svg_content = generate_kolam_svg(pattern, SVGOptions(
            background=background,
            brush=brush,
        ))
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={
                "Cache-Control": "public, max-age=3600",
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate kolam pattern: {str(e)}"
        )

@app.get("/api/kolam/geometric")
async def generate_geometric_kolam(
    size: int = Query(7, ge=3, le=15, description="Grid size for the kolam pattern (3-15)"),
    shape: str = Query("circle", description="Geometric shape (circle, square, triangle)"),
    complexity: int = Query(3, ge=1, le=5, description="Complexity level (1-5)"),
    background: str = Query("#7b3306", description="Background color in hex format"),
    brush: str = Query("#ffffff", description="Pattern color in hex format")
):
    """
    Generate Geometric Kolam with mathematical precision.
    
    Mathematical formulas used:
    - Circle: x = r*cos(θ), y = r*sin(θ)
    - Square: parametric equations for square
    - Triangle: equilateral triangle with inscribed circles
    """
    try:
        pattern = AdvancedKolamGenerator.generate_geometric_kolam(
            size=size,
            shape=shape,
            complexity=complexity,
            colors={"primary": brush, "secondary": brush, "accent": brush}
        )
        
        from models import SVGOptions
        svg_content = generate_kolam_svg(pattern, SVGOptions(
            background=background,
            brush=brush,
        ))
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=3600"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate geometric kolam: {str(e)}")

@app.get("/api/kolam/iyal")
async def generate_iyal_kolam(
    size: int = Query(7, ge=3, le=15, description="Grid size for the kolam pattern (3-15)"),
    flow_intensity: float = Query(0.5, ge=0.1, le=1.0, description="Flow intensity (0.1-1.0)"),
    organic_factor: float = Query(0.3, ge=0.0, le=1.0, description="Organic variation factor (0.0-1.0)"),
    background: str = Query("#7b3306", description="Background color in hex format"),
    brush: str = Query("#ffffff", description="Pattern color in hex format")
):
    """
    Generate Iyal Kolam (freehand/flowing) with organic curves.
    
    Mathematical formulas used:
    - Bezier curves for smooth flowing lines
    - Spiral equations: r = a * θ^b
    - Wave equations with organic variations
    """
    try:
        pattern = AdvancedKolamGenerator.generate_iyal_kolam(
            size=size,
            flow_intensity=flow_intensity,
            organic_factor=organic_factor,
            colors={"primary": brush, "secondary": brush, "accent": brush}
        )
        
        from models import SVGOptions
        svg_content = generate_kolam_svg(pattern, SVGOptions(
            background=background,
            brush=brush,
        ))
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=3600"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate iyal kolam: {str(e)}")

@app.get("/api/kolam/rangoli")
async def generate_rangoli_kolam(
    size: int = Query(7, ge=3, le=15, description="Grid size for the kolam pattern (3-15)"),
    motif_type: str = Query("lotus", description="Motif type (lotus, mandala)"),
    color_scheme: str = Query("traditional", description="Color scheme (traditional, modern)"),
    complexity: int = Query(3, ge=1, le=5, description="Complexity level (1-5)"),
    background: str = Query("#7b3306", description="Background color in hex format"),
    brush: str = Query("#ffffff", description="Pattern color in hex format")
):
    """
    Generate Rangoli Kolam with colorful patterns and traditional motifs.
    
    Mathematical formulas used:
    - Rose curves: r = a * cos(k * θ)
    - Lissajous curves for intricate patterns
    - Mandala geometry with radial symmetry
    """
    try:
        pattern = AdvancedKolamGenerator.generate_rangoli_kolam(
            size=size,
            motif_type=motif_type,
            color_scheme=color_scheme,
            complexity=complexity,
            colors={"primary": brush, "secondary": brush, "accent": brush}
        )
        
        from models import SVGOptions
        svg_content = generate_kolam_svg(pattern, SVGOptions(
            background=background,
            brush=brush,
        ))
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=3600"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate rangoli kolam: {str(e)}")

@app.get("/api/kolam/kavi")
async def generate_kavi_kolam(
    size: int = Query(7, ge=3, le=15, description="Grid size for the kolam pattern (3-15)"),
    line_thickness: float = Query(2.0, ge=0.5, le=5.0, description="Line thickness (0.5-5.0)"),
    precision: float = Query(0.8, ge=0.1, le=1.0, description="Precision level (0.1-1.0)"),
    background: str = Query("#7b3306", description="Background color in hex format"),
    brush: str = Query("#ffffff", description="Pattern color in hex format")
):
    """
    Generate Kavi Kolam (chalk-based) with bold lines and geometric precision.
    
    Mathematical formulas used:
    - Straight line equations for precise geometry
    - Grid-based patterns with mathematical accuracy
    - Symmetric transformations
    """
    try:
        pattern = AdvancedKolamGenerator.generate_kavi_kolam(
            size=size,
            line_thickness=line_thickness,
            precision=precision,
            colors={"primary": brush, "secondary": brush, "accent": brush}
        )
        
        from models import SVGOptions
        svg_content = generate_kolam_svg(pattern, SVGOptions(
            background=background,
            brush=brush,
        ))
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=3600"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate kavi kolam: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
