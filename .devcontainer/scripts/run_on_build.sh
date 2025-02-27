#!/bin/bash

DIR=".devcontainer/scripts/on_build"

for script in "$DIR"/*.sh; do
    if [ -f "$script" ]; then
        echo "=== Executing $script ==="
        bash "$script"
        
        # Check exit status
        if [ $? -eq 0 ]; then
            echo "✓ $script completed successfully"
        else
            echo "❌ $script failed with exit code $?"
        fi
        echo
    fi
done