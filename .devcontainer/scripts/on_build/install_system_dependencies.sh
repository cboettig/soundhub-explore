#!/bin/bash

# Install system dependencies, which pdfplumber requires
apt-get update && apt-get install -y \
    \
    \
    && rm -rf /var/lib/apt/lists/*