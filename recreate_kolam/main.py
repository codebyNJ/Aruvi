import cv2
import numpy as np
from skimage.morphology import skeletonize, thin
from skimage import measure
from scipy import interpolate
import svgwrite
from collections import deque
import matplotlib.pyplot as plt
import io
import base64
import uuid
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import tempfile

# Initialize FastAPI app
app = FastAPI(title="Image to Vector Converter", 
              description="Convert images to SVG vector line drawings")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for temporary storage
TEMP_DIR = tempfile.gettempdir()

def preprocess_image(image_data: np.ndarray):
    """Enhanced preprocessing for cleaner binary image from in-memory data."""
    # Convert to grayscale if needed
    if len(image_data.shape) == 3:
        gray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_data
    
    # Apply noise reduction
    blurred = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Adaptive threshold with optimized parameters
    bw = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 21, 7
    )
    
    # Determine if we need to invert
    white_frac = np.mean(bw == 255)
    if white_frac < 0.5:
        bw = 255 - bw
    
    # Enhanced morphological operations
    kernel = np.ones((2, 2), np.uint8)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=1)
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Remove small noise
    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(bw, connectivity=8)
    sizes = stats[1:, -1]
    bw_cleaned = np.zeros_like(bw)
    for i in range(1, n_labels):
        if sizes[i-1] >= 50:  # Minimum area threshold
            bw_cleaned[labels == i] = 255
    
    return bw_cleaned

def get_skeleton(binary_img):
    """More accurate skeletonization with thinning."""
    # Ensure proper binary format
    binary = (binary_img > 128).astype(np.uint8)
    
    # Use Zhang-Suen thinning algorithm for more accurate results
    skeleton = thin(binary)
    
    return skeleton.astype(np.uint8) * 255

def find_endpoints_junctions(skel):
    """Find endpoints and junctions in the skeleton."""
    # Kernel for convolution to find neighbors
    kernel = np.array([[1, 1, 1],
                       [1, 10, 1],
                       [1, 1, 1]], dtype=np.uint8)
    
    # Convert to binary for processing
    skel_bin = (skel > 0).astype(np.uint8)
    
    # Convolve to count neighbors
    neighbor_count = cv2.filter2D(skel_bin, -1, kernel)
    
    # Endpoints have exactly 1 neighbor (value 11)
    endpoints = np.where(neighbor_count == 11)
    endpoints = list(zip(endpoints[1], endpoints[0]))  # Convert to (x, y)
    
    # Junctions have 3 or more neighbors (value >= 13)
    junctions = np.where(neighbor_count >= 13)
    junctions = list(zip(junctions[1], junctions[0]))  # Convert to (x, y)
    
    return endpoints, junctions

def trace_path_from_point(skel, start_point, visited, min_length=10):
    """Trace a path from a starting point using breadth-first search."""
    directions = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0),           (1, 0),
        (-1, 1),  (0, 1),  (1, 1)
    ]
    
    path = []
    queue = deque([start_point])
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) in visited or x < 0 or y < 0 or x >= skel.shape[1] or y >= skel.shape[0]:
            continue
        
        if skel[y, x] == 0:  # Not part of skeleton
            continue
        
        visited.add((x, y))
        path.append((x, y))
        
        # Check all 8 directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < skel.shape[1] and 0 <= ny < skel.shape[0]:
                if skel[ny, nx] > 0 and (nx, ny) not in visited:
                    queue.append((nx, ny))
    
    # Only return paths that meet the minimum length requirement
    if len(path) >= min_length:
        return np.array(path), visited
    else:
        return None, visited

