#!/bin/bash

sudo apt install nasm pkg-config libopus0 python3-venv
mkdir ffmpeg
cd ffmpeg/
wget https://ffmpeg.org/releases/ffmpeg-4.1.3.tar.bz2
tar -xvjf ffmpeg-4.1.3.tar.bz2
cd ffmpeg-4.1.3/
./configure
make
sudo make install
cd ../../
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .template.env .env