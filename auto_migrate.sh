#!/bin/bash

# Set environment variables for Flask
export FLASK_APP=buxxel_app.py
export FLASK_ENV=development

# Optional: activate virtual environment if you use one
# source venv/bin/activate

# Timestamp for migration message
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "📦 Running auto-migration at $DATE..."

# Run migration
flask db migrate -m "Auto migration @ $DATE"

# Apply upgrade
flask db upgrade

echo "✅ Migration and upgrade complete."