def extract_paths_from_skeleton(skel):
    """Extract paths by tracing from endpoints and junctions."""
    # Find endpoints and junctions
    endpoints, junctions = find_endpoints_junctions(skel)
    
    # Combine all starting points
    start_points = endpoints + junctions
    
    visited = set()
    paths = []
    
    # Trace paths from each starting point
    for point in start_points:
        if point not in visited:
            path, visited = trace_path_from_point(skel, point, visited)
            if path is not None:
                paths.append(path)
    
    # Also find contours for any remaining isolated loops
    contours = measure.find_contours(skel, 0.5)
    for contour in contours:
        if len(contour) > 20:  # Minimum length for contours
            # Convert from (row, col) to (x, y)
            path = np.column_stack([contour[:, 1], contour[:, 0]])
            
            # Check if this path is already discovered
            is_new = True
            for existing_path in paths:
                if len(set(map(tuple, path)) & set(map(tuple, existing_path))) > 5:
                    is_new = False
                    break
            
            if is_new:
                paths.append(path)
    
    return paths

def simplify_path(path, tolerance=0.5):
    """Simplify path using Ramer-Douglas-Peucker algorithm."""
    if len(path) < 3:
        return path
    
    # Convert to format expected by OpenCV
    path_float = path.astype(np.float32)
    
    # Apply Ramer-Douglas-Peucker algorithm
    epsilon = tolerance
    closed = False  # Assume paths are not closed
    
    # Check if path is closed (start and end points are close)
    if np.linalg.norm(path[0] - path[-1]) < 5:
        closed = True
    
    simplified = cv2.approxPolyDP(path_float, epsilon, closed)
    
    return simplified.reshape(-1, 2)

