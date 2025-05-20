#!/bin/bash

set -e

rm -rf gelati.app
pyinstaller --noconfirm --windowed --name gelati \
  --hidden-import=PyQt6.QtCharts \
  --add-data src/gelati/images/gelati_logo2.png:images \
  --add-data src/gelati/images/gelati_logo1.png:images \
  src/gelati/main.py

rm -rf ./build
rm -rf ./gelati.spec
mv ./dist/gelati.app ./
rm -rf ./dist