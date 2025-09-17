from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn

from mandala_generator import MandalaGenerator, create_preset_mandala
from svg_generator import mandala_to_svg_string

app = FastAPI(
    title="Mandala Art Generator API",
    description="Generate beautiful mandala art patterns as SVG images with customizable parameters",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Mandala Art Generator API v1.0",
        "description": "Generate beautiful mandala patterns with mathematical precision",
        "endpoints": {
            "generate": "/api/mandala - Generate custom mandala patterns",
            "preset": "/api/mandala/preset - Generate preset mandala patterns",
            "docs": "/docs - Interactive API documentation"
        },
        "features": [
            "Customizable layers and symmetry",
            "Multiple pattern types (circles, petals, geometric, etc.)",
            "Various color schemes",
            "SVG vector output",
            "Preset configurations"
        ]
    }

@app.get("/api/mandala", 
         summary="Generate Custom Mandala",
         description="Generate a mandala with custom parameters")
async def generate_mandala(
    size: int = Query(800, ge=200, le=2000, description="Canvas size (width and height)"),
    layers: int = Query(6, ge=1, le=15, description="Number of concentric layers"),
    symmetry: int = Query(8, ge=3, le=24, description="Rotational symmetry (number of repetitions)"),
    pattern_types: Optional[str] = Query(None, description="Comma-separated pattern types: circles,petals,geometric,dots,lines,triangles,stars"),
    color_scheme: str = Query("rainbow", description="Color scheme: rainbow,warm,cool,monochrome,earth"),
    complexity: float = Query(0.7, ge=0.1, le=1.0, description="Pattern complexity (0.1 to 1.0)")
):
    """Generate a custom mandala with specified parameters."""
    try:
        # Parse pattern types
        if pattern_types:
            pattern_list = [p.strip() for p in pattern_types.split(",")]
            # Validate pattern types
            valid_patterns = {"circles", "petals", "geometric", "dots", "lines", "triangles", "stars"}
            pattern_list = [p for p in pattern_list if p in valid_patterns]
            if not pattern_list:
                pattern_list = None
        else:
            pattern_list = None
        
        # Generate mandala
        generator = MandalaGenerator(size=size)
        mandala_data = generator.generate_mandala(
            layers=layers,
            symmetry=symmetry,
            pattern_types=pattern_list,
            color_scheme=color_scheme,
            complexity=complexity
        )
        
        # Convert to SVG
        svg_content = mandala_to_svg_string(mandala_data)
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={
                "Content-Disposition": f"inline; filename=mandala_{layers}l_{symmetry}s.svg"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mandala: {str(e)}")

@app.get("/api/mandala/preset/{preset_name}",
         summary="Generate Preset Mandala",
         description="Generate a mandala using predefined presets")
async def generate_preset_mandala(
    preset_name: str = Path(..., description="Preset name: classic,complex,simple,floral,geometric"),
    size: int = Query(800, ge=200, le=2000, description="Canvas size (width and height)")
):
    """Generate a mandala using predefined presets."""
    try:
        valid_presets = {"classic", "complex", "simple", "floral", "geometric"}
        if preset_name not in valid_presets:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid preset. Valid presets: {', '.join(valid_presets)}"
            )
        
        # Generate preset mandala
        mandala_data = create_preset_mandala(preset_name)
        
        # Update size if different from default
        if size != 800:
            generator = MandalaGenerator(size=size)
            preset_configs = {
                "classic": {"layers": 6, "symmetry": 8, "pattern_types": ["circles", "petals", "geometric"], "color_scheme": "rainbow", "complexity": 0.7},
                "complex": {"layers": 10, "symmetry": 12, "pattern_types": ["circles", "petals", "geometric", "dots", "lines", "stars"], "color_scheme": "cool", "complexity": 0.9},
                "simple": {"layers": 4, "symmetry": 6, "pattern_types": ["circles", "dots"], "color_scheme": "monochrome", "complexity": 0.4},
                "floral": {"layers": 7, "symmetry": 8, "pattern_types": ["petals", "circles", "dots"], "color_scheme": "warm", "complexity": 0.8},
                "geometric": {"layers": 5, "symmetry": 6, "pattern_types": ["geometric", "triangles", "lines"], "color_scheme": "earth", "complexity": 0.6}
            }
            config = preset_configs[preset_name]
            mandala_data = generator.generate_mandala(**config)
        
        # Convert to SVG
        svg_content = mandala_to_svg_string(mandala_data)
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={
                "Content-Disposition": f"inline; filename=mandala_{preset_name}.svg"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating preset mandala: {str(e)}")

@app.get("/api/mandala/info",
         summary="Get Mandala Generation Info",
         description="Get information about available options")
async def get_mandala_info():
    """Get information about available mandala generation options."""
    return {
        "pattern_types": {
            "circles": "Circular patterns with varying sizes",
            "petals": "Petal-like elliptical shapes",
            "geometric": "Diamond and polygon shapes",
            "dots": "Concentric dot arrangements",
            "lines": "Radial and curved line patterns",
            "triangles": "Triangular geometric patterns",
            "stars": "5-pointed star patterns"
        },
        "color_schemes": {
            "rainbow": "Full spectrum rainbow colors",
            "warm": "Red, orange, yellow tones",
            "cool": "Blue, cyan, purple tones",
            "monochrome": "Single color variations",
            "earth": "Natural earth tone colors"
        },
        "presets": {
            "classic": "Traditional mandala with 6 layers, 8-fold symmetry",
            "complex": "Intricate design with 10 layers, 12-fold symmetry",
            "simple": "Minimalist design with 4 layers, 6-fold symmetry",
            "floral": "Flower-inspired patterns with petal emphasis",
            "geometric": "Mathematical geometric patterns"
        },
        "parameters": {
            "size": "Canvas size in pixels (200-2000)",
            "layers": "Number of concentric layers (1-15)",
            "symmetry": "Rotational symmetry count (3-24)",
            "complexity": "Pattern detail level (0.1-1.0)"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "mandala-generator"}



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    print("🎨 Starting Mandala Art Generator API...")
    print("📍 Server will be available at: http://localhost:8001")
    print("📚 API Documentation: http://localhost:8001/docs")
    print("🎯 Generate mandala: http://localhost:8001/api/mandala")
    print("🎨 Try presets: http://localhost:8001/api/mandala/preset/classic")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
