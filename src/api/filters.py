"""검색 필터 모듈"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable
from ..database.models import Video

logger = logging.getLogger(__name__)


class VideoFilter:
    """영상 필터링 클래스"""
    
    @staticmethod
    def filter_by_subscribers(videos: List[Video], max_subscribers: int = 10000) -> List[Video]:
        """구독자 수로 필터링
        
        Args:
            videos: 필터링할 영상 리스트
            max_subscribers: 최대 구독자 수
            
        Returns:
            필터링된 영상 리스트
        """
        filtered = [v for v in videos if v.subscriber_count <= max_subscribers]
        logger.info(f"구독자 수 필터링: {len(videos)} -> {len(filtered)}")
        return filtered
    
    @staticmethod
    def filter_by_duration(videos: List[Video], min_duration_seconds: int = 1200) -> List[Video]:
        """영상 길이로 필터링
        
        Args:
            videos: 필터링할 영상 리스트
            min_duration_seconds: 최소 영상 길이 (초)
            
        Returns:
            필터링된 영상 리스트
        """
        filtered = [v for v in videos if v.duration_seconds >= min_duration_seconds]
        logger.info(f"영상 길이 필터링: {len(videos)} -> {len(filtered)}")
        return filtered
    
    @staticmethod
    def filter_by_upload_date(videos: List[Video], days_back: int = 30) -> List[Video]:
        """업로드 날짜로 필터링
        
        Args:
            videos: 필터링할 영상 리스트
            days_back: 며칠 전까지 허용할지
            
        Returns:
            필터링된 영상 리스트
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered = [
            v for v in videos 
            if v.upload_date and v.upload_date >= cutoff_date
        ]
        logger.info(f"업로드 날짜 필터링: {len(videos)} -> {len(filtered)}")
        return filtered
    
    @staticmethod
    def filter_by_view_count(videos: List[Video], min_views: int = 0) -> List[Video]:
        """조회수로 필터링
        
        Args:
            videos: 필터링할 영상 리스트
            min_views: 최소 조회수
            
        Returns:
            필터링된 영상 리스트
        """
        filtered = [v for v in videos if v.view_count >= min_views]
        logger.info(f"조회수 필터링: {len(videos)} -> {len(filtered)}")
        return filtered
    
    @staticmethod
    def sort_by_view_count(videos: List[Video], descending: bool = True) -> List[Video]:
        """조회수 순으로 정렬
        
        Args:
            videos: 정렬할 영상 리스트
            descending: 내림차순 여부
            
        Returns:
            정렬된 영상 리스트
        """
        sorted_videos = sorted(videos, key=lambda x: x.view_count, reverse=descending)
        logger.info(f"조회수 순 정렬 완료: {len(sorted_videos)}개 영상")
        return sorted_videos
    
    @staticmethod
    def sort_by_upload_date(videos: List[Video], descending: bool = True) -> List[Video]:
        """업로드 날짜 순으로 정렬
        
        Args:
            videos: 정렬할 영상 리스트
            descending: 내림차순 여부 (최신순)
            
        Returns:
            정렬된 영상 리스트
        """
        # upload_date가 None인 영상은 맨 뒤로
        videos_with_date = [v for v in videos if v.upload_date]
        videos_without_date = [v for v in videos if not v.upload_date]
        
        sorted_with_date = sorted(
            videos_with_date, 
            key=lambda x: x.upload_date, 
            reverse=descending
        )
        
        result = sorted_with_date + videos_without_date
        logger.info(f"업로드 날짜 순 정렬 완료: {len(result)}개 영상")
        return result
    
    @staticmethod
    def apply_all_filters(
        videos: List[Video],
        max_subscribers: int = 10000,
        min_duration_seconds: int = 1200,
        days_back: int = 30,
        min_views: int = 0,
        max_results: int = 20
    ) -> List[Video]:
        """모든 필터 적용
        
        Args:
            videos: 필터링할 영상 리스트
            max_subscribers: 최대 구독자 수
            min_duration_seconds: 최소 영상 길이 (초)
            days_back: 며칠 전까지 허용할지
            min_views: 최소 조회수
            max_results: 최대 결과 수
            
        Returns:
            필터링 및 정렬된 영상 리스트
        """
        logger.info(f"필터링 시작: {len(videos)}개 영상")
        
        # 1. 구독자 수 필터링
        filtered = VideoFilter.filter_by_subscribers(videos, max_subscribers)
        
        # 2. 영상 길이 필터링
        filtered = VideoFilter.filter_by_duration(filtered, min_duration_seconds)
        
        # 3. 업로드 날짜 필터링
        filtered = VideoFilter.filter_by_upload_date(filtered, days_back)
        
        # 4. 조회수 필터링
        filtered = VideoFilter.filter_by_view_count(filtered, min_views)
        
        # 5. 조회수 순 정렬
        filtered = VideoFilter.sort_by_view_count(filtered, descending=True)
        
        # 6. 결과 수 제한
        result = filtered[:max_results]
        
        logger.info(f"필터링 완료: {len(videos)} -> {len(result)}개 영상")
        return result


class SearchCriteria:
    """검색 조건 관리 클래스"""
    
    def __init__(
        self,
        keyword: str = "",
        max_subscribers: int = 10000,
        min_duration_seconds: int = 1200,
        days_back: int = 30,
        min_views: int = 0,
        max_results: int = 20,
        sort_by: str = "view_count",
        sort_desc: bool = True
    ):
        """검색 조건 초기화
        
        Args:
            keyword: 검색 키워드
            max_subscribers: 최대 구독자 수
            min_duration_seconds: 최소 영상 길이 (초)
            days_back: 며칠 전까지 허용할지
            min_views: 최소 조회수
            max_results: 최대 결과 수
            sort_by: 정렬 기준 (view_count, upload_date, like_count)
            sort_desc: 내림차순 여부
        """
        self.keyword = keyword
        self.max_subscribers = max_subscribers
        self.min_duration_seconds = min_duration_seconds
        self.days_back = days_back
        self.min_views = min_views
        self.max_results = max_results
        self.sort_by = sort_by
        self.sort_desc = sort_desc
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'keyword': self.keyword,
            'max_subscribers': self.max_subscribers,
            'min_duration_seconds': self.min_duration_seconds,
            'days_back': self.days_back,
            'min_views': self.min_views,
            'max_results': self.max_results,
            'sort_by': self.sort_by,
            'sort_desc': self.sort_desc
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SearchCriteria':
        """딕셔너리에서 생성"""
        return cls(**data)
    
    def get_filter_summary(self) -> str:
        """필터 조건 요약 문자열 반환"""
        duration_min = self.min_duration_seconds // 60
        return (
            f"구독자 ≤{self.max_subscribers:,}명 | "
            f"길이 ≥{duration_min}분 | "
            f"최근 {self.days_back}일 | "
            f"결과 {self.max_results}개"
        )