#!/bin/bash

# Cleanup environment
rm -rf build dist venv icon.iconset
rm -f icon.icns icon.png icon_1024.png

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install build dependencies
pip install -r requirements.txt
pip install -e .

# Check if rsvg-convert is installed
if ! command -v rsvg-convert &>/dev/null; then
  echo "Installing librsvg..."
  brew install librsvg
fi

# Generate icons
echo "Generating icons..."
rsvg-convert -w 22 -h 22 icon.svg -o icon.png
rsvg-convert -w 1024 -h 1024 icon.svg -o icon_1024.png

# Create icon.iconset directory
mkdir -p icon.iconset

# Generate different sizes for the app icon
sips -z 16 16 icon_1024.png --out icon.iconset/icon_16x16.png
sips -z 32 32 icon_1024.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32 icon_1024.png --out icon.iconset/icon_32x32.png
sips -z 64 64 icon_1024.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128 icon_1024.png --out icon.iconset/icon_128x128.png
sips -z 256 256 icon_1024.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256 icon_1024.png --out icon.iconset/icon_256x256.png
sips -z 512 512 icon_1024.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512 icon_1024.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon_1024.png --out icon.iconset/icon_512x512@2x.png

# Create .icns file
iconutil -c icns icon.iconset

# Build the application
echo "Building application..."
python setup.py py2app

echo "Build complete! The application is in the dist folder."
