"""데이터 검증 모듈"""

import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DataValidator:
    """데이터 검증 클래스"""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """YouTube API 키 형식 검증
        
        Args:
            api_key: 검증할 API 키
            
        Returns:
            유효성 여부
        """
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Google API 키 형식: 39자 알파벳 숫자 조합
        pattern = r'^[A-Za-z0-9_-]{35,45}$'
        return bool(re.match(pattern, api_key.strip()))
    
    @staticmethod
    def validate_keyword(keyword: str) -> bool:
        """검색 키워드 유효성 검사
        
        Args:
            keyword: 검증할 키워드
            
        Returns:
            유효성 여부
        """
        if not keyword or not isinstance(keyword, str):
            return False
        
        keyword = keyword.strip()
        
        # 길이 검사 (1-100자)
        if len(keyword) < 1 or len(keyword) > 100:
            return False
        
        # 특수문자 검사 (일부 허용)
        allowed_pattern = r'^[a-zA-Z0-9가-힣\s\-_\+\&\(\)]*$'
        return bool(re.match(allowed_pattern, keyword))
    
    @staticmethod
    def sanitize_keyword(keyword: str) -> str:
        """키워드 정제
        
        Args:
            keyword: 정제할 키워드
            
        Returns:
            정제된 키워드
        """
        if not keyword:
            return ""
        
        # 특수문자 제거 (일부 허용)
        keyword = re.sub(r'[^\w\s가-힣\-_\+\&\(\)]', ' ', keyword)
        
        # 여러 공백을 하나로
        keyword = re.sub(r'\s+', ' ', keyword)
        
        # 앞뒤 공백 제거
        return keyword.strip()
    
    @staticmethod
    def validate_video_data(video: Dict[str, Any]) -> bool:
        """영상 데이터 유효성 검사
        
        Args:
            video: 검증할 영상 데이터
            
        Returns:
            유효성 여부
        """
        if not isinstance(video, dict):
            return False
        
        # 필수 필드 확인
        required_fields = ['video_id', 'title', 'channel_name', 'channel_id']
        for field in required_fields:
            if field not in video or not video[field]:
                logger.warning(f"필수 필드 누락: {field}")
                return False
        
        # 영상 ID 형식 검사 (YouTube 영상 ID는 11자)
        video_id = video.get('video_id', '')
        if not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
            logger.warning(f"잘못된 영상 ID 형식: {video_id}")
            return False
        
        # 채널 ID 형식 검사
        channel_id = video.get('channel_id', '')
        if not re.match(r'^UC[a-zA-Z0-9_-]{22}$', channel_id):
            logger.warning(f"잘못된 채널 ID 형식: {channel_id}")
            return False
        
        return True
    
    @staticmethod
    def normalize_video_data(video: Dict[str, Any]) -> Dict[str, Any]:
        """영상 데이터 정규화
        
        Args:
            video: 정규화할 영상 데이터
            
        Returns:
            정규화된 영상 데이터
        """
        normalized = video.copy()
        
        # 숫자 필드 정규화
        numeric_fields = {
            'view_count': 0,
            'subscriber_count': 0,
            'like_count': 0,
            'comment_count': 0,
            'duration_seconds': 0
        }
        
        for field, default_value in numeric_fields.items():
            if field in normalized:
                try:
                    normalized[field] = int(normalized[field]) if normalized[field] else default_value
                except (ValueError, TypeError):
                    normalized[field] = default_value
            else:
                normalized[field] = default_value
        
        # 문자열 필드 정리
        string_fields = ['title', 'channel_name', 'description']
        for field in string_fields:
            if field in normalized and normalized[field]:
                # HTML 태그 제거
                normalized[field] = re.sub(r'<[^>]+>', '', str(normalized[field]))
                # 여러 공백 정리
                normalized[field] = re.sub(r'\s+', ' ', normalized[field]).strip()
        
        # URL 필드 검증
        url_fields = ['video_url', 'thumbnail_url']
        for field in url_fields:
            if field in normalized and normalized[field]:
                url = str(normalized[field])
                if not url.startswith(('http://', 'https://')):
                    normalized[field] = f"https://{url}" if url else ""
        
        return normalized
    
    @staticmethod
    def validate_duration_string(duration_str: str) -> bool:
        """YouTube 영상 길이 형식 검증
        
        Args:
            duration_str: ISO 8601 duration 형식 (PT20M15S)
            
        Returns:
            유효성 여부
        """
        if not duration_str:
            return False
        
        pattern = r'^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$'
        return bool(re.match(pattern, duration_str))
    
    @staticmethod
    def validate_subscriber_count(count: int, max_subscribers: int = 10000) -> bool:
        """구독자 수 필터링 조건 검증
        
        Args:
            count: 구독자 수
            max_subscribers: 최대 구독자 수
            
        Returns:
            조건 만족 여부
        """
        return isinstance(count, int) and 0 <= count <= max_subscribers
    
    @staticmethod
    def validate_upload_date(upload_date: datetime, days_back: int = 30) -> bool:
        """업로드 날짜 필터링 조건 검증
        
        Args:
            upload_date: 업로드 날짜
            days_back: 며칠 전까지 허용할지
            
        Returns:
            조건 만족 여부
        """
        if not isinstance(upload_date, datetime):
            return False
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        return upload_date >= cutoff_date
    
    @staticmethod
    def validate_video_duration(duration_seconds: int, min_duration: int = 1200) -> bool:
        """영상 길이 필터링 조건 검증
        
        Args:
            duration_seconds: 영상 길이 (초)
            min_duration: 최소 길이 (초, 기본값: 20분)
            
        Returns:
            조건 만족 여부
        """
        return isinstance(duration_seconds, int) and duration_seconds >= min_duration