#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
else
    OS="Unknown"
fi

if [[ "$(uname -m)" == "x86_64" ]]; then
    ARCH="64-bit"
else
    ARCH="32-bit"
fi

echo "Detected OS: $OS"
echo "Detected Architecture: $ARCH"

if [[ "$OS" == "Linux" && "$ARCH" == "64-bit" ]]; then
    echo "Downloading geckodriver for Linux 64-bit..."
    wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
    tar -xzf geckodriver.tar.gz
    GECKO_PATH="$(pwd)/geckodriver"
    echo "Downloaded file path: $GECKO_PATH"
elif [[ "$OS" == "Windows" && "$ARCH" == "64-bit" ]]; then
    echo "Downloading geckodriver for Windows 64-bit..."
    wget -O geckodriver.zip https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-win-aarch64.zip
    unzip geckodriver.zip
    GECKO_PATH="$(pwd)/geckodriver.exe"
    echo "Downloaded file path: $GECKO_PATH"
else
    echo "Unsupported OS or architecture"
fi

echo "$GECKO_PATH" > geco.txt
