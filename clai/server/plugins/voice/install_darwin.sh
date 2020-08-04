#!/usr/bin/env bash


echo "==============================================================="
echo ""
echo " Phase 1: Installing necessary tools"
echo ""
echo "==============================================================="

if [[ $(command -v brew) == "" ]]; then
    echo ">> Installing Hombrew"
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    echo ">> Updating Homebrew"
    brew update
fi

# Install ffmpeg
echo ">> Installing ffmpeg"
if brew ls --versions ffmpeg > /dev/null; then
  brew ls --versions ffmpeg
else
  brew install ffmpeg > /dev/null
fi

# Install Python3 dependencies
echo ">> Installing python dependencies"

python3 -m pip install -r requirements.txt 2> /dev/null
