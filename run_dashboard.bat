@echo off
title COVID-19 Risk Prediction & Pandemic Intelligence Platform
echo ====================================================================
echo Starting COVID-19 Risk Prediction & Analytics Dashboard...
echo Using Python environment: C:\Users\Aanshi\AppData\Local\Programs\Python\Python313\python.exe
echo ====================================================================
echo.
"C:\Users\Aanshi\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run app/streamlit_app.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo --------------------------------------------------------------------
    echo [ERROR] The dashboard failed to start.
    echo Please make sure the Python 3.13 environment has all requirements installed.
    echo To install dependencies, run: 
    echo "C:\Users\Aanshi\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt
    echo --------------------------------------------------------------------
    pause
)
