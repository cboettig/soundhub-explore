# First, grab a Unix image with pixi installed
FROM ghcr.io/prefix-dev/pixi:0.39.5-bullseye-slim

# Set the working directory
WORKDIR /workspaces/ocr_extract_nps_tables

# Run on build scripts (system dependencies)
COPY .devcontainer/scripts .devcontainer/scripts
RUN .devcontainer/scripts/run_on_build.sh
