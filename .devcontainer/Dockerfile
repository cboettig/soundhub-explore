# First, grab a Unix image with pixi installed
FROM ghcr.io/schmidtdse/base:latest AS base

# ARG to note whether this is prod or dev mode
ARG IS_DEVCONTAINER=false
ENV IS_DEVCONTAINER=$IS_DEVCONTAINER

# Set the working directory
WORKDIR /workspaces/non-avian-ml-toy

# Copy the repository into the container
COPY --chown=jovyan:users . .

# Run on build scripts (system dependencies)
RUN .devcontainer/scripts/run_on_build.sh

# Copy pixi env into the container
COPY --chown=jovyan:users .pixi .pixi

# Handle startup - if run as prod, run the workflow, if not, stay alive
CMD [ ".devcontainer/scripts/handle_startup.sh" ]
