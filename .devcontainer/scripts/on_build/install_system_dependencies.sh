#!/bin/bash

# Install system dependencies, which pdfplumber requires
apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*