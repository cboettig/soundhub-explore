# First, grab a Unix image with pixi installed - courtesy of Carl
FROM ghcr.io/schmidtdse/base:latest

# Set the default user as jovyan for Jupyter
USER jovyan

# Set the working directory
WORKDIR /workspaces/non-avian-ml-toy

# Copy the repo into the container
COPY . .

# Run on build scripts (system dependencies and pixi env)
# COPY .devcontainer/scripts .devcontainer/scripts
RUN .devcontainer/scripts/run_on_build.sh
