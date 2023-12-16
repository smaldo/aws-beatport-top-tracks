#!/bin/bash

#Layer
LAYER_NAME=hello

# Requirements file
REQ_FILE="requirements.txt"

# Layer directory
LAYER_DIR="python"

# Python version
PYTHON_VERSION="python3.9"

cd $LAYER_NAME
# Create a folder for the layer
mkdir -p $LAYER_DIR/lib/$PYTHON_VERSION/site-packages/

# Install packages from requirements.txt into the layer folder
pip3 install -r $REQ_FILE -t $LAYER_DIR/lib/$PYTHON_VERSION/site-packages/
