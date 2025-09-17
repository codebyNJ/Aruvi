# Mandala Art Generator API Documentation

## Base URL
```
/
```

## Authentication
No authentication is required to use this API.

## Endpoints

### 1. Get API Information
**GET** `/`

Returns basic information about the API and available endpoints.

**Response:**
```json
{
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
```

### 2. Generate Custom Mandala
**GET** `/api/mandala`

Generates a custom mandala with the specified parameters and returns it as an SVG image.

**Query Parameters:**
| Parameter | Type | Required | Default | Description | Constraints |
|-----------|------|----------|---------|-------------|-------------|
| size | integer | No | 800 | Canvas size (width and height in pixels) | 200 ≤ size ≤ 2000 |
| layers | integer | No | 6 | Number of concentric layers | 1 ≤ layers ≤ 15 |
| symmetry | integer | No | 8 | Rotational symmetry (number of repetitions) | 3 ≤ symmetry ≤ 24 |
| pattern_types | string | No | null | Comma-separated list of pattern types | Available types: circles, petals, geometric, dots, lines, triangles, stars |
| color_scheme | string | No | "rainbow" | Color scheme for the mandala | Options: rainbow, warm, cool, monochrome, earth |
| complexity | float | No | 0.7 | Pattern complexity | 0.1 ≤ complexity ≤ 1.0 |

**Example Request:**
```
GET /api/mandala?size=1000&layers=8&symmetry=12&pattern_types=circles,petals&color_scheme=cool&complexity=0.8
```

**Response:**
- Content-Type: `image/svg+xml`
- Returns: SVG image of the generated mandala

### 3. Generate Preset Mandala
**GET** `/api/mandala/preset/{preset_name}`

Generates a mandala using predefined preset configurations.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| preset_name | string | Yes | Name of the preset | Options: classic, complex, simple, floral, geometric |

**Query Parameters:**
| Parameter | Type | Required | Default | Description | Constraints |
|-----------|------|----------|---------|-------------|-------------|
| size | integer | No | 800 | Canvas size (width and height in pixels) | 200 ≤ size ≤ 2000 |

**Example Request:**
```
GET /api/mandala/preset/classic?size=1200
```

**Response:**
- Content-Type: `image/svg+xml`
- Returns: SVG image of the generated mandala

### 4. Get Mandala Information
**GET** `/api/mandala/info`

Returns information about available mandala generation options.

**Response:**
```json
{
    "pattern_types": ["circles", "petals", "geometric", "dots", "lines", "triangles", "stars"],
    "color_schemes": ["rainbow", "warm", "cool", "monochrome", "earth"],
    "presets": ["classic", "complex", "simple", "floral", "geometric"]
}
```

### 5. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
    "status": "OK",
    "version": "1.0.0"
}
```

## Error Responses
The API may return the following error responses:

- **400 Bad Request**: Invalid parameter values
- **404 Not Found**: Requested resource not found
- **500 Internal Server Error**: Server error while generating mandala

## Examples

### Generate a custom mandala with rainbow colors
```
GET /api/mandala?size=1000&layers=5&symmetry=10&color_scheme=rainbow
```

### Generate a complex geometric mandala
```
GET /api/mandala?pattern_types=geometric,lines&complexity=0.9&symmetry=12
```

### Get a preset floral mandala
```
GET /api/mandala/preset/floral?size=1500
```

## Rate Limiting
No rate limiting is currently implemented.
