"""
Smart Kolam RAG System - Fixed Version
Supports Tamil, English queries with domain-specific optimizations
"""

import os
import logging
import warnings
from typing import List, Dict, Optional, Tuple, Any
import json
import time
from datetime import datetime
import re

# Core libraries
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Document processing
import trafilatura
import requests
from pathlib import Path

# Advanced chunking and processing
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=UserWarning)

class SmartKolamRAG:
    """
    Fixed RAG system optimized specifically for Kolam documentation
    Features: Fast retrieval, domain-aware chunking, multilingual support
    """

    def __init__(
        self,
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        chunk_size: int = 600,
        chunk_overlap: int = 150,
        top_k_retrieval: int = 6,
        similarity_threshold: float = 0.1  # Lowered threshold
    ):
        """Initialize Smart Kolam RAG System"""

        self.embedding_model_name = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k_retrieval = top_k_retrieval
        self.similarity_threshold = similarity_threshold

        # Domain-specific keywords for enhanced retrieval
        self.kolam_keywords = {
            'english': [
                'kolam', 'rangoli', 'floor art', 'tamil culture', 'rice flour',
                'geometric patterns', 'pulli', 'dots', 'threshold', 'auspicious',
                'lakshmi', 'pongal', 'margazhi', 'sikku', 'kambi', 'brain',
                'motor skills', 'coordination', 'cognitive', 'meditation',
                'mathematical', 'fibonacci', 'symmetry', 'patterns'
            ],
            'tamil': [
                'கோலம்', 'புள்ளி', 'சிக்கு', 'கம்பி', 'மார்கழி', 'பொங்கல்',
                'லட்சுமி', 'அரிசி மாவு', 'வாசல்', 'மங்கலம்'
            ]
        }

        # Initialize components
        self.embedding_model = None
        self.vector_store = None
        self.documents = []
        self.document_metadata = []
        self.embeddings = None
        self.query_cache = {}

        # Load models
        self._load_models()

    def _load_models(self):
        """Load optimized models for Kolam domain"""
        logger.info("🚀 Loading Smart Kolam RAG models...")

        try:
            self.embedding_model = SentenceTransformer(
                self.embedding_model_name,
                device='cuda' if torch.cuda.is_available() else 'cpu'
            )
            logger.info(f"✅ Embedding model loaded: {self.embedding_model_name}")
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {e}")
            raise

    def _enhance_text_preprocessing(self, text: str) -> str:
        """Enhanced preprocessing for Kolam-specific content"""
        if not text:
            return ""

        # Clean up text
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\u0B80-\u0BFF.,;:!?()-]', ' ', text)

        return text.strip()

    def _domain_aware_chunking(self, text: str) -> List[Document]:
        """Advanced chunking optimized for Kolam documentation"""

        if not text or len(text) < 50:
            logger.warning("Text too short for chunking")
            return []

        # Preprocess text
        text = self._enhance_text_preprocessing(text)

        # Domain-specific separators for Kolam content
        kolam_separators = [
            "\n\n## ",
            "\n\n# ",
            "\n\nKōlam ",
            "\n\nkolam ",
            "\n\n• ",
            "\n\n",
            "\n",
            ". ",
            "! ",
            "? "
        ]

        # Create splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=kolam_separators,
            length_function=len,
            keep_separator=True
        )

        chunks = splitter.split_text(text)

        # Create documents with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 20:  # Skip very short chunks
                continue

            importance_score = self._calculate_chunk_importance(chunk)

            doc = Document(
                page_content=chunk,
                metadata={
                    'chunk_id': i,
                    'length': len(chunk),
                    'importance_score': importance_score,
                    'contains_tamil': bool(re.search(r'[\u0B80-\u0BFF]', chunk)),
                    'keyword_density': self._calculate_keyword_density(chunk)
                }
            )
            documents.append(doc)

        logger.info(f"✅ Created {len(documents)} domain-aware chunks")
        return documents

    def _calculate_chunk_importance(self, text: str) -> float:
        """Calculate importance score based on Kolam-specific keywords"""

        if not text:
            return 0.0

        text_lower = text.lower()
        score = 0.0

        # English keywords scoring
        for keyword in self.kolam_keywords['english']:
            count = text_lower.count(keyword.lower())
            score += count * 1.0

        # Tamil keywords scoring
        for keyword in self.kolam_keywords['tamil']:
            count = text.count(keyword)
            score += count * 1.5

        # Cultural context bonus
        cultural_terms = ['tamil nadu', 'tradition', 'ritual', 'festival', 'culture']
        for term in cultural_terms:
            if term in text_lower:
                score += 0.5

        # Normalize by text length
        return score / max(len(text) / 100, 1)

    def _calculate_keyword_density(self, text: str) -> float:
        """Calculate keyword density for chunk ranking"""

        words = text.lower().split()
        if not words:
            return 0.0

        keyword_count = 0
        all_keywords = self.kolam_keywords['english'] + self.kolam_keywords['tamil']

        for word in words:
            for keyword in all_keywords:
                if keyword.lower() in word:
                    keyword_count += 1

        return keyword_count / len(words)

    def load_kolam_documentation(self):
        """Load and process Kolam-specific URLs with better error handling"""

        logger.info("📚 Loading Kolam documentation...")

        urls = [
            "https://www.sahapedia.org/significance-of-kolam-tamil-culture",
            "https://kolampodu.com/blogs/news"
        ]

        all_documents = []

        # Add fallback content in case URLs fail
        fallback_content = """
        Kolam: Traditional Tamil Floor Art

        Kolam is a traditional decorative art form from Tamil Nadu, India. It involves creating intricate geometric patterns on the floor using rice flour, chalk powder, or other materials.

        Cultural Significance:
        Kolam holds deep cultural and spiritual significance in Tamil tradition. It is believed to bring prosperity, ward off evil, and welcome goddess Lakshmi into homes.

        Types of Kolam:
        1. Pulli Kolam - Uses dots as connecting points
        2. Sikku Kolam - Continuous line patterns without lifting the hand
        3. Kambi Kolam - Rope-like interwoven patterns
        4. Padi Kolam - Step patterns that grow outward

        Materials Used:
        - Rice flour (traditional and eco-friendly)
        - Chalk powder
        - Rangoli colors
        - Sand

        Cognitive Benefits:
        Drawing kolam improves:
        - Hand-eye coordination
        - Mathematical thinking
        - Pattern recognition
        - Concentration and meditation
        - Motor skills development

        Festivals and Occasions:
        Kolam is especially important during:
        - Pongal festival
        - Margazhi month
        - Daily morning rituals
        - Auspicious occasions and ceremonies

        Learning Kolam:
        Beginners should start with simple dot patterns and gradually progress to complex designs. Regular practice improves skill and creativity.
        """

        # Try to load from URLs first
        for url in urls:
            try:
                logger.info(f"🌐 Processing: {url}")

                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    downloaded = response.text
                else:
                    logger.warning(f"⚠️ HTTP {response.status_code} for {url}")
                    continue

                # Extract content
                extracted = trafilatura.extract(
                    downloaded,
                    include_comments=False,
                    include_tables=True,
                    include_images=False,
                    output_format='txt'
                )

                if extracted and len(extracted) > 100:
                    # Domain-aware chunking
                    documents = self._domain_aware_chunking(extracted)

                    # Add source metadata
                    for doc in documents:
                        doc.metadata['source'] = url
                        doc.metadata['source_type'] = 'web'

                    all_documents.extend(documents)
                    logger.info(f"✅ Processed {len(documents)} chunks from {url}")
                else:
                    logger.warning(f"⚠️ No meaningful content from: {url}")

            except Exception as e:
                logger.error(f"❌ Error processing {url}: {e}")
                continue

        # Add fallback content if no URLs worked
        if not all_documents:
            logger.info("📝 Using fallback Kolam content")
            fallback_docs = self._domain_aware_chunking(fallback_content)
            for doc in fallback_docs:
                doc.metadata['source'] = 'fallback_content'
                doc.metadata['source_type'] = 'builtin'
            all_documents.extend(fallback_docs)

        if not all_documents:
            raise ValueError("❌ No documents were successfully loaded!")

        # Store documents
        self.documents = [doc.page_content for doc in all_documents]
        self.document_metadata = [doc.metadata for doc in all_documents]

        logger.info(f"✅ Total documents loaded: {len(self.documents)}")

        # Create vector store
        self._create_smart_vector_store()

    def _create_smart_vector_store(self):
        """Create optimized FAISS vector store with better error handling"""

        logger.info("🧠 Creating smart vector embeddings...")

        try:
            if not self.documents:
                raise ValueError("No documents to embed")

            # Create embeddings in batches
            batch_size = 16
            all_embeddings = []

            for i in range(0, len(self.documents), batch_size):
                batch = self.documents[i:i+batch_size]
                try:
                    batch_embeddings = self.embedding_model.encode(
                        batch,
                        batch_size=len(batch),
                        show_progress_bar=True,
                        convert_to_numpy=True
                    )
                    all_embeddings.append(batch_embeddings)
                except Exception as e:
                    logger.error(f"Error encoding batch {i}: {e}")
                    continue

            if not all_embeddings:
                raise ValueError("Failed to create any embeddings")

            # Combine all embeddings
            self.embeddings = np.vstack(all_embeddings).astype('float32')

            # Create FAISS index
            dimension = self.embeddings.shape[1]
            self.vector_store = faiss.IndexFlatIP(dimension)

            # Normalize for cosine similarity
            faiss.normalize_L2(self.embeddings)
            self.vector_store.add(self.embeddings)

            logger.info(f"✅ Vector store created with {len(self.documents)} documents")

        except Exception as e:
            logger.error(f"❌ Error creating vector store: {e}")
            raise

    def _smart_retrieve(self, query: str, k: int = None) -> Tuple[List[str], List[float], List[Dict]]:
        """Enhanced retrieval with better error handling"""

        if k is None:
            k = self.top_k_retrieval

        try:
            # Enhance query
            enhanced_query = self._enhance_query(query)

            # Encode query
            query_embedding = self.embedding_model.encode([enhanced_query])
            query_embedding = np.array(query_embedding).astype('float32')
            faiss.normalize_L2(query_embedding)

            # Search
            search_k = min(k * 2, len(self.documents))
            scores, indices = self.vector_store.search(query_embedding, search_k)

            # Filter results
            valid_results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx >= 0 and idx < len(self.documents):  # Valid index
                    if score >= self.similarity_threshold:
                        valid_results.append((score, idx))

            # If no good results, take top k anyway
            if not valid_results:
                logger.warning(f"No results above threshold, taking top {k}")
                valid_results = [(scores[0][i], indices[0][i]) for i in range(min(k, len(scores[0])))
                               if indices[0][i] >= 0]

            # Sort and limit
            valid_results.sort(reverse=True, key=lambda x: x[0])
            valid_results = valid_results[:k]

            # Extract results
            retrieved_docs = []
            similarity_scores = []
            metadata_list = []

            for score, idx in valid_results:
                retrieved_docs.append(self.documents[idx])
                similarity_scores.append(float(score))
                metadata_list.append(self.document_metadata[idx])

            logger.info(f"⚡ Retrieved {len(retrieved_docs)} documents")
            return retrieved_docs, similarity_scores, metadata_list

        except Exception as e:
            logger.error(f"❌ Error in retrieval: {e}")
            return [], [], []

    def _enhance_query(self, query: str) -> str:
        """Enhance query with domain context"""

        query_lower = query.lower()

        if any(term in query_lower for term in ['what is', 'என்ன']):
            query += " kolam traditional art Tamil culture"
        elif any(term in query_lower for term in ['how to', 'எப்படி']):
            query += " kolam drawing method technique"
        elif any(term in query_lower for term in ['benefits', 'நன்மை']):
            query += " kolam cognitive motor skills brain"
        elif any(term in query_lower for term in ['types', 'வகை']):
            query += " kolam patterns designs pulli sikku kambi"

        return query

    def _generate_simple_answer(self, query: str, context: str) -> str:
        """Generate simple rule-based answer when LLM fails"""

        query_lower = query.lower()

        # Extract relevant sentences from context
        sentences = context.split('. ')
        relevant_sentences = []

        # Find sentences with query keywords
        query_words = set(query_lower.split())
        kolam_words = {'kolam', 'tamil', 'art', 'pattern', 'culture', 'traditional'}
        query_words.update(kolam_words)

        for sentence in sentences:
            sentence_words = set(sentence.lower().split())
            if query_words & sentence_words:  # If any common words
                relevant_sentences.append(sentence.strip())

        if relevant_sentences:
            # Take top 3 most relevant sentences
            answer = '. '.join(relevant_sentences[:3])
            if not answer.endswith('.'):
                answer += '.'
            return answer

        # Fallback answer based on context
        if 'kolam' in context.lower():
            return "Based on the available information about Kolam: " + context[:300] + "..."

        return "I found some information related to your question, but I need more specific details to provide a comprehensive answer about Kolam."

    def smart_query(self, question: str, include_metadata: bool = False) -> Dict[str, Any]:
        """Main smart query interface with robust error handling"""

        logger.info(f"🤔 Smart Kolam Query: {question[:50]}...")
        start_time = time.time()

        try:
            # Validate inputs
            if not question or not question.strip():
                return {
                    'answer': "Please ask a specific question about Kolam.",
                    'query': question,
                    'retrieved_docs': 0,
                    'processing_time': 0,
                    'confidence': 0.0,
                    'error': 'Empty query'
                }

            if not self.vector_store:
                return {
                    'answer': "Knowledge base not loaded. Please load Kolam documentation first.",
                    'query': question,
                    'retrieved_docs': 0,
                    'processing_time': 0,
                    'confidence': 0.0,
                    'error': 'No vector store'
                }

            # Smart retrieval
            retrieved_docs, scores, metadata = self._smart_retrieve(question)

            if not retrieved_docs:
                return {
                    'answer': "I couldn't find relevant information about Kolam for your question. Please try asking about Kolam traditions, techniques, cultural significance, or benefits.",
                    'query': question,
                    'retrieved_docs': 0,
                    'processing_time': time.time() - start_time,
                    'confidence': 0.0,
                    'error': 'No retrieval results'
                }

            # Create context
            context = self._create_smart_context(retrieved_docs, metadata)

            # Generate answer using simple method
            answer = self._generate_simple_answer(question, context)

            # Calculate confidence
            confidence = np.mean(scores) if scores else 0.0

            result = {
                'answer': answer,
                'query': question,
                'retrieved_docs': len(retrieved_docs),
                'confidence': float(confidence),
                'processing_time': time.time() - start_time,
                'has_tamil_content': any(meta.get('contains_tamil', False) for meta in metadata)
            }

            if include_metadata:
                result.update({
                    'context_snippets': retrieved_docs[:3],
                    'similarity_scores': scores[:3],
                    'source_metadata': metadata[:3]
                })

            logger.info(f"✅ Query completed in {result['processing_time']:.2f}s")
            return result

        except Exception as e:
            logger.error(f"❌ Error in smart_query: {e}")
            return {
                'answer': f"I encountered an error processing your question: {str(e)}",
                'query': question,
                'retrieved_docs': 0,
                'processing_time': time.time() - start_time,
                'confidence': 0.0,
                'error': str(e)
            }

    def _create_smart_context(self, docs: List[str], metadata: List[Dict]) -> str:
        """Create intelligently combined context"""

        if not docs:
            return ""

        # Sort by importance if available
        doc_meta_pairs = list(zip(docs, metadata))
        doc_meta_pairs.sort(key=lambda x: x[1].get('importance_score', 0), reverse=True)

        # Combine with length limit
        combined_context = []
        total_length = 0
        max_length = 1500

        for doc, meta in doc_meta_pairs:
            if total_length + len(doc) < max_length:
                combined_context.append(doc.strip())
                total_length += len(doc)
            else:
                remaining = max_length - total_length
                if remaining > 100:
                    combined_context.append(doc[:remaining].strip() + "...")
                break

        return "\n\n".join(combined_context)

    def get_kolam_statistics(self) -> Dict[str, Any]:
        """Get statistics about the loaded knowledge base"""

        if not self.documents:
            return {"error": "No documents loaded"}

        total_docs = len(self.documents)
        tamil_docs = sum(1 for meta in self.document_metadata if meta.get('contains_tamil', False))

        if self.document_metadata:
            avg_importance = np.mean([meta.get('importance_score', 0) for meta in self.document_metadata])
            avg_keyword_density = np.mean([meta.get('keyword_density', 0) for meta in self.document_metadata])
        else:
            avg_importance = 0
            avg_keyword_density = 0

        sources = set(meta.get('source', 'unknown') for meta in self.document_metadata)

        return {
            'total_documents': total_docs,
            'tamil_content_docs': tamil_docs,
            'english_only_docs': total_docs - tamil_docs,
            'average_importance_score': float(avg_importance),
            'average_keyword_density': float(avg_keyword_density),
            'data_sources': list(sources),
            'cache_size': len(self.query_cache),
            'vector_store_size': self.vector_store.ntotal if self.vector_store else 0
        }

    def debug_system(self) -> Dict[str, Any]:
        """Debug system state"""

        return {
            'embedding_model_loaded': self.embedding_model is not None,
            'documents_loaded': len(self.documents),
            'vector_store_created': self.vector_store is not None,
            'embeddings_shape': self.embeddings.shape if self.embeddings is not None else None,
            'cache_entries': len(self.query_cache),
            'sample_document': self.documents[0][:200] + "..." if self.documents else None
        }

