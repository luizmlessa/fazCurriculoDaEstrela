@echo off
title Faz Curriculo da Estrela
cd /d "%~dp0"

echo ========================================
echo   Faz Curriculo da Estrela
echo ========================================
echo.

REM === 1. Verifica se o Ollama esta rodando ===
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Ollama ja esta rodando
) else (
    echo [..] Iniciando Ollama em modo CPU...
    set OLLAMA_GPU_LAYERS=0
    start "Ollama" /MIN cmd /c "ollama serve"
    timeout /t 5 /nobreak >NUL
    echo [OK] Ollama iniciado
)

REM === 2. Verifica se o modelo esta disponivel ===
echo [..] Verificando modelo qwen2.5:14b...
ollama list | find "qwen2.5:14b" >NUL
if not "%ERRORLEVEL%"=="0" (
    echo [AVISO] Modelo qwen2.5:14b nao encontrado.
    echo Baixando agora... ^(isso pode demorar^)
    ollama pull qwen2.5:14b
)

REM === 3. Ativa o ambiente virtual ===
if exist ".venv\Scripts\activate.bat" (
    echo [OK] Ativando ambiente virtual
    call .venv\Scripts\activate.bat
) else (
    echo [ERRO] Ambiente virtual nao encontrado.
    echo Rode: python -m venv .venv
    pause
    exit /b 1
)

REM === 4. Sobe o Streamlit ===
echo.
echo ========================================
echo   Abrindo interface...
echo ========================================
echo.
echo A interface vai abrir no navegador em alguns segundos.
echo.
echo Para fechar a aplicacao:
echo   1. Feche esta janela
echo   2. Feche o Ollama no outro terminal
echo.

timeout /t 2 /nobreak >NUL
start "" http://localhost:8501

streamlit run app.py

pause