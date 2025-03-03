# First, grab a Unix image with pixi installed
FROM ghcr.io/schmidtdse/base:latest AS base

# Cache buster
ARG CACHE_BUSTER=1

# ARG to note whether this is prod or dev mode
ARG IS_DEVCONTAINER=false
ENV IS_DEVCONTAINER=$IS_DEVCONTAINER

# Set the working directory
WORKDIR /workspaces/non-avian-ml-toy

# Copy the devcontainer scripts into the container
COPY --chown=jovyan:users .devcontainer/scripts .devcontainer/scripts

# Run on build scripts (system dependencies)
RUN .devcontainer/scripts/run_on_build.sh

# Print the current directory (DEBUG)
RUN pwd
RUN ls -la

# Copy pixi env into the container
RUN .devcontainer/scripts/direct_call/verify_or_install_pixi_env.sh

# Copy the rest of the files into the container
COPY --chown=jovyan:users . .

# Handle startup - if run as prod, run the workflow, if not, stay alive
CMD [ ".devcontainer/scripts/handle_startup.sh" ]
