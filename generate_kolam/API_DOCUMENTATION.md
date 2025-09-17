# Zen Kolam API Documentation

Welcome to the Zen Kolam API! This API allows you to generate various types of South Indian kolam patterns as SVG images with mathematical precision.

## Base URL
```
http://localhost:8000
```

## API Endpoints

### 1. Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns API information and available endpoints
- **Response**:
  ```json
  {
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
  ```

### 2. Generate Any Kolam Type
- **URL**: `/api/kolam`
- **Method**: `GET`
- **Description**: Generate any type of kolam pattern as a static SVG image with customizable colors
- **Parameters**:
  - `kolam_type` (string, optional): Type of kolam (geometric, iyal, rangoli, kavi, traditional_1d). Default: traditional_1d
  - `size` (int, optional): Grid size for the kolam pattern (3-15). Default: 7
  - `background` (string, optional): Background color in hex format. Default: "#7b3306"
  - `brush` (string, optional): Pattern color in hex format. Default: "#ffffff"
- **Response**: SVG image with Content-Type: image/svg+xml

### 3. Generate Geometric Kolam
- **URL**: `/api/kolam/geometric`
- **Method**: `GET`
- **Description**: Generate Geometric Kolam with mathematical precision
- **Parameters**:
  - `size` (int, optional): Grid size (3-15). Default: 7
  - `shape` (string, optional): Geometric shape (circle, square, triangle). Default: "circle"
  - `complexity` (int, optional): Complexity level (1-5). Default: 3
  - `background` (string, optional): Background color in hex format. Default: "#7b3306"
  - `brush` (string, optional): Pattern color in hex format. Default: "#ffffff"
- **Response**: SVG image with Content-Type: image/svg+xml

### 4. Generate Iyal Kolam
- **URL**: `/api/kolam/iyal`
- **Method**: `GET`
- **Description**: Generate Iyal Kolam (freehand/flowing) with organic curves
- **Parameters**:
  - `size` (int, optional): Grid size (3-15). Default: 7
  - `flow_intensity` (float, optional): Flow intensity (0.1-1.0). Default: 0.5
  - `organic_factor` (float, optional): Organic variation factor (0.0-1.0). Default: 0.3
  - `background` (string, optional): Background color in hex format. Default: "#7b3306"
  - `brush` (string, optional): Pattern color in hex format. Default: "#ffffff"
- **Response**: SVG image with Content-Type: image/svg+xml

### 5. Generate Rangoli Kolam
- **URL**: `/api/kolam/rangoli`
- **Method**: `GET`
- **Description**: Generate Rangoli Kolam with colorful patterns and traditional motifs
- **Parameters**:
  - `size` (int, optional): Grid size (3-15). Default: 7
  - `motif_type` (string, optional): Motif type (lotus, mandala). Default: "lotus"
  - `color_scheme` (string, optional): Color scheme (traditional, modern). Default: "traditional"
  - `complexity` (int, optional): Complexity level (1-5). Default: 3
  - `background` (string, optional): Background color in hex format. Default: "#7b3306"
  - `brush` (string, optional): Pattern color in hex format. Default: "#ffffff"
- **Response**: SVG image with Content-Type: image/svg+xml

### 6. Generate Kavi Kolam
- **URL**: `/api/kolam/kavi`
- **Method**: `GET`
- **Description**: Generate Kavi Kolam (chalk-based) with bold lines and geometric precision
- **Parameters**:
  - `size` (int, optional): Grid size (3-15). Default: 7
  - `line_thickness` (float, optional): Line thickness (0.5-5.0). Default: 2.0
  - `precision` (float, optional): Precision level (0.1-1.0). Default: 0.8
  - `background` (string, optional): Background color in hex format. Default: "#7b3306"
  - `brush` (string, optional): Pattern color in hex format. Default: "#ffffff"
- **Response**: SVG image with Content-Type: image/svg+xml

## Examples

### Example 1: Generate a simple traditional kolam
```
GET /api/kolam?kolam_type=traditional_1d&size=5&background=#000000&brush=#FFD700
```

### Example 2: Generate a complex geometric kolam with custom colors
```
GET /api/kolam/geometric?shape=circle&size=9&complexity=4&background=#1a1a2e&brush=#e94560
```

### Example 3: Generate a flowing iyal kolam with high organic variation
```
GET /api/kolam/iyal?size=11&flow_intensity=0.8&organic_factor=0.7&background=#16213e&brush=#f8f1f1
```

## Error Handling
All endpoints return appropriate HTTP status codes:
- `200 OK`: Successful request, returns SVG image
- `400 Bad Request`: Invalid parameters provided
- `500 Internal Server Error`: Server-side error during kolam generation

## Caching
Responses include a `Cache-Control` header with a max-age of 3600 seconds (1 hour) to improve performance.
