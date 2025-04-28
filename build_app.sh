#!/bin/bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Convert SVG to ICNS
if ! command -v rsvg-convert &>/dev/null; then
  echo "Installing librsvg..."
  brew install librsvg
fi

# Convert SVG to PNG
rsvg-convert -w 1024 -h 1024 icon.svg >icon_1024.png

# Create ICNS file
mkdir icon.iconset
sips -z 16 16 icon_1024.png --out icon.iconset/icon_16x16.png
sips -z 32 32 icon_1024.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32 icon_1024.png --out icon.iconset/icon_32x32.png
sips -z 64 64 icon_1024.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128 icon_1024.png --out icon.iconset/icon_128x128.png
sips -z 256 256 icon_1024.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256 icon_1024.png --out icon.iconset/icon_256x256.png
sips -z 512 512 icon_1024.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512 icon_1024.png --out icon.iconset/icon_512x512.png
cp icon_1024.png icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset

# Build the application
python setup.py py2app

# Clean up
rm -rf icon.iconset
rm icon_1024.png

echo "Build complete! The application is in the dist folder."
