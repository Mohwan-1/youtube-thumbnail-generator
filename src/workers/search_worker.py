"""검색 워커 모듈"""

import logging
from PySide6.QtCore import QThread, Signal
from typing import List
import time

from ..api.client import YouTubeAPIClient
from ..database.models import Video
from ..utils.validators import DataValidator

logger = logging.getLogger(__name__)


class SearchWorker(QThread):
    """백그라운드 검색 워커"""
    
    # 시그널 정의
    progress_updated = Signal(int)              # 진행률 업데이트
    log_message = Signal(str, str)              # 로그 메시지 (message, level)
    search_completed = Signal(list)             # 검색 완료 (videos)
    search_failed = Signal(str)                 # 검색 실패 (error_message)
    
    def __init__(self, youtube_client: YouTubeAPIClient, keyword: str):
        """검색 워커 초기화
        
        Args:
            youtube_client: YouTube API 클라이언트
            keyword: 검색 키워드
        """
        super().__init__()
        self.youtube_client = youtube_client
        self.keyword = keyword
        self.is_cancelled = False
    
    def run(self):
        """검색 실행"""
        try:
            self.log_message.emit(f"검색 시작: '{self.keyword}'", "INFO")
            self.progress_updated.emit(10)
            
            # 키워드 유효성 검사
            if not DataValidator.validate_keyword(self.keyword):
                self.search_failed.emit("유효하지 않은 키워드입니다.")
                return
            
            self.progress_updated.emit(20)
            
            # YouTube API로 검색
            self.log_message.emit("YouTube API 검색 중...", "INFO")
            videos = self.youtube_client.search_videos(
                keyword=self.keyword,
                max_results=20,
                max_subscribers=10000,
                min_duration_seconds=1200,
                days_back=30
            )
            
            if self.is_cancelled:
                return
            
            self.progress_updated.emit(80)
            
            # 검색 결과 검증
            validated_videos = []
            for video in videos:
                if self.is_cancelled:
                    return
                
                if DataValidator.validate_video_data(video.to_dict()):
                    validated_videos.append(video)
                else:
                    self.log_message.emit(f"유효하지 않은 영상 데이터 제외: {video.video_id}", "WARNING")
            
            self.progress_updated.emit(90)
            
            # 완료 처리
            self.log_message.emit(f"검색 완료: {len(validated_videos)}개 영상 발견", "SUCCESS")
            self.progress_updated.emit(100)
            
            # 잠시 대기 (사용자가 진행률을 볼 수 있도록)
            time.sleep(0.5)
            
            self.search_completed.emit(validated_videos)
            
        except Exception as e:
            logger.error(f"검색 워커 실행 중 오류: {e}")
            self.log_message.emit(f"검색 중 오류 발생: {str(e)}", "ERROR")
            self.search_failed.emit(str(e))
    
    def cancel(self):
        """검색 취소"""
        self.is_cancelled = True
        self.log_message.emit("검색이 취소되었습니다.", "WARNING")