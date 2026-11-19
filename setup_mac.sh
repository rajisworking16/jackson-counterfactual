#!/bin/bash
# Run once from the project root in VS Code's terminal:  bash setup_mac.sh
set -e
cd "$(dirname "$0")"

# Python environment + libraries
python3 -m venv .venv
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
python -m ipykernel install --user --name jackson-counterfactual --display-name "Python (jackson-counterfactual)"

# Git: needs a name and email set once per machine
if [ -z "$(git config --global user.name)" ]; then
  echo "Set your Git identity first:"
  echo '  git config --global user.name "Your Name"'
  echo '  git config --global user.email "you@example.com"'
  exit 1
fi

if [ ! -d .git ]; then
  git init -b main
  git add -A
  git commit -m "Phase 0: project scaffold - data schemas, starter datasets, notebooks"
fi

python -c "import pandas, numpy, streamlit, plotly; print('libraries OK')"
git log --oneline
echo "SETUP DONE. Next: gh repo create jackson-counterfactual --public --source=. --remote=origin --push"
