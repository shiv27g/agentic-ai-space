# Repository for Agentic AI

# Windows - Anaconda Prompt
# Mac - Terminal

# Goto Folder which you have script

```
conda deactivate
pyenv local 3.12.13
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# for conda
conda create --prefix ./env python=3.12 -y
conda activate ./env 
pip install -r requirements.txt

python main.py```