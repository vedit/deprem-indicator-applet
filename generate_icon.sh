#!/bin/bash

# Check if rsvg-convert is installed
if ! command -v rsvg-convert &>/dev/null; then
  echo "Installing librsvg..."
  brew install librsvg
fi

# Generate menu bar icon (22px)
echo "Generating menu bar icon (22px)..."
rsvg-convert -w 22 -h 22 icon.svg >icon.png

# Generate app icon (1024px)
echo "Generating app icon (1024px)..."
rsvg-convert -w 1024 -h 1024 icon.svg >icon_1024.png

echo "Icons generated successfully!"
