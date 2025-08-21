"""YouTube API 클라이언트 모듈"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

from ..utils.validators import DataValidator
from ..utils.helpers import FormatHelper
from ..database.models import Video

logger = logging.getLogger(__name__)


class YouTubeAPIClient:
    """YouTube Data API v3 클라이언트"""
    
    def __init__(self, api_key: str):
        """YouTube API 클라이언트 초기화
        
        Args:
            api_key: YouTube Data API 키
        """
        self.api_key = api_key
        self.youtube = None
        self.quota_used = 0
        self.daily_quota_limit = 10000
        self._init_client()
    
    def _init_client(self) -> None:
        """YouTube API 클라이언트 초기화"""
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
            logger.info("YouTube API 클라이언트 초기화 완료")
        except Exception as e:
            logger.error(f"YouTube API 클라이언트 초기화 실패: {e}")
            raise
    
    def validate_api_key(self) -> bool:
        """API 키 유효성 검사
        
        Returns:
            유효성 여부
        """
        try:
            if not self.youtube:
                return False
            
            # 간단한 테스트 요청
            request = self.youtube.search().list(
                part='snippet',
                q='test',
                maxResults=1,
                type='video'
            )
            
            response = request.execute()
            logger.info("API 키 유효성 검사 통과")
            return True
            
        except HttpError as e:
            if e.resp.status == 403:
                logger.error("API 키가 유효하지 않거나 할당량이 초과되었습니다")
            else:
                logger.error(f"API 키 검증 중 HTTP 오류: {e}")
            return False
        except Exception as e:
            logger.error(f"API 키 검증 실패: {e}")
            return False
    
    def search_videos(
        self, 
        keyword: str, 
        max_results: int = 20,
        max_subscribers: int = 10000,
        min_duration_seconds: int = 1200,
        days_back: int = 30
    ) -> List[Video]:
        """키워드로 영상 검색 및 필터링
        
        Args:
            keyword: 검색 키워드
            max_results: 최대 결과 수
            max_subscribers: 최대 구독자 수
            min_duration_seconds: 최소 영상 길이 (초)
            days_back: 며칠 전까지 검색할지
            
        Returns:
            필터링된 영상 리스트
        """
        if not self.youtube:
            logger.error("YouTube API 클라이언트가 초기화되지 않았습니다")
            return []
        
        if not DataValidator.validate_keyword(keyword):
            logger.error(f"유효하지 않은 키워드: {keyword}")
            return []
        
        try:
            # 1단계: 기본 검색
            search_results = self._search_videos_basic(keyword, days_back)
            if not search_results:
                return []
            
            # 2단계: 영상 상세 정보 조회
            video_details = self._get_video_details([item['id']['videoId'] for item in search_results])
            
            # 3단계: 채널 정보 조회 및 필터링
            filtered_videos = []
            for video_data in video_details:
                try:
                    # 채널 정보 조회
                    channel_info = self._get_channel_info(video_data['snippet']['channelId'])
                    if not channel_info:
                        continue
                    
                    # 구독자 수 필터링
                    subscriber_count = channel_info.get('subscriberCount', 0)
                    if not DataValidator.validate_subscriber_count(subscriber_count, max_subscribers):
                        continue
                    
                    # 영상 길이 필터링
                    duration_seconds = self._parse_duration(video_data.get('contentDetails', {}).get('duration', ''))
                    if not DataValidator.validate_video_duration(duration_seconds, min_duration_seconds):
                        continue
                    
                    # Video 객체 생성
                    video = self._create_video_object(video_data, channel_info, keyword)
                    if video:
                        filtered_videos.append(video)
                    
                    # 결과 수 제한
                    if len(filtered_videos) >= max_results:
                        break
                        
                except Exception as e:
                    logger.warning(f"영상 처리 중 오류: {e}")
                    continue
            
            # 조회수 순으로 정렬
            filtered_videos.sort(key=lambda x: x.view_count, reverse=True)
            
            logger.info(f"검색 완료: {keyword} - {len(filtered_videos)}개 영상")
            return filtered_videos[:max_results]
            
        except Exception as e:
            logger.error(f"영상 검색 실패: {e}")
            return []
    
    def _search_videos_basic(self, keyword: str, days_back: int = 30) -> List[Dict[str, Any]]:
        """기본 영상 검색
        
        Args:
            keyword: 검색 키워드
            days_back: 며칠 전까지 검색할지
            
        Returns:
            검색 결과 리스트
        """
        try:
            # 날짜 계산
            published_after = (datetime.now() - timedelta(days=days_back)).isoformat() + 'Z'
            
            request = self.youtube.search().list(
                part='snippet',
                q=keyword,
                type='video',
                order='viewCount',
                publishedAfter=published_after,
                videoDuration='long',  # 20분 이상
                maxResults=50,
                regionCode='KR'
            )
            
            response = request.execute()
            self.quota_used += 100  # Search API 비용
            
            return response.get('items', [])
            
        except HttpError as e:
            logger.error(f"YouTube 검색 API 오류: {e}")
            return []
        except Exception as e:
            logger.error(f"기본 검색 실패: {e}")
            return []
    
    def _get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """영상 상세 정보 조회
        
        Args:
            video_ids: 영상 ID 리스트
            
        Returns:
            영상 상세 정보 리스트
        """
        if not video_ids:
            return []
        
        try:
            # 50개씩 배치 처리 (API 제한)
            all_videos = []
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                
                request = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(batch_ids)
                )
                
                response = request.execute()
                self.quota_used += 1  # Videos API 비용
                
                all_videos.extend(response.get('items', []))
                
                # API 제한 방지를 위한 지연
                time.sleep(0.1)
            
            return all_videos
            
        except Exception as e:
            logger.error(f"영상 상세 정보 조회 실패: {e}")
            return []
    
    def _get_channel_info(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """채널 정보 조회
        
        Args:
            channel_id: 채널 ID
            
        Returns:
            채널 정보 또는 None
        """
        try:
            request = self.youtube.channels().list(
                part='statistics',
                id=channel_id
            )
            
            response = request.execute()
            self.quota_used += 1  # Channels API 비용
            
            items = response.get('items', [])
            if items:
                stats = items[0].get('statistics', {})
                return {
                    'subscriberCount': int(stats.get('subscriberCount', 0))
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"채널 정보 조회 실패 (channel_id: {channel_id}): {e}")
            return None
    
    def _parse_duration(self, duration_str: str) -> int:
        """YouTube duration 형식을 초로 변환
        
        Args:
            duration_str: ISO 8601 duration 형식 (예: PT20M15S)
            
        Returns:
            총 초 수
        """
        try:
            total_seconds, _ = FormatHelper.parse_iso_duration(duration_str)
            return total_seconds
        except Exception as e:
            logger.warning(f"Duration 파싱 실패: {duration_str} - {e}")
            return 0
    
    def _create_video_object(
        self, 
        video_data: Dict[str, Any], 
        channel_info: Dict[str, Any], 
        keyword: str
    ) -> Optional[Video]:
        """Video 객체 생성
        
        Args:
            video_data: YouTube API 영상 데이터
            channel_info: 채널 정보
            keyword: 검색 키워드
            
        Returns:
            Video 객체 또는 None
        """
        try:
            snippet = video_data.get('snippet', {})
            statistics = video_data.get('statistics', {})
            content_details = video_data.get('contentDetails', {})
            
            # 기본 정보
            video_id = video_data.get('id', '')
            title = snippet.get('title', '')
            channel_name = snippet.get('channelTitle', '')
            channel_id = snippet.get('channelId', '')
            
            # 통계 정보
            view_count = int(statistics.get('viewCount', 0))
            like_count = int(statistics.get('likeCount', 0))
            comment_count = int(statistics.get('commentCount', 0))
            subscriber_count = channel_info.get('subscriberCount', 0)
            
            # 영상 길이
            duration_str = content_details.get('duration', '')
            duration_seconds, duration_formatted = FormatHelper.parse_iso_duration(duration_str)
            
            # 업로드 날짜
            published_at = snippet.get('publishedAt', '')
            upload_date = None
            if published_at:
                upload_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            
            # URL 생성
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            thumbnail_url = snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
            
            # Video 객체 생성
            video = Video(
                video_id=video_id,
                title=title,
                channel_name=channel_name,
                channel_id=channel_id,
                subscriber_count=subscriber_count,
                view_count=view_count,
                like_count=like_count,
                comment_count=comment_count,
                duration_seconds=duration_seconds,
                duration_formatted=duration_formatted,
                upload_date=upload_date,
                thumbnail_url=thumbnail_url,
                video_url=video_url,
                search_keyword=keyword
            )
            
            # 데이터 유효성 검사
            if DataValidator.validate_video_data(video.to_dict()):
                return video
            else:
                logger.warning(f"유효하지 않은 영상 데이터: {video_id}")
                return None
                
        except Exception as e:
            logger.error(f"Video 객체 생성 실패: {e}")
            return None
    
    def get_quota_usage(self) -> Dict[str, int]:
        """API 할당량 사용량 조회
        
        Returns:
            할당량 정보
        """
        return {
            'used': self.quota_used,
            'limit': self.daily_quota_limit,
            'remaining': max(0, self.daily_quota_limit - self.quota_used),
            'percentage': min(100, (self.quota_used / self.daily_quota_limit) * 100)
        }
    
    def reset_quota_usage(self) -> None:
        """할당량 사용량 초기화 (일일 리셋용)"""
        self.quota_used = 0
        logger.info("API 할당량 사용량 초기화")