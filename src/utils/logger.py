"""로깅 설정 모듈"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


class LoggerSetup:
    """로깅 설정 클래스"""
    
    @staticmethod
    def setup_logging(
        log_level: str = "INFO",
        log_dir: str = "logs",
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        console_output: bool = True
    ) -> None:
        """로깅 설정 초기화
        
        Args:
            log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir: 로그 파일 디렉토리
            max_file_size: 최대 파일 크기 (바이트)
            backup_count: 백업 파일 개수
            console_output: 콘솔 출력 여부
        """
        # 로그 디렉토리 생성
        Path(log_dir).mkdir(exist_ok=True)
        
        # 로그 포맷
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 루트 로거 설정
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level.upper()))
        
        # 기존 핸들러 제거
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # 파일 핸들러 (일반 로그)
        file_handler = RotatingFileHandler(
            filename=f"{log_dir}/app.log",
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        
        # 에러 로그 별도 파일
        error_handler = RotatingFileHandler(
            filename=f"{log_dir}/error.log",
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_handler)
        
        # 콘솔 핸들러
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(getattr(logging, log_level.upper()))
            root_logger.addHandler(console_handler)
        
        # 외부 라이브러리 로그 레벨 조정
        logging.getLogger('googleapiclient').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('google.auth').setLevel(logging.WARNING)
        
        # 로깅 설정 완료 메시지
        logger = logging.getLogger(__name__)
        logger.info("로깅 설정 완료")
    
    @staticmethod
    def get_logger(name: Optional[str] = None) -> logging.Logger:
        """로거 인스턴스 반환
        
        Args:
            name: 로거 이름 (기본값: 호출하는 모듈명)
            
        Returns:
            로거 인스턴스
        """
        return logging.getLogger(name)