"""
This is a setup.py script generated for the Marmara Deprem application
"""

from setuptools import setup
import os

APP = ["marmara.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": False,
    "iconfile": "icon.icns",
    "plist": {
        "CFBundleName": "Marmara Deprem",
        "CFBundleDisplayName": "Marmara Deprem",
        "CFBundleGetInfoString": "Marmara Denizi Deprem Takip Uygulaması",
        "CFBundleIdentifier": "com.marmara.deprem",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHumanReadableCopyright": "Copyright © 2024, All Rights Reserved",
        "LSUIElement": True,  # This makes it a menu bar app
        "CFBundleIconFile": "icon.icns",  # Specify the icon file in the bundle
    },
    "packages": ["rumps", "requests"],
    "includes": [
        "rumps",
        "requests",
        "idna",
        "chardet",
        "urllib3",
        "certifi",
        "logging",
        "traceback",
        "subprocess",
        "os",
        "hashlib",
    ],
    "excludes": [
        "imp",
        "tkinter",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
    ],
    "resources": ["icon.icns", "icon.png"],  # Include both icon files
}

# Ensure the icon files exist
if not os.path.exists("icon.icns"):
    raise FileNotFoundError("icon.icns file not found")
if not os.path.exists("icon.png"):
    raise FileNotFoundError("icon.png file not found")

setup(
    name="marmara-deprem",
    version="1.0.0",
    description="Marmara Denizi Deprem Takip Uygulaması",
    python_requires=">=3.7",
    install_requires=["rumps>=0.4.0", "requests>=2.31.0"],
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app>=0.28.6"],
)
