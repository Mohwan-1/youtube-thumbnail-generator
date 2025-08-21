"""설정 관리 모듈"""

import keyring
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


class Config:
    """애플리케이션 설정 관리"""
    
    SERVICE_NAME = "youtube_analytics"
    API_KEY_NAME = "api_key"
    CONFIG_FILE = "config.json"
    
    def __init__(self, config_dir: Optional[str] = None):
        """설정 초기화
        
        Args:
            config_dir: 설정 파일 디렉토리 (기본값: 현재 디렉토리)
        """
        self.config_dir = Path(config_dir) if config_dir else Path.cwd()
        self.config_path = self.config_dir / self.CONFIG_FILE
        self._config_data: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """설정 파일 로드"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
                logger.info("설정 파일 로드 완료")
            else:
                self._config_data = self._get_default_config()
                self._save_config()
                logger.info("기본 설정 파일 생성")
        except Exception as e:
            logger.error(f"설정 파일 로드 실패: {e}")
            self._config_data = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """기본 설정 반환"""
        return {
            "app": {
                "name": "YouTube Keyword Analytics Tool",
                "version": "1.0.0",
                "window_width": 1200,
                "window_height": 800,
                "theme": "dark"
            },
            "search": {
                "max_results": 20,
                "max_subscribers": 10000,
                "min_duration_seconds": 1200,
                "days_back": 30
            },
            "database": {
                "filename": "youtube_analytics.db",
                "backup_enabled": True,
                "backup_interval_days": 7
            },
            "export": {
                "default_format": "csv",
                "include_thumbnails": False,
                "filename_format": "search_{keyword}_{date}.csv"
            }
        }
    
    def _save_config(self) -> None:
        """설정 파일 저장"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=2, ensure_ascii=False)
            logger.info("설정 파일 저장 완료")
        except Exception as e:
            logger.error(f"설정 파일 저장 실패: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """설정 값 가져오기
        
        Args:
            key: 설정 키 (예: "app.name", "search.max_results")
            default: 기본값
            
        Returns:
            설정 값
        """
        keys = key.split('.')
        value = self._config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """설정 값 저장
        
        Args:
            key: 설정 키
            value: 설정 값
        """
        keys = key.split('.')
        config = self._config_data
        
        # 중첩된 딕셔너리 생성
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config()
    
    def save_api_key(self, api_key: str) -> bool:
        """API 키 안전하게 저장
        
        Args:
            api_key: YouTube Data API 키
            
        Returns:
            저장 성공 여부
        """
        try:
            keyring.set_password(self.SERVICE_NAME, self.API_KEY_NAME, api_key)
            logger.info("API 키 저장 완료")
            return True
        except Exception as e:
            logger.error(f"API 키 저장 실패: {e}")
            return False
    
    def get_api_key(self) -> Optional[str]:
        """저장된 API 키 가져오기
        
        Returns:
            API 키 또는 None
        """
        try:
            api_key = keyring.get_password(self.SERVICE_NAME, self.API_KEY_NAME)
            if api_key:
                logger.info("API 키 조회 완료")
            else:
                logger.warning("저장된 API 키가 없습니다")
            return api_key
        except Exception as e:
            logger.error(f"API 키 조회 실패: {e}")
            return None
    
    def delete_api_key(self) -> bool:
        """API 키 삭제
        
        Returns:
            삭제 성공 여부
        """
        try:
            keyring.delete_password(self.SERVICE_NAME, self.API_KEY_NAME)
            logger.info("API 키 삭제 완료")
            return True
        except Exception as e:
            logger.error(f"API 키 삭제 실패: {e}")
            return False