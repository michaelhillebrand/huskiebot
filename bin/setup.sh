#!/bin/bash
set -e

APP_PATH=`pwd`

# Install OS packages
# For Python and the bot framework
sudo apt install nasm pkg-config libopus0 python3 python3-dev python3-venv libffi-dev
# For use by this setup script
sudo apt install unzip
# For use by the chromedriver
sudo apt install libnss3 

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
if [[ -f .env ]]; then
  echo ".env file already created, skipping"
else
  echo "Creating .env file from template"
  cp .template.env .env
fi

# Creates log folder
echo "Creating log folder"
mkdir -p logs

# Install Chrome driver
mkdir -p drivers
if [[ -f drivers/chromedriver ]]; then
  echo "chromedriver already installed, skipping install"
else
  echo "Installing chromedriver"
  cd drivers
  wget https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip
  unzip chromedriver_linux64.zip
  rm chromedriver_linux64.zip
  cd $APP_PATH
fi

# Install Chrome
if type google-chrome > /dev/null; then
  echo "google-chrome already installed, skipping install"
else
  echo "google-chrome does not exit on this system, installing"
  mkdir -p google-chrome

  if [[ -f google-chrome/google-chrome-stable_current_amd64.deb ]]; then
    echo "google-chrome .deb file already exists, skipping download"
  else
    echo "Getting google-chrome from repository..."
    cd google-chrome
    # wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add - # Get apt installation key
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    # Attempt to install, it will probably fail due to missing dependencies
    # But we don't want the whole script to fail out. Putting it in a conditional makes it not fail out even though we have `set -e` set
    # plus, when using &&, the first command maintains the exit code so we can still check it
    sudo dpkg -i google-chrome-stable_current_amd64.deb && true
    if [[ $? -ne 0 ]]; then # the install failed
      sudo apt -f install # lets have apt fix the install by installing the necessary dependencies
      sudo dpkg -i google-chrome-stable_current_amd64.deb # rerun the install, if it fails this time, we want the script to fail
    fi
    cd $APP_PATH
    rm -r google-chrome
  fi
fi
