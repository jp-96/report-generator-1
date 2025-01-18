#!/bin/bash

# Install utils
apt-get update && apt-get install -y \
    unzip \
    fontconfig

# Create the fonts directory
mkdir -p ~/.local/share/fonts

# Navigate to the directory containing your font archives
cd /usr/local/customfonts/archiveipa

# Install Japanese fonts
# ###################################
#   IPA FONT LICENSE AGREEMENT V1.0
# https://moji.or.jp/ipafont/license/
# ###################################
# IPAmj Mincho Font
unzip ipamjm00601.zip -d ~/.local/share/fonts/ipamjm00601 \
# IPAex Font（2 fonts）
unzip IPAexfont00401.zip -d ~/.local/share/fonts/IPAexfont00401 \
# IPA Font（4 fonts）
unzip IPAfont00303.zip -d ~/.local/share/fonts/IPAfont00303 \

# Build font information cache files
fc-cache -vf
