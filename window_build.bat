
pyinstaller --noconfirm --windowed --name gelati --hidden-import=PyQt6.QtCharts --add-data src/gelati/images/gelati_logo2.png:images --add-data src/gelati/images/gelati_logo1.png:images src/gelati/main.py

@REM rmdir /s /q build
@REM del /f gelati.spec
@REM move dist\gelati.app .\
@REM rmdir /s /q dist