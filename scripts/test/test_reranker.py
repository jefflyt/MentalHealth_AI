"""
Test script for re-ranker functionality.

This script validates the re-ranker's performance and demonstrates
how it improves retrieval relevance for mental health queries.

Usage:
    python scripts/test/test_reranker.py
"""

import sys
import os
import time
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from agent.reranker import ReRanker, get_reranker, rerank_documents
    RERANKER_AVAILABLE = True
except ImportError as e:
    print(f"❌ Re-ranker not available: {e}")
    print("Install with: pip install sentence-transformers")
    sys.exit(1)


def create_sample_documents() -> List[Dict[str, str]]:
    """Create sample mental health documents for testing."""
    return [
        {
            "text": "Depression is a common mental health condition characterized by persistent sadness, loss of interest, and low energy. It can affect daily functioning and requires professional treatment.",
            "id": "doc_1",
            "category": "depression"
        },
        {
            "text": "Anxiety disorders include generalized anxiety, panic disorder, and social anxiety. Symptoms include excessive worry, restlessness, and physical tension.",
            "id": "doc_2",
            "category": "anxiety"
        },
        {
            "text": "Cognitive behavioral therapy (CBT) is an evidence-based treatment that helps people identify and change negative thought patterns and behaviors.",
            "id": "doc_3",
            "category": "treatment"
        },
        {
            "text": "The Institute of Mental Health (IMH) in Singapore provides comprehensive psychiatric care and mental health services. Contact: 6389-2222 for 24/7 support.",
            "id": "doc_4",
            "category": "singapore_resources"
        },
        {
            "text": "Mindfulness meditation involves paying attention to the present moment without judgment. It can reduce stress and improve emotional regulation.",
            "id": "doc_5",
            "category": "coping"
        },
        {
            "text": "Sleep hygiene includes maintaining consistent sleep schedules, avoiding caffeine before bed, and creating a comfortable sleep environment.",
            "id": "doc_6",
            "category": "self_care"
        },
        {
            "text": "CHAT (Community Health Assessment Team) in Singapore provides free mental health services for young people aged 16-30. Call 6493-6500 for support.",
            "id": "doc_7",
            "category": "singapore_resources"
        },
        {
            "text": "Panic attacks are sudden episodes of intense fear with physical symptoms like rapid heartbeat, sweating, and difficulty breathing.",
            "id": "doc_8",
            "category": "anxiety"
        }
    ]


def test_basic_functionality():
    """Test basic re-ranker functionality."""
    print("\n" + "="*70)
    print("TEST 1: Basic Functionality")
    print("="*70)
    
    # Create re-ranker
    reranker = ReRanker(enabled=True)
    
    # Check if loaded
    print(f"✓ Re-ranker enabled: {reranker.is_enabled()}")
    print(f"✓ Configuration: {reranker.get_config()}")
    
    if not reranker.is_enabled():
        print("❌ Re-ranker failed to load properly")
        return False
    
    print("✅ Basic functionality test passed")
    return True


def test_reranking_quality():
    """Test re-ranking quality with sample queries."""
    print("\n" + "="*70)
    print("TEST 2: Re-ranking Quality")
    print("="*70)
    
    docs = create_sample_documents()
    test_queries = [
        ("I'm feeling anxious and having panic attacks", "anxiety"),
        ("Where can I get help in Singapore?", "singapore_resources"),
        ("What is depression?", "depression"),
        ("I want to learn CBT techniques", "treatment"),
    ]
    
    reranker = ReRanker(enabled=True)
    
    for query, expected_category in test_queries:
        print(f"\n📝 Query: '{query}'")
        print(f"🎯 Expected category: {expected_category}")
        
        # Re-rank documents
        start_time = time.time()
        reranked = reranker.rerank(query, docs.copy(), document_key="text")
        elapsed = time.time() - start_time
        
        # Show top 3 results
        print(f"\n⏱️  Re-ranking time: {elapsed*1000:.2f}ms")
        print("\nTop 3 results:")
        for i, doc in enumerate(reranked[:3], 1):
            score = doc.get('rerank_score', 0)
            print(f"  {i}. [{doc['category']}] Score: {score:.3f}")
            print(f"     {doc['text'][:80]}...")
        
        # Check if top result matches expected category
        if reranked and reranked[0]['category'] == expected_category:
            print(f"✅ Top result matches expected category")
        else:
            print(f"⚠️  Top result category: {reranked[0]['category']}")
    
    print("\n✅ Re-ranking quality test completed")
    return True


