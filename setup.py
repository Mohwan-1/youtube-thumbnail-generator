"""설치 및 배포 설정"""

from setuptools import setup, find_packages
from pathlib import Path
import sys

# 프로젝트 루트 디렉토리
project_root = Path(__file__).parent

# README 파일 읽기
readme_path = project_root / "readme_document.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "YouTube 키워드 기반 영상 분석 도구"

# 버전 정보
VERSION = "1.0.0"

# 필수 패키지
REQUIRED_PACKAGES = [
    "PySide6>=6.6.0",
    "pandas>=2.1.3",
    "requests>=2.31.0",
    "google-api-python-client>=2.108.0",
    "google-auth-oauthlib>=1.1.0",
    "keyring>=24.3.0",
    "isodate>=0.6.1",
    "python-dateutil>=2.8.2",
]

# 개발용 패키지
DEV_PACKAGES = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=22.0.0",
    "flake8>=5.0.0",
    "mypy>=1.0.0",
    "bandit>=1.7.0",
    "safety>=2.0.0",
    "pyinstaller>=5.0.0",
]

setup(
    name="youtube-keyword-analytics",
    version=VERSION,
    author="YouTube Analytics Team",
    author_email="developer@example.com",
    description="YouTube 키워드 기반 영상 분석 도구",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/youtube-keyword-analytics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=REQUIRED_PACKAGES,
    extras_require={
        "dev": DEV_PACKAGES,
    },
    entry_points={
        "console_scripts": [
            "youtube-analytics=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["gui/styles/*.qss", "gui/icons/*.png"],
    },
    zip_safe=False,
)