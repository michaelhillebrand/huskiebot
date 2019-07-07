#!/bin/bash
set -e

APP_PATH=`pwd`

# Install OS packages
sudo apt install nasm pkg-config libopus0 python3-venv

# Install ffmpeg
if type blah > /dev/null; then
  echo "ffmpeg has already been installed, skipping"
else
  echo "ffmpeg does not exit on this system"
  mkdir -p ffmpeg
  cd ffmpeg/

  if [[ -d ffmpeg-4.1.3 ]]; then
    echo "ffmpeg-4.1.3 directory already exists"
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
  echo "venv directory already exists"
else
  echo "Creating virtualenv"
  python3 -m venv venv
fi
source venv/bin/activate
pip install -Ur requirements.txt
deactivate

# Create .env file
cp .template.env .env
