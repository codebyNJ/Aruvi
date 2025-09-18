# Aruvi: Digital Kolam Platform

![Aruvi Logo](./Doodle%20-%2051.png)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> India's first digital platform for creating, studying, and preserving traditional Kolam art through AI and mathematics.

## 🌟 About Aruvi

Aruvi brings the ancient South Indian art of Kolam into the digital age. Our platform combines cultural preservation with modern technology, making traditional Kolam patterns accessible to everyone.

## ✨ Features

- **KolamGPT**: AI-powered pattern generation and cultural insights
- **KolamGenerator**: Create custom designs with mathematical precision
- **KolamExtract**: Digitize and analyze traditional patterns
- **SVG Export**: High-quality vector output for all designs
- **REST API**: Seamless integration with other applications

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aruvikolam.git
cd aruvikolam

# Set up environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the FastAPI server
uvicorn app:app --reload
```

Visit `http://localhost:8000` in your browser to access the application.

## 📚 Documentation

For detailed API documentation and usage examples, please visit our [Documentation](docs/).

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
