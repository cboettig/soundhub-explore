# Training non-avian sound classifiers

This is a toy example using the `opensoundscapes` package as a wrapper to create custom classifiers for models pre-trained with bird embeddings.  The bird models we will be using first are `BirdNet` and Google's `Perch` model.  

### Next steps

We will complete the following throughout this semester: 

- Learn to run the exploratory notebook `train_on_embeddings.ipynb` to create and test a custom classifer
- Create custom classifiers using ONNX formatted pre-trained models instead of `opensoundscapes`
- Create an approach for using stratified k-fold cross validation on multiple audio sample directories
- Refactor code to be a python module that runs on startup
- Send jobs to a super computer for iteration with various parameters
- Experiment with new model architectures and data augmentation techniques
- Write a report that compares approaches and results! :rocket:


## Development Container 

Note: This repository contains a development container that can be used both locally with `VSCode`, on the cloud with `GitHub Codespaces`, or any combination of cloud backend and IDE using `DevPod`!

## Prerequisites

### Local

- [VS Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [VS Code Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Cloud

- A GitHub account (for using GitHub Codespaces)

OR

- DevPod set up locally and configured to an appropriate cloud backend (more detail on this later!).


## Getting Started

### Using GitHub Codespaces

1. Click the "Code" button on the repository page
2. Select "Open with Codespaces"
3. Click "New codespace" (you can change the machine type here as well)
4. Wait for the environment to build and initialize

### Using VS Code + Docker Locally

1. Clone the repository:
```sh
git clone https://github.com/username/repo-name.git
cd repo-name
```

2. Open in VS Code:
```sh
code .
```

3. When prompted "Reopen in Container", click "Reopen in Container"
   - Or press `CMD + Shift + P`, type "Remote-Containers: Reopen in Container"

## Project Structure

```
.
├── .devcontainer/          # Development container configuration
├── .vscode/               # VS Code settings, primarily for debugger launch configs
├── data/                  # Data storage - ignored by `git`!
│   ├── audio/...
├── exploratory/          # Jupyter notebooks for interactive work
├── src/                  # Source code - sourced as a python module (incomplete)
└── pixi.toml             # Pixi dependencies and settings
```

## Getting Data

Data can be stored in the `data/` directory. This directory is ignored by `git`, so you can store large files here without worrying about them being committed to the repository. This is useful for storing data that is too large to be stored in the repository, or for storing sensitive data that you don't want to share.

By default, we download the data used for this toy-ish example from a public GCP bucket, within `.devcontainer/scripts/post_create/download_input_data.sh`. This script is run by `.devcontainer/scripts/run_post_create.sh` after the container is created.

## Managing Dependencies

The container will automatically install all required system dependencies and Python packages during the build process.

Additional system dependencies can be added to `.devcontainer/scripts/on_build/install_system_dependencies.sh` - or, to keep things cleaner, you can break up installs across multiple scripts. These will be called in order of their filenames, by `.devcontainer/scripts/run_on_build.sh`. This is performed during the `Docker` build process, so it's a good place to put things like `apt-get` installs.

After the container builds, `Python` dependecies are installed by `pixi`, using the `pixi.toml` and `pixi.lock` files. In order to add a new dependency here, you can either add it manually to the `pixi.toml` file, or use the `pixi` CLI to add it. For example, to add `numpy`:

```sh
pixi add numpy
```