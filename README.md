# Marmara Deprem Indicator

A macOS menu bar application that monitors and displays earthquake information from the Marmara Sea region.

An unmaintained Linux GTK version can be found in `gtk` branch

## Features

- Shows the latest earthquake information in the menu bar
- Displays notifications for new earthquakes
- Provides earthquake statistics
- Updates automatically every 60 seconds

## Installation

### From Source

1. Make sure you have Python 3.12+ installed on your system
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python marmara.py
   ```

### Building macOS Application

To build a standalone macOS application:

1. Make sure you have the required tools installed:
   ```bash
   brew install librsvg
   ```

2. Run the build script:
   ```bash
   chmod +x build_app.sh
   ./build_app.sh
   ```

3. The built application will be in the `dist` folder. You can drag it to your Applications folder.

## Usage

The application will appear in your macOS menu bar. Click on the icon to:
- View the latest earthquake information
- Check earthquake statistics
- Test notifications
- Quit the application

## Requirements

- macOS 10.12 or later
- Python 3.12 or later
- rumps
- requests
- py2app (for building the application)

## Building from Source

If you want to build the application yourself:

1. Install the build dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```bash
   ./build_app.sh
   ```

The application will be built in the `dist` folder.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Data is scraped from [Kandilli Rasathanesi website](http://www.koeri.boun.edu.tr/scripts/lst4.asp) in 60 second intervals 

Images
-----
Last Earthquake:


![Last Marmara Earthquake](https://github.com/vedit/deprem-indicator-applet/raw/master/images/last_eq.png "Last Earthquake")


Marmara Earthquake Stats:


![Marmara Earthquake Stats](https://github.com/vedit/deprem-indicator-applet/raw/master/images/eq_stats.png "Marmara Earthquake Stats")
