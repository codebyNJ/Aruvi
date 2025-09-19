# Aruvi Kolam API - Mathematical Formulas & Implementation

## Overview

The Zen Kolam API implements various types of South Indian kolam patterns using precise mathematical formulas. Each kolam type uses different mathematical approaches to generate beautiful, symmetric patterns.

## Kolam Types & Mathematical Formulas

### 1. Geometric Kolam

**Mathematical Foundation:**
- **Circle**: `x = r*cos(θ)`, `y = r*sin(θ)`
- **Square**: Parametric equations for square vertices
- **Triangle**: Equilateral triangle with inscribed circles

**Implementation:**
```python
# Circle generation
for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

# Square generation
half_side = side_length / 2
square_points = [
    Point(center_x - half_side, center_y - half_side),
    Point(center_x + half_side, center_y - half_side),
    Point(center_x + half_side, center_y + half_side),
    Point(center_x - half_side, center_y + half_side)
]
```

**Postman Example:**
```
GET /api/kolam/geometric?size=7&shape=circle&complexity=3&background=%237b3306&brush=%23ffffff
```

### 2. Iyal Kolam (Freehand/Flowing)

**Mathematical Foundation:**
- **Spiral Equations**: `r = a * θ^b`
- **Bezier Curves**: For smooth flowing lines
- **Wave Equations**: `y = A * sin(ωt + φ)`
- **Organic Variation**: Noise functions for natural flow

**Implementation:**
```python
# Spiral generation
for i in range(50):
    theta = (i / 49) * 4 * math.pi + spiral_angle_offset
    r = a * (theta ** b)
    
    # Add organic variation
    noise_factor = 1 + organic_factor * math.sin(theta * 3) * math.cos(theta * 2)
    r *= noise_factor
    
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)

# Wave generation
wave_amplitude = max_radius * 0.2 * flow_intensity
wave_freq = 3 + organic_factor * 2
wave_offset = wave_amplitude * math.sin(t * wave_freq * math.pi)
```

**Postman Example:**
```
GET /api/kolam/iyal?size=7&flow_intensity=0.5&organic_factor=0.3&background=%237b3306&brush=%23ffffff
```

### 3. Rangoli Kolam (Colorful Traditional)

**Mathematical Foundation:**
- **Rose Curves**: `r = a * cos(k * θ)`
- **Lissajous Curves**: `x = A * sin(at + δ)`, `y = B * sin(bt)`
- **Mandala Geometry**: Radial symmetry with `θ = 2π/n`
- **Lotus Petal Equations**: Parametric curves for petal shapes

**Implementation:**
```python
# Rose curve generation
for i in range(num_points):
    theta = 2 * math.pi * i / num_points
    r = max_radius * 0.8 * (1 - abs(t - 0.5) * 2)
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)

# Lotus petal generation
for i in range(20):
    t = i / 19
    r = max_radius * 0.8 * (1 - abs(t - 0.5) * 2)
    theta = petal_angle + (t - 0.5) * math.pi / 3
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)
```

**Postman Example:**
```
GET /api/kolam/rangoli?size=7&motif_type=lotus&color_scheme=traditional&complexity=3&background=%237b3306&brush=%23ff6b6b
```

### 4. Kavi Kolam (Chalk-based Bold)

**Mathematical Foundation:**
- **Straight Line Equations**: `y = mx + c`
- **Grid-based Patterns**: Cartesian coordinate system
- **Symmetric Transformations**: Reflection and rotation matrices
- **Diamond Geometry**: Rhombus calculations

**Implementation:**
```python
# Diamond pattern generation
for level in range(1, diamond_size + 1):
    half_size = (level * cell_size) / 2
    diamond_points = [
        Point(center_x, center_y - half_size),
        Point(center_x + half_size, center_y),
        Point(center_x, center_y + half_size),
        Point(center_x - half_size, center_y)
    ]

# Cross pattern generation
for i in range(1, grid_size, 2):
    for j in range(1, grid_size, 2):
        x = j * cell_size
        y = i * cell_size
        # Horizontal and vertical lines
```

**Postman Example:**
```
GET /api/kolam/kavi?size=7&line_thickness=2.0&precision=0.8&background=%237b3306&brush=%23ffffff
```

### 5. Traditional 1D Kolam

**Mathematical Foundation:**
- **Matrix-based Generation**: Using predefined pattern matrices
- **Symmetry Operations**: Horizontal and vertical inversions
- **Pattern Matching**: 16-pattern system with connection rules
- **Grid-based Algorithm**: Recursive pattern generation