def main():
    """Fixed demonstration of Smart Kolam RAG System"""

    print("🎨 SMART KOLAM RAG SYSTEM - FIXED VERSION")
    print("=" * 50)

    try:
        # Initialize with simpler settings
        kolam_rag = SmartKolamRAG(
            chunk_size=400,
            chunk_overlap=100,
            top_k_retrieval=3,
            similarity_threshold=0.1
        )

        print("📚 Loading Kolam documentation...")
        kolam_rag.load_kolam_documentation()

        # Debug system
        debug_info = kolam_rag.debug_system()
        print(f"\n🔧 Debug Info:")
        for key, value in debug_info.items():
            print(f"   • {key}: {value}")

        # Get statistics
        stats = kolam_rag.get_kolam_statistics()
        print(f"\n📊 Knowledge Base Statistics:")
        print(f"   • Total documents: {stats['total_documents']}")
        print(f"   • Tamil content: {stats['tamil_content_docs']} docs")
        print(f"   • Data sources: {stats['data_sources']}")

        # Test with simpler queries
        test_queries = [
            "What is Kolam?",
            "Tell me about kolam benefits",
            "How to draw kolam patterns?",
            "What materials are used for kolam?",
            "Kolam cultural significance"
        ]

        print(f"\n🤖 Testing {len(test_queries)} queries...")
        print("=" * 50)

        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Query {i}: {query}")
            print("-" * 40)

            # Execute query with metadata
            result = kolam_rag.smart_query(query, include_metadata=True)

            print(f"💡 Answer:\n{result['answer']}\n")
            print(f"📈 Metrics:")
            print(f"   • Retrieved docs: {result['retrieved_docs']}")
            print(f"   • Confidence: {result['confidence']:.3f}")
            print(f"   • Processing time: {result['processing_time']:.2f}s")

            if 'error' in result:
                print(f"   • Error: {result['error']}")

            # Show context snippets if available
            if 'context_snippets' in result and result['context_snippets']:
                print(f"   • Context preview: {result['context_snippets'][0][:100]}...")

        print("\n" + "=" * 50)
        print("✅ Fixed Smart Kolam RAG Demo Completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
