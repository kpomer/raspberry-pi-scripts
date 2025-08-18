#!/bin/bash

# Ensure we are inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Error: Not inside a git repository."
    exit 1
fi

# cd to the root of the repo (so the script works no matter where it’s stored/run)
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT" || { echo "Failed to cd into repo root"; exit 1; }

echo "Repo: $REPO_ROOT"
echo "Pulling latest changes from 'main'..."
git pull origin main

# Check the exit status of the git pull command
if [ $? -eq 0 ]; then
    echo "Successfully pulled latest changes."
else
    echo "Failed to pull changes. Please check for conflicts or network issues."
fi