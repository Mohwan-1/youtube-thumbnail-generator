"""YouTube Keyword Analytics Tool - 메인 애플리케이션"""

import sys
import os
import logging
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from src.utils.logger import LoggerSetup
from src.gui.main_window import MainWindow


def setup_application():
    """애플리케이션 설정"""
    # 로깅 설정
    LoggerSetup.setup_logging(
        log_level="INFO",
        log_dir="logs",
        console_output=True
    )
    
    logger = logging.getLogger(__name__)
    logger.info("YouTube Keyword Analytics Tool 시작")
    
    # QApplication 생성
    app = QApplication(sys.argv)
    
    # 애플리케이션 정보 설정
    app.setApplicationName("YouTube Keyword Analytics Tool")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("YouTube Analytics Team")
    
    # High DPI 지원
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    return app, logger


def main():
    """메인 함수"""
    try:
        # 애플리케이션 설정
        app, logger = setup_application()
        
        # 메인 윈도우 생성 및 표시
        main_window = MainWindow()
        main_window.show()
        
        logger.info("메인 윈도우 표시 완료")
        
        # 애플리케이션 실행
        exit_code = app.exec()
        
        logger.info(f"애플리케이션 종료 (코드: {exit_code})")
        return exit_code
        
    except Exception as e:
        print(f"애플리케이션 실행 중 치명적 오류: {e}")
        logging.error(f"애플리케이션 실행 중 치명적 오류: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())