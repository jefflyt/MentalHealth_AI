#!/bin/bash
# Script to activate the new Python 3.11 conda environment
# Usage: source activate_env.sh

echo "🐍 Activating Python 3.11 Mental Health AI Environment..."
conda activate mentalhealth_py311

echo "✅ Environment activated!"
echo "Python version: $(python --version)"
echo "PyTorch available: $(python -c 'import torch; print("✅ Yes, version", torch.__version__)' 2>/dev/null || echo "❌ No")"
echo "Sentence-transformers available: $(python -c 'import sentence_transformers; print("✅ Yes, version", sentence_transformers.__version__)' 2>/dev/null || echo "❌ No")"
echo ""
echo "🚀 Ready to run mental health AI with re-ranker support!"
echo "Example commands:"
echo "  python app.py"
echo "  python run_web.py"
echo "  python scripts/test/test_reranker.py"