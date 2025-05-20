
pyinstaller --noconfirm --windowed --name gelati --hidden-import=PyQt6.QtCharts --add-data src/gelati/images/gelati_logo2.png:images --add-data src/gelati/images/gelati_logo1.png:images src/gelati/main.py

rmdir /s /q build
del /f gelati.spec
move dist\gelati\gelati.app .\
rmdir /s /q dist