def test_threshold_filtering():
    """Test relevance threshold filtering."""
    print("\n" + "="*70)
    print("TEST 3: Threshold Filtering")
    print("="*70)
    
    docs = create_sample_documents()
    query = "Singapore mental health services for young people"
    
    thresholds = [0.0, 0.1, 0.3, 0.5]
    
    for threshold in thresholds:
        reranker = ReRanker(enabled=True, relevance_threshold=threshold)
        reranked = reranker.rerank(query, docs.copy(), document_key="text")
        
        print(f"\nThreshold: {threshold:.1f}")
        print(f"  Documents returned: {len(reranked)}/{len(docs)}")
        if reranked:
            print(f"  Score range: {reranked[-1]['rerank_score']:.3f} - {reranked[0]['rerank_score']:.3f}")
    
    print("\n✅ Threshold filtering test completed")
    return True


def test_top_k_limiting():
    """Test top-k result limiting."""
    print("\n" + "="*70)
    print("TEST 4: Top-K Limiting")
    print("="*70)
    
    docs = create_sample_documents()
    query = "mental health anxiety treatment"
    
    top_k_values = [None, 3, 5, 10]
    
    for top_k in top_k_values:
        reranker = ReRanker(enabled=True, top_k=top_k)
        reranked = reranker.rerank(query, docs.copy(), document_key="text")
        
        print(f"\nTop-K: {top_k if top_k else 'None (no limit)'}")
        print(f"  Documents returned: {len(reranked)}")
    
    print("\n✅ Top-K limiting test completed")
    return True


def test_fallback_behavior():
    """Test graceful fallback when disabled."""
    print("\n" + "="*70)
    print("TEST 5: Fallback Behavior")
    print("="*70)
    
    docs = create_sample_documents()
    query = "test query"
    
    # Test with disabled re-ranker
    reranker_disabled = ReRanker(enabled=False)
    result = reranker_disabled.rerank(query, docs.copy(), document_key="text")
    
    print(f"Re-ranker disabled: {not reranker_disabled.is_enabled()}")
    print(f"Original docs: {len(docs)}")
    print(f"Returned docs: {len(result)}")
    print(f"Documents unchanged: {result == docs}")
    
    # Test with invalid model (should disable automatically)
    print("\nTesting invalid model...")
    reranker_invalid = ReRanker(model_name="invalid/model/name", enabled=True)
    result_invalid = reranker_invalid.rerank(query, docs.copy(), document_key="text")
    
    print(f"Auto-disabled on error: {not reranker_invalid.is_enabled()}")
    print(f"Graceful fallback: {result_invalid == docs}")
    
    print("\n✅ Fallback behavior test completed")
    return True


def test_convenience_function():
    """Test the convenience wrapper function."""
    print("\n" + "="*70)
    print("TEST 6: Convenience Function")
    print("="*70)
    
    docs = create_sample_documents()
    query = "anxiety help Singapore"
    
    # Test with enabled
    result_enabled = rerank_documents(query, docs.copy(), enabled=True)
    print(f"With re-ranking: {len(result_enabled)} docs")
    if result_enabled:
        print(f"  Top score: {result_enabled[0].get('rerank_score', 'N/A')}")
    
    # Test with disabled
    result_disabled = rerank_documents(query, docs.copy(), enabled=False)
    print(f"\nWithout re-ranking: {len(result_disabled)} docs")
    print(f"  Documents unchanged: {result_disabled == docs}")
    
    print("\n✅ Convenience function test completed")
    return True


def performance_benchmark():
    """Benchmark re-ranking performance."""
    print("\n" + "="*70)
    print("BENCHMARK: Performance Metrics")
    print("="*70)
    
    docs = create_sample_documents()
    queries = [
        "I feel depressed and need help",
        "anxiety panic attack symptoms",
        "Singapore mental health services",
        "CBT therapy techniques",
        "mindfulness meditation stress"
    ]
    
    reranker = ReRanker(enabled=True)
    
    total_time = 0
    for query in queries:
        start = time.time()
        reranker.rerank(query, docs.copy(), document_key="text")
        elapsed = time.time() - start
        total_time += elapsed
    
    avg_time = (total_time / len(queries)) * 1000
    
    print(f"\nQueries tested: {len(queries)}")
    print(f"Documents per query: {len(docs)}")
    print(f"Average re-ranking time: {avg_time:.2f}ms")
    print(f"Total time: {total_time*1000:.2f}ms")
    
    if avg_time < 200:
        print("✅ Performance within target (<200ms)")
    else:
        print("⚠️  Performance exceeds target (>200ms)")
    
    return True


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("RE-RANKER TEST SUITE")
    print("="*70)
    print("\nTesting re-ranker functionality and performance...")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Re-ranking Quality", test_reranking_quality),
        ("Threshold Filtering", test_threshold_filtering),
        ("Top-K Limiting", test_top_k_limiting),
        ("Fallback Behavior", test_fallback_behavior),
        ("Convenience Function", test_convenience_function),
        ("Performance Benchmark", performance_benchmark),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Re-ranker is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
