@echo off
py -3 -m pip install --upgrade pip
py -3 -m pip install -r requirements.txt
py -3 -m PyInstaller --noconfirm --clean --onefile --windowed --name AutoTuneAI app.py
echo EXE: dist\AutoTuneAI.exe
pause
