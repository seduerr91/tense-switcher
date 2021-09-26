#!/bin/bash
echo $PWD

echo "Installing Dependencies"
rm -rf env
python3 -m venv env
source env/bin/activate

pip3 install -r requirements.txt
python3 -m spacy download en_core_web_sm

echo "Fixing Bug of Tool"

rm ./env/lib/python3.9/site-packages/pattern/text/__init__.py
cp bugfix/__init__.py ./env/lib/python3.9/site-packages/pattern/text/__init__.py

# bash tree.sh

echo $PWD

python3 prepare_data.py
python3 app.py
