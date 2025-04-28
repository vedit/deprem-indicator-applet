# Marmara Deprem Indicator

A macOS menu bar application that monitors and displays earthquake information from the Marmara Sea region.

## Features

- Shows the latest earthquake information in the menu bar
- Displays notifications for new earthquakes
- Provides earthquake statistics
- Updates automatically every 60 seconds

## Installation

1. Make sure you have Python 3.7+ installed on your system
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python marmara.py
   ```

## Usage

The application will appear in your macOS menu bar. Click on the icon to:
- View the latest earthquake information
- Check earthquake statistics
- Quit the application

## Requirements

- macOS 10.12 or later
- Python 3.7 or later
- rumps
- requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Data is scraped from [Kandilli Rasathanesi website](http://www.koeri.boun.edu.tr/scripts/lst4.asp) in 60 second intervals 

Images
-----
Last Earthquake:


![Last Marmara Earthquake](https://github.com/vedit/deprem-indicator-applet/raw/master/images/last_eq.png "Last Earthquake")


Marmara Earthquake Stats:


![Marmara Earthquake Stats](https://github.com/vedit/deprem-indicator-applet/raw/master/images/eq_stats.png "Marmara Earthquake Stats")
