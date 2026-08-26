@echo off
title Painel de Ordens de Servico - Technogym
cd /d "%~dp0"

echo ========================================================
echo   Iniciando Painel de Ordens de Servico (Streamlit)...
echo ========================================================
echo.

python -m streamlit run streamlit_app.py

pause
