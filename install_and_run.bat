@echo off
title YouTube Keyword Analytics Tool - 설치 및 실행
color 0A

echo ===============================================
echo  YouTube Keyword Analytics Tool v1.0
echo  키워드 기반 YouTube 영상 분석 도구
echo ===============================================
echo.

echo [1단계] Python 및 UV 설치 확인 중...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo    https://python.org 에서 Python 3.8+ 설치 후 다시 실행하세요.
    pause
    exit /b 1
)

echo ✅ Python 설치 확인됨

echo.
echo [2단계] UV 패키지 매니저 설치 중...
pip install uv
if errorlevel 1 (
    echo ❌ UV 설치 실패
    echo    인터넷 연결을 확인하고 다시 시도하세요.
    pause
    exit /b 1
)

echo ✅ UV 설치 완료

echo.
echo [3단계] 프로젝트 의존성 설치 중...
uv pip install PySide6>=6.6.0 pandas>=2.1.3 requests>=2.31.0 google-api-python-client>=2.108.0 google-auth-oauthlib>=1.1.0 keyring>=24.3.0 isodate>=0.6.1 python-dateutil>=2.8.2
if errorlevel 1 (
    echo ❌ 의존성 설치 실패
    echo    pip로 다시 시도합니다...
    pip install PySide6>=6.6.0 pandas>=2.1.3 requests>=2.31.0 google-api-python-client>=2.108.0 google-auth-oauthlib>=1.1.0 keyring>=24.3.0 isodate>=0.6.1 python-dateutil>=2.8.2
    if errorlevel 1 (
        echo ❌ 의존성 설치 최종 실패
        pause
        exit /b 1
    )
)

echo ✅ 의존성 설치 완료

echo.
echo [4단계] 필요한 디렉토리 생성 중...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports

echo ✅ 디렉토리 생성 완료

echo.
echo [5단계] 애플리케이션 실행 중...
echo.
echo 🚀 YouTube Keyword Analytics Tool을 시작합니다...
echo    첫 실행 시 YouTube Data API 키가 필요합니다.
echo    API 키 발급: https://console.cloud.google.com/
echo.

python main.py
if errorlevel 1 (
    echo.
    echo ❌ 애플리케이션 실행 중 오류가 발생했습니다.
    echo    로그를 확인하거나 다시 시도하세요.
    pause
)

echo.
echo 애플리케이션이 종료되었습니다.
pause