**Implementation:**
```python
# Pattern matrix generation
pt_dn = [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1]
pt_rt = [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1]

# Symmetry operations
h_inv = [1, 2, 5, 4, 3, 9, 8, 7, 6, 10, 11, 12, 15, 14, 13, 16]
v_inv = [1, 4, 3, 2, 5, 7, 6, 9, 8, 10, 11, 14, 13, 12, 15, 16]
```

**Postman Example:**
```
GET /api/kolam?kolam_type=traditional_1d&size=7&background=%237b3306&brush=%23ffffff
```

## API Endpoints

### General Endpoint
```
GET /api/kolam
```
**Parameters:**
- `kolam_type`: geometric, iyal, rangoli, kavi, traditional_1d
- `size`: Grid size (3-15)
- `background`: Background color (hex)
- `brush`: Pattern color (hex)

### Specific Type Endpoints

#### Geometric Kolam
```
GET /api/kolam/geometric
```
**Parameters:**
- `shape`: circle, square, triangle
- `complexity`: 1-5
- `size`: 3-15
- `background`: hex color
- `brush`: hex color

#### Iyal Kolam
```
GET /api/kolam/iyal
```
**Parameters:**
- `flow_intensity`: 0.1-1.0
- `organic_factor`: 0.0-1.0
- `size`: 3-15
- `background`: hex color
- `brush`: hex color

#### Rangoli Kolam
```
GET /api/kolam/rangoli
```
**Parameters:**
- `motif_type`: lotus, mandala
- `color_scheme`: traditional, modern
- `complexity`: 1-5
- `size`: 3-15
- `background`: hex color
- `brush`: hex color

#### Kavi Kolam
```
GET /api/kolam/kavi
```
**Parameters:**
- `line_thickness`: 0.5-5.0
- `precision`: 0.1-1.0
- `size`: 3-15
- `background`: hex color
- `brush`: hex color

## Postman Collection Usage

1. **Import Collection**: Import `Zen_Kolam_API_Postman_Collection.json` into Postman
2. **Set Base URL**: Update the `base_url` variable to your server address
3. **Run Requests**: Execute any of the pre-configured requests
4. **Customize Parameters**: Modify query parameters as needed

## Mathematical Complexity

### Geometric Kolam
- **Time Complexity**: O(n²) where n is the grid size
- **Space Complexity**: O(n²) for pattern storage
- **Mathematical Operations**: Trigonometric functions, parametric equations

### Iyal Kolam
- **Time Complexity**: O(m×n) where m is spiral points, n is grid size
- **Space Complexity**: O(m×n) for curve storage
- **Mathematical Operations**: Spiral equations, wave functions, noise generation

### Rangoli Kolam
- **Time Complexity**: O(k×n) where k is motif complexity, n is grid size
- **Space Complexity**: O(k×n) for pattern storage
- **Mathematical Operations**: Rose curves, Lissajous curves, radial symmetry

### Kavi Kolam
- **Time Complexity**: O(n²) for grid-based patterns
- **Space Complexity**: O(n²) for line storage
- **Mathematical Operations**: Linear equations, geometric transformations

### Traditional 1D Kolam
- **Time Complexity**: O(n²) for matrix operations
- **Space Complexity**: O(n²) for pattern matrix
- **Mathematical Operations**: Matrix operations, symmetry transformations

## Color Schemes

### Traditional Colors
- Primary: `#ff6b6b` (Red)
- Secondary: `#4ecdc4` (Teal)
- Accent: `#45b7d1` (Blue)
- Highlight: `#f9ca24` (Yellow)
- Background: `#6c5ce7` (Purple)

### Modern Colors
- Primary: `#ffffff` (White)
- Secondary: `#ff9ff3` (Pink)
- Accent: `#54a0ff` (Blue)
- Highlight: `#5f27cd` (Purple)
- Background: `#00d2d3` (Cyan)

## Error Handling

The API includes comprehensive error handling for:
- Invalid kolam types
- Parameter validation
- Mathematical computation errors
- SVG generation failures

## Performance Considerations

- **Caching**: SVG responses are cached for 1 hour
- **Optimization**: Mathematical calculations are optimized for real-time generation
- **Memory Management**: Efficient memory usage for large patterns
- **Concurrent Requests**: Thread-safe pattern generation
