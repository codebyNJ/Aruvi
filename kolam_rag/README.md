# Smart Kolam RAG System

A sophisticated Retrieval-Augmented Generation (RAG) system specifically designed for Kolam-related queries. This system supports both Tamil and English queries with domain-specific optimizations for traditional Tamil floor art documentation.

## Features

- **Multilingual Support**: Handles both Tamil and English queries
- **Domain-Aware Chunking**: Optimized text processing for Kolam-specific content
- **Smart Retrieval**: Enhanced query processing with domain keywords
- **Fallback Content**: Built-in Kolam knowledge base for offline operation
- **Performance Optimized**: Fast FAISS-based vector search
- **Robust Error Handling**: Graceful degradation when external sources fail

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For GPU support (optional):
```bash
# Uncomment faiss-gpu in requirements.txt and install
pip install faiss-gpu
```

## Quick Start

```python
from smart_kolam_rag import SmartKolamRAG

# Initialize the RAG system
kolam_rag = SmartKolamRAG()

# Load Kolam documentation
kolam_rag.load_kolam_documentation()

# Query the system
result = kolam_rag.smart_query("What is Kolam?")
print(result['answer'])
```

## Usage Examples

### Basic Query
```python
# Simple question about Kolam
result = kolam_rag.smart_query("What materials are used for kolam?")
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']:.3f}")
```

### Query with Metadata
```python
# Get detailed information including sources
result = kolam_rag.smart_query(
    "How does kolam benefit cognitive development?", 
    include_metadata=True
)

print(f"Answer: {result['answer']}")
print(f"Retrieved {result['retrieved_docs']} documents")
print(f"Processing time: {result['processing_time']:.2f}s")

# Access context snippets
if 'context_snippets' in result:
    for i, snippet in enumerate(result['context_snippets']):
        print(f"Context {i+1}: {snippet[:100]}...")
```

### Tamil Language Query
```python
# Tamil language support
result = kolam_rag.smart_query("கோலம் என்றால் என்ன?")
print(result['answer'])
```

## Configuration Options

```python
kolam_rag = SmartKolamRAG(
    embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    chunk_size=600,           # Size of text chunks
    chunk_overlap=150,        # Overlap between chunks
    top_k_retrieval=6,        # Number of documents to retrieve
    similarity_threshold=0.1  # Minimum similarity score
)
```

## System Statistics

Get insights about your knowledge base:

```python
stats = kolam_rag.get_kolam_statistics()
print(f"Total documents: {stats['total_documents']}")
print(f"Tamil content: {stats['tamil_content_docs']} docs")
print(f"Data sources: {stats['data_sources']}")
```

## Supported Query Types

### Cultural and Historical
- "What is the cultural significance of Kolam?"
- "When is Kolam traditionally drawn?"
- "கோலத்தின் வரலாறு என்ன?"

### Technical and Methods
- "How to draw Pulli Kolam?"
- "What are the different types of Kolam patterns?"
- "What materials are needed for Kolam?"

### Benefits and Applications
- "What are the cognitive benefits of drawing Kolam?"
- "How does Kolam help with motor skills?"
- "Educational benefits of Kolam practice"

## Data Sources

The system retrieves information from:
- Sahapedia (Cultural heritage documentation)
- Kolampodu.com (Traditional art blog)
- Built-in fallback content (Comprehensive Kolam knowledge)

## Architecture

### Components
1. **SmartKolamRAG**: Main RAG system class
2. **Domain-Aware Chunking**: Kolam-specific text processing
3. **Multilingual Embeddings**: Support for Tamil and English
4. **FAISS Vector Store**: Fast similarity search
5. **Query Enhancement**: Domain-specific query expansion

### Processing Pipeline
1. **Document Loading**: Web scraping + fallback content
2. **Text Preprocessing**: Cleaning and normalization
3. **Smart Chunking**: Domain-aware text segmentation
4. **Embedding Creation**: Multilingual sentence embeddings
5. **Vector Indexing**: FAISS-based similarity search
6. **Query Processing**: Enhanced retrieval and answer generation

## Performance

- **Embedding Model**: Multilingual MiniLM (384 dimensions)
- **Vector Store**: FAISS IndexFlatIP (cosine similarity)
- **Batch Processing**: 16 documents per batch
- **Typical Query Time**: 0.1-0.5 seconds
- **Memory Usage**: ~200MB (base model + embeddings)

## Error Handling

The system includes robust error handling:
- Network failures → Fallback to built-in content
- Model loading errors → Clear error messages
- Empty queries → Helpful prompts
- No results → Suggested query improvements

## Debugging

Enable debug information:

```python
debug_info = kolam_rag.debug_system()
for key, value in debug_info.items():
    print(f"{key}: {value}")
```

## Contributing

To extend the system:
1. Add new data sources in `load_kolam_documentation()`
2. Enhance keywords in `kolam_keywords` dictionary
3. Improve query enhancement in `_enhance_query()`
4. Add new chunking separators for better text processing

## License

This project is part of the SIH-2025 Kolam generation and analysis toolkit.

## Support

For issues or questions about the Kolam RAG system, please refer to the main project documentation or create an issue in the repository.
