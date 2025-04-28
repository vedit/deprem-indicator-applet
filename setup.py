"""
This is a setup.py script generated for the Marmara Deprem application
"""

from setuptools import setup

APP = ["marmara.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
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
    },
    "packages": ["rumps", "requests"],
    "includes": ["rumps", "requests"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
