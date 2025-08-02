#!/bin/bash

echo "🧠 Running safe migration flow for Buxxel..."

# Set environment variables
export FLASK_APP=buxxel_app.py
export FLASK_ENV=development

# Auto-create migrations folder if missing
if [ ! -d "migrations" ]; then
  echo "⚙️ Initializing migrations folder..."
  flask --app buxxel_app.py db init
fi

# Check if 'is_featured' already exists in the DB schema
if sqlite3 buxxel.db "PRAGMA table_info(vendor);" | grep -q "is_featured"; then
  echo "✅ Column 'is_featured' already exists — skipping migration."
else
  # Timestamped message
  DATE=$(date '+%Y-%m-%d %H:%M:%S')
  echo "🛠️ Migrating changes: is_featured missing — adding column @ $DATE"

  flask --app buxxel_app.py db migrate -m "Auto migration @ $DATE"
  flask --app buxxel_app.py db upgrade
fi

echo "🎉 Migration script completed."
