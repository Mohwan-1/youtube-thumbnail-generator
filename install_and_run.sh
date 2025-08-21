#!/bin/bash

# YouTube Keyword Analytics Tool - 설치 및 실행 스크립트 (Linux/macOS)

set -e  # 오류 발생시 중단

echo "==============================================="
echo " YouTube Keyword Analytics Tool v1.0"
echo " 키워드 기반 YouTube 영상 분석 도구"
echo "==============================================="
echo

echo "[1단계] Python 설치 확인 중..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python이 설치되지 않았습니다."
        echo "   패키지 매니저를 통해 Python 3.8+ 설치 후 다시 실행하세요."
        echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "   macOS: brew install python3"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python 설치 확인됨"

# Python 버전 확인
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(sys.version_info[:2])")
echo "   버전: $($PYTHON_CMD --version)"

echo
echo "[2단계] pip 업그레이드 및 UV 설치 중..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install uv

echo "✅ UV 설치 완료"

echo
echo "[3단계] 프로젝트 의존성 설치 중..."
if ! uv pip install \
    "PySide6>=6.6.0" \
    "pandas>=2.1.3" \
    "requests>=2.31.0" \
    "google-api-python-client>=2.108.0" \
    "google-auth-oauthlib>=1.1.0" \
    "keyring>=24.3.0" \
    "isodate>=0.6.1" \
    "python-dateutil>=2.8.2"; then
    
    echo "❌ UV로 설치 실패, pip로 재시도..."
    $PYTHON_CMD -m pip install \
        "PySide6>=6.6.0" \
        "pandas>=2.1.3" \
        "requests>=2.31.0" \
        "google-api-python-client>=2.108.0" \
        "google-auth-oauthlib>=1.1.0" \
        "keyring>=24.3.0" \
        "isodate>=0.6.1" \
        "python-dateutil>=2.8.2"
fi

echo "✅ 의존성 설치 완료"

echo
echo "[4단계] 필요한 디렉토리 생성 중..."
mkdir -p data logs exports

echo "✅ 디렉토리 생성 완료"

echo
echo "[5단계] 애플리케이션 실행 중..."
echo
echo "🚀 YouTube Keyword Analytics Tool을 시작합니다..."
echo "   첫 실행 시 YouTube Data API 키가 필요합니다."
echo "   API 키 발급: https://console.cloud.google.com/"
echo

# GUI 환경 확인
if [[ -z "$DISPLAY" ]] && [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "⚠️  경고: GUI 디스플레이가 감지되지 않았습니다."
    echo "   X11 전달 또는 데스크톱 환경에서 실행하세요."
fi

$PYTHON_CMD main.py

echo
echo "애플리케이션이 종료되었습니다."