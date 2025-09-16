# SIH 2025 - Kolam Pattern Processing Suite 🎨

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0%2B-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![SIH](https://img.shields.io/badge/SIH-2025-orange.svg)](https://www.sih.gov.in/)

> A comprehensive suite of AI-powered tools for generating, processing, and recreating traditional South Indian kolam patterns. Built for Smart India Hackathon 2025.

## 🌟 Project Overview

This project provides a complete ecosystem for working with kolam patterns - from mathematical generation to image-based recreation. It combines traditional cultural art with modern computer vision and mathematical algorithms to preserve and digitize South Indian heritage.

### What are Kolams?

Kolams are intricate geometric patterns traditionally drawn with rice flour at the entrance of homes in South India. They represent prosperity, welcome guests, and showcase mathematical beauty through symmetry and continuous lines. This project aims to digitally preserve and recreate these cultural treasures.

## 🏗️ Project Architecture

The SIH-2025 Kolam Suite consists of two main components:

```
SIH-2025/
├── 📁 generate_kolam/          # Kolam Pattern Generator
│   ├── 🎯 Mathematical kolam generation
│   ├── 🔄 16 different curve types
│   ├── 📐 SVG vector output
│   └── 🚀 FastAPI server
│
└── 📁 recreate_kolam/          # Image-to-Vector Converter  
    ├── 🖼️ Image preprocessing
    ├── 🔍 Pattern recognition
    ├── 📏 Vectorization algorithms
    └── 🎨 SVG reconstruction
```

## ✨ Key Features

### 🎨 Kolam Pattern Generator (`generate_kolam/`)
- **Mathematical Precision**: Generate authentic kolam patterns using advanced algorithms
- **16 Curve Types**: Support for various traditional kolam curve styles
- **Symmetry Control**: Automatic symmetrical pattern generation
- **Vector Output**: High-quality SVG format for infinite scalability
- **REST API**: Easy integration with web applications
- **Interactive Documentation**: Auto-generated API docs

### 🔄 Image Recreation System (`recreate_kolam/`)
- **Image Processing**: Advanced preprocessing for clean pattern extraction
- **Pattern Recognition**: AI-powered detection of kolam structures
- **Vectorization**: Convert raster images to scalable vector graphics
- **Noise Reduction**: Clean up hand-drawn or photographed patterns
- **API Integration**: RESTful endpoints for batch processing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SIH-2025
   ```

2. **Set up Kolam Generator**
   ```bash
   cd generate_kolam
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Set up Image Recreator**
   ```bash
   cd ../recreate_kolam
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

### Running the Services

#### Start Kolam Generator API
```bash
cd generate_kolam
python main.py
```
- Server: http://localhost:8000
- API Docs: http://localhost:8000/docs

#### Start Image Recreation API
```bash
cd recreate_kolam
python main.py
```
- Server: http://localhost:8001 (or configured port)
- Upload and convert images to vector format

## 📖 API Documentation

### Kolam Generator API

**Base URL:** `http://localhost:8000`

#### Generate Kolam Pattern
```http
GET /api/kolam?size=10&background=%23ffffff&brush=%23000000
```

**Parameters:**
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `size` | integer | `7` | `3-15` | Grid size determining pattern complexity |
| `background` | string | `#7b3306` | hex color | Background color of the SVG |
| `brush` | string | `#ffffff` | hex color | Pattern line color |
| `type` | string | `geometric` | enum | Pattern type (geometric, iyal, rangoli, etc.) |

**Response:** SVG image with `Content-Type: image/svg+xml`

### Image Recreation API

**Base URL:** `http://localhost:8001`

#### Convert Image to Vector
```http
POST /convert
Content-Type: multipart/form-data

file: [image file]
```

**Supported Formats:** JPG, PNG, BMP, TIFF
**Response:** JSON with SVG data and processing metadata

## 🛠️ Technical Stack

### Core Technologies
- **FastAPI**: High-performance web framework
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical computing
- **scikit-image**: Advanced image processing algorithms
- **SVGWrite**: SVG generation and manipulation
- **Matplotlib**: Visualization and plotting

### Algorithms & Techniques
- **Mathematical Pattern Generation**: Geometric algorithms for authentic kolam creation
- **Image Preprocessing**: Noise reduction, thresholding, morphological operations
- **Skeletonization**: Extract pattern structure from images
- **Vectorization**: Convert raster to vector using interpolation
- **Path Optimization**: Smooth and optimize SVG paths

## 📁 Detailed Project Structure

### Generate Kolam Module
```
generate_kolam/
├── 📄 main.py                           # FastAPI application entry point
├── 📄 models.py                         # Pydantic data models
├── 📄 kolam_generator.py                # Core pattern generation logic
├── 📄 advanced_kolam_generator.py       # Advanced algorithms with 16 curve types
├── 📄 svg_generator.py                  # SVG rendering utilities
├── 📄 kolam_patterns.py                 # Pattern data management
├── 📄 image_processor.py                # Image processing utilities
├── 📁 data/
│   └── kolamPatternsData.json           # Pattern definitions and rules
├── 📄 requirements.txt                  # Python dependencies
├── 📄 KOLAM_MATHEMATICAL_FORMULAS.md    # Mathematical documentation
└── 📄 Zen_Kolam_API_Postman_Collection.json # API testing collection
```

### Recreate Kolam Module
```
recreate_kolam/
├── 📄 main.py              # FastAPI application for image processing
├── 📄 requirements.txt     # Python dependencies
└── 📁 venv/               # Virtual environment
```

## 🔧 Development

### Setting up Development Environment

1. **Install development dependencies**
   ```bash
   pip install black flake8 pytest mypy
   ```

2. **Code formatting**
   ```bash
   black .
   flake8 .
   mypy .
   ```

3. **Running tests**
   ```bash
   pytest tests/
   ```

### Architecture Principles

- **Modular Design**: Separate concerns between generation and recreation
- **API-First**: RESTful interfaces for all functionality
- **Type Safety**: Full type hints throughout the codebase
- **Documentation**: Comprehensive inline and API documentation
- **Performance**: Optimized algorithms for real-time processing

## 🎯 Use Cases

### Educational Applications
- **Cultural Preservation**: Digitize traditional kolam patterns
- **Mathematical Learning**: Explore geometry and symmetry concepts
- **Art Education**: Understand traditional Indian art forms

### Commercial Applications
- **Design Tools**: Generate patterns for textile, architecture, and graphic design
- **Mobile Apps**: Kolam drawing and learning applications
- **Cultural Tourism**: Interactive exhibits and digital art installations

### Research Applications
- **Pattern Analysis**: Study mathematical properties of traditional art
- **Computer Vision**: Advance image-to-vector conversion techniques
- **Cultural Studies**: Document and analyze regional pattern variations

## 🤝 Contributing

We welcome contributions to the SIH-2025 Kolam Suite! Please follow these guidelines:

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure code passes all checks: `black .`, `flake8 .`, `pytest`
6. Commit changes: `git commit -m "Add amazing feature"`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use type hints for all functions
- Add comprehensive docstrings
- Write meaningful commit messages
- Include tests for new features

### Areas for Contribution
- **Algorithm Improvements**: Enhance pattern generation algorithms
- **New Pattern Types**: Add support for regional kolam variations
- **Performance Optimization**: Improve processing speed
- **Documentation**: Expand tutorials and examples
- **Testing**: Increase test coverage
- **UI/UX**: Develop web interfaces

## 🐛 Troubleshooting

### Common Issues

**Installation Problems:**
```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

**API Server Issues:**
```bash
# Check if port is in use
netstat -an | findstr :8000

# Run with different port
uvicorn main:app --port 8001
```

**Image Processing Errors:**
- Ensure image files are in supported formats (JPG, PNG, BMP, TIFF)
- Check image file size (recommended < 10MB)
- Verify image contains clear, high-contrast patterns

### Performance Optimization

**For Large Images:**
- Resize images before processing
- Use appropriate preprocessing parameters
- Consider batch processing for multiple images

**For Complex Patterns:**
- Adjust grid size parameters
- Use appropriate curve types for pattern complexity
- Enable caching for repeated requests

## 📚 Additional Resources

### Documentation
- **Mathematical Formulas**: See `generate_kolam/KOLAM_MATHEMATICAL_FORMULAS.md`
- **API Testing**: Import `Zen_Kolam_API_Postman_Collection.json` into Postman
- **Pattern Data**: Explore `generate_kolam/data/kolamPatternsData.json`

### Cultural Resources
- [Kolam Traditions](https://en.wikipedia.org/wiki/Kolam) - Wikipedia overview
- [Mathematical Aspects of Kolam](https://www.jstor.org/stable/2690392) - Academic research
- [South Indian Art Forms](https://www.indianetzone.com/2/kolam.htm) - Cultural context

### Technical References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenCV Tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)
- [SVG Specification](https://www.w3.org/TR/SVG2/)

## 🏆 Smart India Hackathon 2025

This project was developed for Smart India Hackathon 2025, addressing the challenge of digitally preserving and recreating traditional Indian art forms using modern technology.

### Problem Statement
Develop a comprehensive system for:
- Generating authentic kolam patterns using mathematical algorithms
- Converting hand-drawn or photographed kolam images to digital vector format
- Preserving cultural heritage through technology
- Making traditional art accessible to modern applications

### Solution Approach
Our solution combines:
- **Mathematical Generation**: Algorithmic creation of authentic patterns
- **Computer Vision**: Advanced image processing for pattern extraction
- **Cultural Authenticity**: Adherence to traditional kolam principles
- **Modern Technology**: FastAPI, OpenCV, and vector graphics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Traditional Kolam Artists**: For inspiring this digital preservation effort
- **Smart India Hackathon**: For providing the platform to develop this solution
- **Open Source Community**: FastAPI, OpenCV, and other amazing tools
- **Cultural Researchers**: For documenting kolam traditions and mathematics
- **Team Contributors**: Everyone who made this project possible

## 📞 Support & Contact

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Email**: [Contact Team](mailto:team@example.com)
- **SIH Portal**: [Smart India Hackathon](https://www.sih.gov.in/)

## 🎖️ Team Information

**Team Name**: [Your Team Name]
**Institution**: [Your Institution]
**SIH 2025 Problem Statement**: [PS Number and Title]

---

**Made with ❤️ for Smart India Hackathon 2025 - Preserving Indian cultural heritage through innovative technology.**
