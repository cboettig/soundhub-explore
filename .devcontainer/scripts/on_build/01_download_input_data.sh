#!/bin/bash

# Check if the directory exists
if [ ! -d "/workspaces/non-avian-ml-toy" ]; then
    mkdir -p /workspaces/non-avian-ml-toy
fi

# Download data if not already present
if [ ! -f "/workspaces/non-avian-ml-toy/data.zip" ]; then
    echo "Downloading input data..."
    curl -L -o /workspaces/non-avian-ml-toy/data.zip "https://storage.googleapis.com/dse-staff-public/data.zip"
fi

# Verify download before unzipping
if [ -f "/workspaces/non-avian-ml-toy/data.zip" ]; then
    echo "Unzipping data..."
    unzip -o /workspaces/non-avian-ml-toy/data.zip -d /workspaces/non-avian-ml-toy/
    rm /workspaces/non-avian-ml-toy/data.zip
    echo "Data extraction complete!"
else
    echo "Download failed. File not found!"
    exit 1
fi