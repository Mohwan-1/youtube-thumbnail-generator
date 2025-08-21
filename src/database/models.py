"""데이터베이스 모델 정의"""

from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Video:
    """영상 데이터 모델"""
    video_id: str
    title: str
    channel_name: str
    channel_id: str
    subscriber_count: int = 0
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    duration_seconds: int = 0
    duration_formatted: str = "0:00"
    upload_date: Optional[datetime] = None
    thumbnail_url: str = ""
    video_url: str = ""
    search_keyword: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'video_id': self.video_id,
            'title': self.title,
            'channel_name': self.channel_name,
            'channel_id': self.channel_id,
            'subscriber_count': self.subscriber_count,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'duration_seconds': self.duration_seconds,
            'duration_formatted': self.duration_formatted,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'thumbnail_url': self.thumbnail_url,
            'video_url': self.video_url,
            'search_keyword': self.search_keyword,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Video':
        """딕셔너리에서 생성"""
        # datetime 필드 변환
        for date_field in ['upload_date', 'created_at', 'updated_at']:
            if data.get(date_field) and isinstance(data[date_field], str):
                try:
                    data[date_field] = datetime.fromisoformat(data[date_field])
                except ValueError:
                    data[date_field] = None
        
        return cls(**data)


@dataclass
class SearchHistory:
    """검색 히스토리 모델"""
    keyword: str
    results_count: int = 0
    search_date: Optional[datetime] = None
    id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'keyword': self.keyword,
            'results_count': self.results_count,
            'search_date': self.search_date.isoformat() if self.search_date else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SearchHistory':
        """딕셔너리에서 생성"""
        if data.get('search_date') and isinstance(data['search_date'], str):
            try:
                data['search_date'] = datetime.fromisoformat(data['search_date'])
            except ValueError:
                data['search_date'] = None
        
        return cls(**data)