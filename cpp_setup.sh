#!/bin/sh

# Step 1: Install Command Line Tools
echo "Installing Command Line Tools..."
xcode-select --install

# Optional Step 2: Install Xcode
echo "To install Xcode, please visit the Apple App Store and search for 'Xcode'. Download and install it there."

# Step 3: Install Homebrew
echo "Installing Homebrew..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

echo "Adding Homebrew to PATH..."
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

echo "Updating and checking Homebrew..."
brew update
brew doctor

# Step 4: Install GCC
echo "Installing GCC..."
brew install gcc

echo "Adding GCC to PATH..."
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Step 5: Verify the installation
echo "GCC Installation Information:"
gcc --version

echo "The C++ environment is now set up on your M1 MacBook Pro."
