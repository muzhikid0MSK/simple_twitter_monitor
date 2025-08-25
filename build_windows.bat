@echo off
echo ====================================
echo    Twitter����� �����ű�
echo ====================================
echo.

REM ���Python����
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [����] δ��⵽Python����
    pause
    exit /b 1
)

echo [��Ϣ] ��⵽Python����
echo.

REM ��װ����
echo [��Ϣ] ���ڰ�װ������...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [����] ��������װʧ��
    pause
    exit /b 1
)

echo [��Ϣ] ��������װ���
echo.

REM ��������Ŀ¼
if not exist "build" mkdir build
if not exist "dist" mkdir dist

REM ������ִ���ļ�
echo [��Ϣ] ���ڹ�����ִ���ļ�...
pyinstaller --clean --onefile --windowed --icon=assets/icon.ico --name=TwitterMonitor main.py

if %errorlevel% neq 0 (
    echo [����] ����ʧ��
    pause
    exit /b 1
)

echo.
echo [�ɹ�] ������ɣ�
echo ��ִ���ļ�λ��: dist\TwitterMonitor.exe
echo.

REM ���Ʊ�Ҫ�ļ�
echo [��Ϣ] ���ڸ��Ʊ�Ҫ�ļ�...
if exist "drivers" xcopy /E /I drivers dist\drivers
if exist "assets" xcopy /E /I assets dist\assets
if exist "config.json" copy config.json dist\

echo.
echo [���] �����ļ���׼��������
echo ��ִ���ļ�: dist\TwitterMonitor.exe
echo �����ļ�: dist\config.json
echo �����ļ�: dist\drivers\
echo.

pause
