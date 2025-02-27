# First, grab a Unix image with pixi installed
FROM ghcr.io/prefix-dev/pixi:0.41.4-bullseye-slim

# Set the working directory
WORKDIR /workspaces/non-avian-ml-toy

# Run on build scripts (system dependencies)
COPY .devcontainer/scripts .devcontainer/scripts
RUN .devcontainer/scripts/run_on_build.sh
