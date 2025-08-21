@echo off
title YouTube Analytics - 실행 파일 빌드
color 0E

echo ===============================================
echo  YouTube Keyword Analytics Tool
echo  실행 파일 빌드 스크립트
echo ===============================================
echo.

echo [1단계] 환경 확인 중...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    pause
    exit /b 1
)

echo ✅ Python 확인됨

echo.
echo [2단계] PyInstaller 설치 중...
pip install pyinstaller
if errorlevel 1 (
    echo ❌ PyInstaller 설치 실패
    pause
    exit /b 1
)

echo ✅ PyInstaller 설치 완료

echo.
echo [3단계] 빌드 디렉토리 정리 중...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

mkdir build 2>nul
mkdir dist 2>nul

echo ✅ 빌드 디렉토리 정리 완료

echo.
echo [4단계] 의존성 패키지 설치 중...
pip install PySide6>=6.6.0 pandas>=2.1.3 requests>=2.31.0 google-api-python-client>=2.108.0 google-auth-oauthlib>=1.1.0 keyring>=24.3.0 isodate>=0.6.1 python-dateutil>=2.8.2
if errorlevel 1 (
    echo ❌ 의존성 설치 실패
    pause
    exit /b 1
)

echo ✅ 의존성 설치 완료

echo.
echo [5단계] 실행 파일 빌드 중...
echo    이 과정은 몇 분 소요될 수 있습니다...

pyinstaller --onefile ^
    --windowed ^
    --name="YouTubeAnalytics" ^
    --add-data="src;src" ^
    --hidden-import="PySide6.QtCore" ^
    --hidden-import="PySide6.QtWidgets" ^
    --hidden-import="PySide6.QtGui" ^
    --hidden-import="google.auth" ^
    --hidden-import="google.auth.transport" ^
    --hidden-import="googleapiclient" ^
    --hidden-import="pandas" ^
    --hidden-import="keyring" ^
    --hidden-import="isodate" ^
    --exclude-module="tkinter" ^
    --exclude-module="matplotlib" ^
    --exclude-module="numpy" ^
    --exclude-module="scipy" ^
    --clean ^
    main.py

if errorlevel 1 (
    echo ❌ 빌드 실패
    echo    오류 로그를 확인하세요.
    pause
    exit /b 1
)

echo ✅ 빌드 완료

echo.
echo [6단계] 배포 패키지 구성 중...

REM 실행 파일 확인
if not exist "dist\YouTubeAnalytics.exe" (
    echo ❌ 실행 파일을 찾을 수 없습니다.
    pause
    exit /b 1
)

REM 파일 크기 확인
for %%A in ("dist\YouTubeAnalytics.exe") do set "filesize=%%~zA"
set /a filesize_mb=%filesize% / 1048576

echo ✅ 실행 파일 생성됨: dist\YouTubeAnalytics.exe (%filesize_mb% MB)

REM README 복사
if exist "readme_document.md" copy "readme_document.md" "dist\README.md"

REM 배치 파일 생성
echo @echo off > "dist\run.bat"
echo title YouTube Keyword Analytics Tool >> "dist\run.bat"
echo echo YouTube Keyword Analytics Tool을 시작합니다... >> "dist\run.bat"
echo echo. >> "dist\run.bat"
echo echo 첫 실행시 YouTube Data API 키가 필요합니다. >> "dist\run.bat"
echo echo API 키 발급: https://console.cloud.google.com/ >> "dist\run.bat"
echo echo. >> "dist\run.bat"
echo YouTubeAnalytics.exe >> "dist\run.bat"
echo pause >> "dist\run.bat"

echo ✅ 배포 패키지 구성 완료

echo.
echo ===============================================
echo  빌드 완료!
echo ===============================================
echo.
echo 📁 배포 디렉토리: dist\
echo 🚀 실행 파일: dist\YouTubeAnalytics.exe
echo 📄 실행 배치: dist\run.bat
echo.
echo 사용법:
echo 1. dist 폴더를 원하는 위치에 복사
echo 2. run.bat을 실행하거나 YouTubeAnalytics.exe를 직접 실행
echo 3. YouTube Data API 키 입력
echo 4. 키워드 검색 시작
echo.
echo ⚠️  주의사항:
echo - 첫 실행 시 보안 경고가 나타날 수 있습니다
echo - Windows Defender에서 차단될 수 있으니 예외 처리하세요
echo - API 키는 안전하게 보관하세요
echo.

pause