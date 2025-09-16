"""
Example usage script for Smart Kolam RAG System
Demonstrates various ways to interact with the RAG pipeline
"""

from smart_kolam_rag import SmartKolamRAG
import time

def demonstrate_basic_usage():
    """Demonstrate basic RAG system usage"""
    print("🎨 KOLAM RAG SYSTEM - EXAMPLE USAGE")
    print("=" * 50)
    
    # Initialize the system
    print("🚀 Initializing Smart Kolam RAG...")
    kolam_rag = SmartKolamRAG(
        chunk_size=400,
        chunk_overlap=100,
        top_k_retrieval=3,
        similarity_threshold=0.1
    )
    
    # Load documentation
    print("📚 Loading Kolam documentation...")
    kolam_rag.load_kolam_documentation()
    
    # Get system statistics
    stats = kolam_rag.get_kolam_statistics()
    print(f"\n📊 Knowledge Base Statistics:")
    print(f"   • Total documents: {stats['total_documents']}")
    print(f"   • Tamil content: {stats['tamil_content_docs']} docs")
    print(f"   • Data sources: {len(stats['data_sources'])}")
    
    return kolam_rag

def test_various_queries(kolam_rag):
    """Test different types of queries"""
    
    queries = [
        # Basic information
        {
            "query": "What is Kolam?",
            "category": "Basic Information"
        },
        
        # Cultural significance
        {
            "query": "What is the cultural significance of Kolam in Tamil tradition?",
            "category": "Cultural Context"
        },
        
        # Technical aspects
        {
            "query": "What are the different types of Kolam patterns?",
            "category": "Technical Details"
        },
        
        # Materials and methods
        {
            "query": "What materials are used to draw Kolam?",
            "category": "Materials & Methods"
        },
        
        # Benefits and applications
        {
            "query": "How does drawing Kolam benefit cognitive development?",
            "category": "Benefits & Applications"
        },
        
        # Festivals and occasions
        {
            "query": "When is Kolam traditionally drawn during festivals?",
            "category": "Festivals & Occasions"
        }
    ]
    
    print(f"\n🤖 Testing {len(queries)} different query types...")
    print("=" * 50)
    
    for i, query_info in enumerate(queries, 1):
        query = query_info["query"]
        category = query_info["category"]
        
        print(f"\n🔍 Query {i} ({category}):")
        print(f"Question: {query}")
        print("-" * 40)
        
        # Execute query with metadata
        start_time = time.time()
        result = kolam_rag.smart_query(query, include_metadata=True)
        
        print(f"💡 Answer:")
        print(f"{result['answer']}\n")
        
        print(f"📈 Metrics:")
        print(f"   • Retrieved docs: {result['retrieved_docs']}")
        print(f"   • Confidence: {result['confidence']:.3f}")
        print(f"   • Processing time: {result['processing_time']:.2f}s")
        print(f"   • Has Tamil content: {result.get('has_tamil_content', False)}")
        
        if 'error' in result:
            print(f"   • Error: {result['error']}")
        
        # Show a snippet of retrieved context
        if 'context_snippets' in result and result['context_snippets']:
            snippet = result['context_snippets'][0][:150]
            print(f"   • Context preview: {snippet}...")

def test_tamil_queries(kolam_rag):
    """Test Tamil language queries"""
    
    print(f"\n🇮🇳 Testing Tamil Language Queries...")
    print("=" * 50)
    
    tamil_queries = [
        "கோலம் என்றால் என்ன?",
        "கோலம் வரைவதால் என்ன நன்மைகள்?",
        "கோலத்தின் வகைகள் என்னென்ன?"
    ]
    
    for i, query in enumerate(tamil_queries, 1):
        print(f"\n🔍 Tamil Query {i}: {query}")
        print("-" * 40)
        
        result = kolam_rag.smart_query(query)
        
        print(f"💡 Answer:")
        print(f"{result['answer']}\n")
        
        print(f"📈 Metrics:")
        print(f"   • Confidence: {result['confidence']:.3f}")
        print(f"   • Processing time: {result['processing_time']:.2f}s")

def test_edge_cases(kolam_rag):
    """Test edge cases and error handling"""
    
    print(f"\n🧪 Testing Edge Cases...")
    print("=" * 50)
    
    edge_cases = [
        "",  # Empty query
        "   ",  # Whitespace only
        "What is quantum physics?",  # Unrelated query
        "Tell me about machine learning algorithms",  # Another unrelated query
    ]
    
    for i, query in enumerate(edge_cases, 1):
        print(f"\n🔍 Edge Case {i}: '{query}'")
        print("-" * 40)
        
        result = kolam_rag.smart_query(query)
        
        print(f"💡 Answer:")
        print(f"{result['answer']}\n")
        
        if 'error' in result:
            print(f"❌ Error handled: {result['error']}")

def interactive_mode(kolam_rag):
    """Interactive query mode"""
    
    print(f"\n💬 Interactive Mode - Ask questions about Kolam!")
    print("Type 'quit' to exit, 'stats' for statistics, 'debug' for debug info")
    print("=" * 50)
    
    while True:
        try:
            query = input("\n🤔 Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif query.lower() == 'stats':
                stats = kolam_rag.get_kolam_statistics()
                print(f"\n📊 Statistics:")
                for key, value in stats.items():
                    print(f"   • {key}: {value}")
                continue
            elif query.lower() == 'debug':
                debug_info = kolam_rag.debug_system()
                print(f"\n🔧 Debug Info:")
                for key, value in debug_info.items():
                    print(f"   • {key}: {value}")
                continue
            elif not query:
                print("Please enter a question about Kolam.")
                continue
            
            # Process the query
            result = kolam_rag.smart_query(query, include_metadata=True)
            
            print(f"\n💡 Answer:")
            print(f"{result['answer']}")
            
            print(f"\n📈 Quick Stats:")
            print(f"   • Confidence: {result['confidence']:.3f}")
            print(f"   • Retrieved docs: {result['retrieved_docs']}")
            print(f"   • Time: {result['processing_time']:.2f}s")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main demonstration function"""
    
    try:
        # Initialize and demonstrate basic usage
        kolam_rag = demonstrate_basic_usage()
        
        # Test various query types
        test_various_queries(kolam_rag)
        
        # Test Tamil language queries
        test_tamil_queries(kolam_rag)
        
        # Test edge cases
        test_edge_cases(kolam_rag)
        
        # Ask user if they want interactive mode
        print(f"\n" + "=" * 50)
        print("✅ Demonstration completed!")
        
        user_input = input("\n💬 Would you like to try interactive mode? (y/n): ").strip().lower()
        if user_input in ['y', 'yes']:
            interactive_mode(kolam_rag)
        
        print("\n🎨 Thank you for trying the Smart Kolam RAG System!")
        
    except Exception as e:
        print(f"❌ Error in demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
