#!/bin/bash

# Optional: add timestamp or custom message
message="🚀 Auto-deploy: $(date +'%Y-%m-%d %H:%M')"

# Stage changes
git add .

# Commit with message
git commit -m "$message"

# Push to GitHub
git push origin main
