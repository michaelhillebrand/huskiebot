#!/bin/bash
set -e

APP_PATH=`pwd`

# Install OS packages
# For Python and the bot framework
sudo apt install nasm pkg-config libopus0 python3 python3-dev python3-venv libffi-dev
# For use by this setup script
sudo apt install unzip

# Install ffmpeg
if type ffmpeg > /dev/null; then
  echo "ffmpeg has already been installed, skipping install"
else
  echo "ffmpeg does not exit on this system, installing"
  mkdir -p ffmpeg
  cd ffmpeg/

  if [[ -d ffmpeg-4.1.3 ]]; then
    echo "ffmpeg-4.1.3 directory already exists, skipping download"
  else
    echo "Getting ffmpeg from source..."
    wget https://ffmpeg.org/releases/ffmpeg-4.1.3.tar.bz2
    tar -xvjf ffmpeg-4.1.3.tar.bz2
  fi

  # Build ffmpeg
  cd ffmpeg-4.1.3/
  ./configure
  make
  sudo make install
  cd $APP_PATH # Use $APP_PATH just to make sure we go back to where we want to
fi

# Set up virtual environment
if [[ -d venv ]]; then
  echo "venv directory already exists, skipping virtualenv creation"
else
  echo "Creating virtualenv"
  python3 -m venv venv
fi
echo "Installing/upgrading dependencies in virtualenv"
source venv/bin/activate
pip install -Ur requirements.txt
deactivate

# Create .env file
cp .template.env .env

# Creates log folder
echo "Creating log folder"
mkdir -p logs

# Install Chrome driver
mkdir -p drivers
if [[ -f drivers/chromedriver ]]; then
  echo "chromedriver already installed, skipping install"
else
  echo "Installing chromedriver"
  wget https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip
  unzip chromedriver_linux64.zip -d drivers/
  rm chromedriver_linux64.zip
fi
