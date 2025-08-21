"""빌드 설정 및 실행 파일 생성 스크립트"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BuildConfig:
    """빌드 설정 클래스"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.src_dir = self.project_root / "src"
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.main_script = self.project_root / "main.py"
        
        # 애플리케이션 정보
        self.app_name = "YouTubeAnalytics"
        self.app_version = "1.0.0"
        self.app_description = "YouTube Keyword Analytics Tool"
        
    def clean_build_dirs(self):
        """빌드 디렉토리 정리"""
        logger.info("빌드 디렉토리 정리 중...")
        
        dirs_to_clean = [self.build_dir, self.dist_dir]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                logger.info(f"삭제됨: {dir_path}")
        
        # 디렉토리 다시 생성
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
        logger.info("빌드 디렉토리 정리 완료")
    
    def create_spec_file(self):
        """PyInstaller spec 파일 생성"""
        logger.info("PyInstaller spec 파일 생성 중...")
        
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# 프로젝트 루트 경로
project_root = Path("{self.project_root.as_posix()}")

block_cipher = None

a = Analysis(
    ['{self.main_script.as_posix()}'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # 설정 파일 및 리소스
        (str(project_root / "src"), "src"),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets', 
        'PySide6.QtGui',
        'google.auth',
        'google.auth.transport',
        'google.auth.transport.requests',
        'googleapiclient',
        'googleapiclient.discovery',
        'googleapiclient.errors',
        'pandas',
        'keyring',
        'keyring.backends',
        'isodate',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'PIL',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 애플리케이션이므로 콘솔 창 숨김
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon=None,  # 아이콘 파일이 있다면 경로 추가
)
'''
        
        spec_file_path = self.project_root / f"{self.app_name}.spec"
        with open(spec_file_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        logger.info(f"Spec 파일 생성 완료: {spec_file_path}")
        return spec_file_path
    
    def create_version_info(self):
        """버전 정보 파일 생성 (Windows용)"""
        logger.info("버전 정보 파일 생성 중...")
        
        version_info_content = f'''
# UTF-8
#
# 버전 정보 리소스
#

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'YouTube Analytics Team'),
            StringStruct(u'FileDescription', u'{self.app_description}'),
            StringStruct(u'FileVersion', u'{self.app_version}'),
            StringStruct(u'InternalName', u'{self.app_name}'),
            StringStruct(u'LegalCopyright', u'Copyright (C) 2024'),
            StringStruct(u'OriginalFilename', u'{self.app_name}.exe'),
            StringStruct(u'ProductName', u'{self.app_description}'),
            StringStruct(u'ProductVersion', u'{self.app_version}')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        version_file_path = self.project_root / "version_info.txt"
        with open(version_file_path, 'w', encoding='utf-8') as f:
            f.write(version_info_content)
        
        logger.info(f"버전 정보 파일 생성 완료: {version_file_path}")
        return version_file_path
    
    def install_dependencies(self):
        """의존성 패키지 설치"""
        logger.info("의존성 패키지 설치 중...")
        
        try:
            # UV를 사용하여 패키지 설치
            subprocess.run([
                "uv", "pip", "install", 
                "PySide6>=6.6.0",
                "pandas>=2.1.3", 
                "requests>=2.31.0",
                "google-api-python-client>=2.108.0",
                "google-auth-oauthlib>=1.1.0",
                "keyring>=24.3.0",
                "isodate>=0.6.1",
                "python-dateutil>=2.8.2",
                "pyinstaller>=5.0.0"
            ], check=True)
            
            logger.info("의존성 패키지 설치 완료")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"의존성 설치 실패: {e}")
            raise
        except FileNotFoundError:
            logger.warning("UV가 설치되지 않음. pip 사용...")
            
            # UV가 없으면 pip 사용
            subprocess.run([
                sys.executable, "-m", "pip", "install",
                "PySide6>=6.6.0",
                "pandas>=2.1.3", 
                "requests>=2.31.0",
                "google-api-python-client>=2.108.0",
                "google-auth-oauthlib>=1.1.0",
                "keyring>=24.3.0",
                "isodate>=0.6.1",
                "python-dateutil>=2.8.2",
                "pyinstaller>=5.0.0"
            ], check=True)
            
            logger.info("의존성 패키지 설치 완료 (pip 사용)")
    
    def build_executable(self):
        """실행 파일 빌드"""
        logger.info("실행 파일 빌드 시작...")
        
        try:
            # spec 파일 생성
            spec_file = self.create_spec_file()
            
            # 버전 정보 파일 생성 (Windows)
            if sys.platform == "win32":
                self.create_version_info()
            
            # PyInstaller 실행
            cmd = [
                "pyinstaller",
                "--clean",
                "--noconfirm",
                str(spec_file)
            ]
            
            logger.info(f"PyInstaller 명령 실행: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            logger.info("PyInstaller 실행 완료")
            if result.stdout:
                logger.info(f"PyInstaller 출력: {result.stdout}")
            
            # 빌드된 파일 확인
            if sys.platform == "win32":
                exe_path = self.dist_dir / f"{self.app_name}.exe"
            else:
                exe_path = self.dist_dir / self.app_name
            
            if exe_path.exists():
                file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
                logger.info(f"실행 파일 생성 완료: {exe_path} ({file_size:.1f} MB)")
                return exe_path
            else:
                raise FileNotFoundError(f"실행 파일을 찾을 수 없습니다: {exe_path}")
                
        except subprocess.CalledProcessError as e:
            logger.error(f"PyInstaller 실행 실패: {e}")
            if e.stderr:
                logger.error(f"오류 출력: {e.stderr}")
            raise
    
    def create_installer_script(self):
        """설치 스크립트 생성"""
        logger.info("설치 스크립트 생성 중...")
        
        if sys.platform == "win32":
            # Windows 배치 파일
            installer_content = f'''@echo off
echo YouTube Keyword Analytics Tool 설치
echo.

set INSTALL_DIR=%USERPROFILE%\\YouTubeAnalytics
echo 설치 디렉토리: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo 파일 복사 중...
copy "{self.app_name}.exe" "%INSTALL_DIR%\\"
copy "README.md" "%INSTALL_DIR%\\" 2>nul

echo 바탕화면 바로가기 생성...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\YouTube Analytics.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{self.app_name}.exe'; $Shortcut.Save()"

echo.
echo 설치 완료!
echo 바탕화면의 'YouTube Analytics' 바로가기를 사용하여 프로그램을 실행하세요.
echo.
pause
'''
            installer_path = self.dist_dir / "install.bat"
        else:
            # Unix/Linux 셸 스크립트
            installer_content = f'''#!/bin/bash
echo "YouTube Keyword Analytics Tool 설치"
echo

INSTALL_DIR="$HOME/YouTubeAnalytics"
echo "설치 디렉토리: $INSTALL_DIR"

mkdir -p "$INSTALL_DIR"

echo "파일 복사 중..."
cp "{self.app_name}" "$INSTALL_DIR/"
cp "README.md" "$INSTALL_DIR/" 2>/dev/null || true

chmod +x "$INSTALL_DIR/{self.app_name}"

echo "데스크톱 항목 생성..."
DESKTOP_FILE="$HOME/.local/share/applications/youtube-analytics.desktop"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=YouTube Analytics
Comment={self.app_description}
Exec=$INSTALL_DIR/{self.app_name}
Icon=application-x-executable
Terminal=false
Categories=Office;
EOF

echo
echo "설치 완료!"
echo "애플리케이션 메뉴에서 'YouTube Analytics'를 찾아 실행하세요."
echo
'''
            installer_path = self.dist_dir / "install.sh"
        
        with open(installer_path, 'w', encoding='utf-8') as f:
            f.write(installer_content)
        
        # 실행 권한 부여 (Unix/Linux)
        if sys.platform != "win32":
            os.chmod(installer_path, 0o755)
        
        logger.info(f"설치 스크립트 생성 완료: {installer_path}")
        return installer_path
    
    def create_readme(self):
        """README 파일 생성"""
        logger.info("README 파일 생성 중...")
        
        readme_content = f'''# YouTube Keyword Analytics Tool v{self.app_version}

YouTube 키워드 기반 영상 분석 도구

## 주요 기능
- 키워드 기반 YouTube 영상 검색
- 구독자 10,000명 이하 채널 필터링
- 20분 이상 영상 길이 필터링
- 최근 1개월 업로드 영상 필터링
- 조회수 순 정렬 및 표시
- CSV 파일 내보내기
- 로컬 데이터베이스 자동 저장

## 시스템 요구사항
- Windows 10/11 또는 macOS 10.14+ 또는 Ubuntu 18.04+
- 최소 4GB RAM
- 인터넷 연결
- YouTube Data API v3 키

## 설치 방법
1. YouTube Data API 키 발급 (Google Cloud Console)
2. 프로그램 실행
3. API 키 입력 및 저장
4. 키워드 검색 시작

## 사용법
1. 상단에 YouTube API 키 입력
2. 검색할 키워드 입력
3. '검색 시작' 버튼 클릭
4. 결과 확인 및 CSV 내보내기

## 라이선스
MIT License

## 지원
버그 리포트 및 기능 요청: GitHub Issues
'''
        
        readme_path = self.dist_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        logger.info(f"README 파일 생성 완료: {readme_path}")
        return readme_path
    
    def build_all(self):
        """전체 빌드 프로세스 실행"""
        logger.info("=== YouTube Keyword Analytics Tool 빌드 시작 ===")
        
        try:
            # 1. 빌드 디렉토리 정리
            self.clean_build_dirs()
            
            # 2. 의존성 설치
            self.install_dependencies()
            
            # 3. 실행 파일 빌드
            exe_path = self.build_executable()
            
            # 4. 설치 스크립트 생성
            installer_path = self.create_installer_script()
            
            # 5. README 생성
            readme_path = self.create_readme()
            
            logger.info("=== 빌드 완료 ===")
            logger.info(f"실행 파일: {exe_path}")
            logger.info(f"설치 스크립트: {installer_path}")
            logger.info(f"README: {readme_path}")
            logger.info(f"배포 디렉토리: {self.dist_dir}")
            
            return True
            
        except Exception as e:
            logger.error(f"빌드 실패: {e}")
            return False


def main():
    """메인 함수"""
    builder = BuildConfig()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "clean":
            builder.clean_build_dirs()
        elif command == "install":
            builder.install_dependencies()
        elif command == "build":
            builder.build_executable()
        elif command == "all":
            builder.build_all()
        else:
            print(f"알 수 없는 명령: {command}")
            print("사용법: python build_config.py [clean|install|build|all]")
    else:
        # 기본적으로 전체 빌드 실행
        builder.build_all()


if __name__ == "__main__":
    main()