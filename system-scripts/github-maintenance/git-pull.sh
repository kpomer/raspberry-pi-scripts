#!/bin/bash

# This script navigates to the raspberry-pi-scripts repository
# and pulls the latest changes from the 'main' branch on GitHub.

# --- Configuration ---
# Path to local raspberry-pi-scripts repo
REPO_PATH="/home/kevinpomer/Code/Github/raspberry-pi-scripts"

# --- Script Logic ---

echo "Attempting to pull latest changes for raspberry-pi-scripts..."

# Check if the repository directory exists
if [ ! -d "$REPO_PATH" ]; then
    echo "Error: Repository directory not found at $REPO_PATH"
    echo "Please ensure the REPO_PATH variable in the script is correct."
    exit 1
fi

# Navigate to the repository directory
cd "$REPO_PATH"

# Check if it's a Git repository
if [ ! -d ".git" ]; then
    echo "Error: Not a Git repository at $REPO_PATH"
    echo "Please ensure you have cloned the repository correctly."
    exit 1
fi

# Perform the git pull operation
git pull origin main

# Check the exit status of the git pull command
if [ $? -eq 0 ]; then
    echo "Successfully pulled latest changes."
else
    echo "Failed to pull changes. Please check for conflicts or network issues."
fi