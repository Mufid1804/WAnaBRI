#!/bin/bash

# Check if Go is installed
if ! command -v go &> /dev/null
then
    echo "Go is not installed. Please install Go first."
    exit 1
fi

# Install Subfinder
echo "Installing Subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install Httprobe
echo "Installing Httprobe..."
go install github.com/tomnomnom/httprobe@latest

echo "Installation complete!"
