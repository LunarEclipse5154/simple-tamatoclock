@echo off
echo Installing requirements...
pip install -r requirements.txt

echo Building application...
python build.py

echo Build complete!
echo The executable can be found in the dist folder.
pause 