def smooth_path(path, smoothing=0.002, num_points=200):
    """Fit a spline to smooth strokes with better handling."""
    if len(path) < 4:
        return path
    
    x, y = path[:, 0], path[:, 1]
    
    # Remove duplicate points
    unique_points = []
    for i in range(len(x)):
        if i == 0 or (x[i] != x[i-1] or y[i] != y[i-1]):
            unique_points.append((x[i], y[i]))
    
    if len(unique_points) < 4:
        return path
    
    x, y = zip(*unique_points)
    
    try:
        # Use cubic spline interpolation
        tck, u = interpolate.splprep([x, y], s=smoothing*len(path), k=3)
        u_new = np.linspace(u.min(), u.max(), num_points)
        out = interpolate.splev(u_new, tck)
        return np.column_stack(out)
    except:
        # Fallback: use moving average smoothing
        window_size = min(5, len(x) // 2)
        if window_size > 1:
            x_smooth = np.convolve(x, np.ones(window_size)/window_size, mode='valid')
            y_smooth = np.convolve(y, np.ones(window_size)/window_size, mode='valid')
            return np.column_stack([x_smooth, y_smooth])
        else:
            return path

def image_to_svg_string(image_data: np.ndarray, img_shape, scale=1.0, stroke_width=1.0):
    """Convert image data to SVG string."""
    h, w = img_shape
    
    # Create in-memory SVG
    svg_io = io.StringIO()
    dwg = svgwrite.Drawing(size=(w*scale, h*scale))
    dwg.add(dwg.rect(insert=(0, 0), size=(w*scale, h*scale), fill='white'))
    
    # Convert image to base64 for SVG
    _, buffer = cv2.imencode('.png', image_data)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # Add image to SVG
    dwg.add(dwg.image(href=f"data:image/png;base64,{img_base64}", 
                      insert=(0, 0), 
                      size=(w*scale, h*scale)))
    
    # Get SVG as string
    svg_content = dwg.tostring()
    return svg_content

def paths_to_svg_string(paths, img_shape, scale=1.0, stroke_width=1.0):
    """Convert paths to SVG string instead of saving to file."""
    h, w = img_shape
    
    # Create in-memory SVG
    svg_io = io.StringIO()
    dwg = svgwrite.Drawing(size=(w*scale, h*scale))
    dwg.add(dwg.rect(insert=(0, 0), size=(w*scale, h*scale), fill='white'))
    
    for path in paths:
        if len(path) < 2:
            continue
        
        # Convert points to SVG coordinates
        pts = [(float(x*scale), float(y*scale)) for x, y in path]
        
        # Use path element for better rendering of complex shapes
        path_data = "M " + " L ".join(f"{x},{y}" for x, y in pts)
        
        svg_path = dwg.path(
            d=path_data,
            stroke='black',
            fill='none',
            stroke_width=stroke_width,
            stroke_linecap='round',
            stroke_linejoin='round'
        )
        dwg.add(svg_path)
    
    # Get SVG as string
    svg_content = dwg.tostring()
    return svg_content

def visualize_processing_steps(bw, skel, paths, filename):
    """Visualize the processing steps for debugging."""
    plt.figure(figsize=(15, 5))
    
    # Original binary image
    plt.subplot(131)
    plt.imshow(bw, cmap='gray')
    plt.title('Binary Image')
    plt.axis('off')
    
    # Skeleton
    plt.subplot(132)
    plt.imshow(skel, cmap='gray')
    plt.title('Skeleton')
    plt.axis('off')
    
    # Extracted paths
    plt.subplot(133)
    plt.imshow(np.ones_like(bw) * 255, cmap='gray')
    for path in paths:
        plt.plot(path[:, 0], path[:, 1], 'b-', linewidth=1)
    plt.title('Extracted Paths')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

def image_to_svg(image_data: np.ndarray, smoothing=0.002, num_points=200, generate_debug=False):
    """Main function to convert image to SVG vector."""
    # Preprocess the image
    bw = preprocess_image(image_data)
    
    # Get skeleton
    skel = get_skeleton(bw)
    
    # Extract paths
    raw_paths = extract_paths_from_skeleton(skel)
    
    # Generate debug visualization if requested
    if generate_debug:
        debug_filename = os.path.join(TEMP_DIR, f"debug_{uuid.uuid4().hex}.png")
        visualize_processing_steps(bw, skel, raw_paths, debug_filename)
    
    # Simplify and smooth paths
    simplified_paths = [simplify_path(p, tolerance=0.8) for p in raw_paths]
    smoothed_paths = [smooth_path(p, smoothing=smoothing, num_points=num_points) 
                     for p in simplified_paths]
    
    # Convert binary image to SVG
    binary_svg = image_to_svg_string(bw, img_shape=bw.shape)
    
    # Convert paths to SVG
    paths_svg = paths_to_svg_string(smoothed_paths, img_shape=bw.shape, stroke_width=1.2)
    
    return binary_svg, paths_svg, len(raw_paths)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Image to Vector Converter API",
        "endpoints": {
            "/convert": "POST endpoint to convert images to SVG",
            "/health": "GET endpoint to check API health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

@app.post("/convert")
async def convert_image_to_svg(
    file: UploadFile = File(..., description="Image file to convert to SVG"),
    smoothing: Optional[float] = 0.002,
    num_points: Optional[int] = 200,
    debug: Optional[bool] = False
):
    """
    Convert an uploaded image to SVG vector format.
    
    Parameters:
    - file: Image file (JPG, PNG, etc.)
    - smoothing: Smoothing factor for paths (default: 0.002)
    - num_points: Number of points for spline interpolation (default: 200)
    - debug: Whether to generate debug visualization (default: False)
    
    Returns:
    - JSON with binary image SVG, extracted paths SVG, and metadata
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")
    
    try:
        # Read image data
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image_data = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image_data is None:
            raise HTTPException(status_code=400, detail="Could not decode image")
        
        # Convert to SVG
        binary_svg, paths_svg, num_paths = image_to_svg(
            image_data, 
            smoothing=smoothing, 
            num_points=num_points,
            generate_debug=debug
        )
        
        # Generate a preview image
        _, buffer = cv2.imencode('.png', image_data)
        preview_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Return JSON response with both SVGs
        return JSONResponse(
            content={
                "binary_svg": binary_svg,
                "paths_svg": paths_svg,
                "preview": f"data:image/png;base64,{preview_base64}",
                "paths_count": num_paths,
                "filename": file.filename,
                "status": "success"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)