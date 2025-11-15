#!/usr/bin/env bash
# Script to ensure the Python 3.11 conda environment exists and activate it
# Usage: source activate_env.sh

set -euo pipefail

ENV_NAME=mentalhealth_py311
REQUIREMENTS_FILE=requirements.txt

if ! command -v conda >/dev/null 2>&1; then
	echo "❌ Conda is not installed or not on PATH. Please install Miniconda/Anaconda first."
	return 1
fi

echo "🐍 Ensuring Python 3.11 environment ${ENV_NAME} exists..."
if ! conda env list | awk '{print $1}' | grep -xq "${ENV_NAME}"; then
	echo "🛠️  Creating ${ENV_NAME} with Python 3.11.13..."
	conda create -y -n "${ENV_NAME}" python=3.11.13
fi

echo "🚀 Activating ${ENV_NAME}..."
conda activate "${ENV_NAME}"

if [[ -f "${REQUIREMENTS_FILE}" ]]; then
	echo "📦 Installing requirements (if not already present)..."
	pip install -r "${REQUIREMENTS_FILE}" || true
fi

echo "✅ Environment activated!" 
python --version
if python -c 'import torch' &>/dev/null; then
	echo "✅ PyTorch available ($(python -c 'import torch; print(torch.__version__)'))"
else
	echo "⚠️ PyTorch not installed yet. Run 'pip install torch>=2.0.0' after activation."
fi
if python -c 'import sentence_transformers' &>/dev/null; then
	echo "✅ Sentence-transformers available ($(python -c 'import sentence_transformers; print(sentence_transformers.__version__)'))"
else
	echo "⚠️ sentence-transformers not installed yet. Run 'pip install sentence-transformers>=2.2.0' after activation."
fi

echo ""
echo "Ready to run the AI Mental Health app with re-ranker support!"
echo "Example commands:" 
echo "  python app.py"
echo "  python run_web.py"
echo "  python scripts/test/test_reranker.py"