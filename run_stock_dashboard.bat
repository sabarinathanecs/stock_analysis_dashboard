@echo off
cd /d "%~dp0"

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Converting YAML files to CSV...
cd scripts
python extract_yaml_to_csv.py

echo.
echo Launching Streamlit dashboard...
cd ..\dashboard
streamlit run app.py

pause
