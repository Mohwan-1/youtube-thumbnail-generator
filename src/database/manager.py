"""데이터베이스 관리 모듈"""

import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from .models import Video, SearchHistory

logger = logging.getLogger(__name__)


class DatabaseManager:
    """SQLite 데이터베이스 관리 클래스"""
    
    def __init__(self, db_path: str = "data/youtube_analytics.db"):
        """데이터베이스 매니저 초기화
        
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
    
    @contextmanager
    def get_connection(self):
        """데이터베이스 연결 컨텍스트 매니저"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
        
        try:
            # 성능 최적화 설정
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=10000")
            conn.execute("PRAGMA temp_store=MEMORY")
            
            yield conn
        finally:
            conn.close()
    
    def _init_database(self) -> None:
        """데이터베이스 및 테이블 초기화"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # videos 테이블 생성
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS videos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        video_id TEXT UNIQUE NOT NULL,
                        title TEXT NOT NULL,
                        channel_name TEXT NOT NULL,
                        channel_id TEXT NOT NULL,
                        subscriber_count INTEGER DEFAULT 0,
                        view_count INTEGER DEFAULT 0,
                        like_count INTEGER DEFAULT 0,
                        comment_count INTEGER DEFAULT 0,
                        duration_seconds INTEGER DEFAULT 0,
                        duration_formatted TEXT,
                        upload_date DATETIME,
                        thumbnail_url TEXT,
                        video_url TEXT,
                        search_keyword TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # search_history 테이블 생성
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS search_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        keyword TEXT NOT NULL,
                        results_count INTEGER DEFAULT 0,
                        search_date DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 인덱스 생성
                indexes = [
                    "CREATE UNIQUE INDEX IF NOT EXISTS idx_videos_video_id ON videos(video_id)",
                    "CREATE INDEX IF NOT EXISTS idx_videos_view_count ON videos(view_count DESC)",
                    "CREATE INDEX IF NOT EXISTS idx_videos_upload_date ON videos(upload_date DESC)",
                    "CREATE INDEX IF NOT EXISTS idx_videos_search_keyword ON videos(search_keyword)",
                    "CREATE INDEX IF NOT EXISTS idx_videos_subscriber_count ON videos(subscriber_count)",
                    "CREATE INDEX IF NOT EXISTS idx_search_history_keyword ON search_history(keyword)",
                    "CREATE INDEX IF NOT EXISTS idx_search_history_date ON search_history(search_date DESC)"
                ]
                
                for index_sql in indexes:
                    cursor.execute(index_sql)
                
                conn.commit()
                logger.info("데이터베이스 초기화 완료")
                
        except Exception as e:
            logger.error(f"데이터베이스 초기화 실패: {e}")
            raise
    
    def save_video(self, video: Video) -> bool:
        """영상 데이터 저장 (INSERT OR REPLACE)
        
        Args:
            video: 저장할 영상 데이터
            
        Returns:
            저장 성공 여부
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 현재 시간으로 updated_at 설정
                video.updated_at = datetime.now()
                if not video.created_at:
                    video.created_at = video.updated_at
                
                cursor.execute("""
                    INSERT OR REPLACE INTO videos (
                        video_id, title, channel_name, channel_id,
                        subscriber_count, view_count, like_count, comment_count,
                        duration_seconds, duration_formatted, upload_date,
                        thumbnail_url, video_url, search_keyword,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    video.video_id, video.title, video.channel_name, video.channel_id,
                    video.subscriber_count, video.view_count, video.like_count, video.comment_count,
                    video.duration_seconds, video.duration_formatted, video.upload_date,
                    video.thumbnail_url, video.video_url, video.search_keyword,
                    video.created_at, video.updated_at
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"영상 데이터 저장 실패: {e}")
            return False
    
    def save_videos_batch(self, videos: List[Video]) -> int:
        """영상 데이터 배치 저장
        
        Args:
            videos: 저장할 영상 리스트
            
        Returns:
            저장된 영상 수
        """
        if not videos:
            return 0
        
        saved_count = 0
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for video in videos:
                    try:
                        video.updated_at = datetime.now()
                        if not video.created_at:
                            video.created_at = video.updated_at
                        
                        cursor.execute("""
                            INSERT OR REPLACE INTO videos (
                                video_id, title, channel_name, channel_id,
                                subscriber_count, view_count, like_count, comment_count,
                                duration_seconds, duration_formatted, upload_date,
                                thumbnail_url, video_url, search_keyword,
                                created_at, updated_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            video.video_id, video.title, video.channel_name, video.channel_id,
                            video.subscriber_count, video.view_count, video.like_count, video.comment_count,
                            video.duration_seconds, video.duration_formatted, video.upload_date,
                            video.thumbnail_url, video.video_url, video.search_keyword,
                            video.created_at, video.updated_at
                        ))
                        saved_count += 1
                        
                    except Exception as e:
                        logger.warning(f"영상 저장 실패 (video_id: {video.video_id}): {e}")
                
                conn.commit()
                logger.info(f"배치 저장 완료: {saved_count}/{len(videos)}")
                
        except Exception as e:
            logger.error(f"배치 저장 실패: {e}")
        
        return saved_count
    
    def get_videos_by_keyword(self, keyword: str, limit: int = 20) -> List[Video]:
        """키워드로 영상 검색
        
        Args:
            keyword: 검색 키워드
            limit: 최대 결과 수
            
        Returns:
            영상 리스트
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM videos 
                    WHERE search_keyword = ? 
                    ORDER BY view_count DESC 
                    LIMIT ?
                """, (keyword, limit))
                
                rows = cursor.fetchall()
                return [Video.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            logger.error(f"영상 검색 실패: {e}")
            return []
    
    def get_all_videos(self, limit: int = 100) -> List[Video]:
        """모든 영상 조회
        
        Args:
            limit: 최대 결과 수
            
        Returns:
            영상 리스트
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM videos 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                return [Video.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            logger.error(f"전체 영상 조회 실패: {e}")
            return []
    
    def add_search_history(self, keyword: str, results_count: int) -> bool:
        """검색 히스토리 추가
        
        Args:
            keyword: 검색 키워드
            results_count: 결과 수
            
        Returns:
            추가 성공 여부
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO search_history (keyword, results_count)
                    VALUES (?, ?)
                """, (keyword, results_count))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"검색 히스토리 추가 실패: {e}")
            return False
    
    def get_search_history(self, limit: int = 50) -> List[SearchHistory]:
        """검색 히스토리 조회
        
        Args:
            limit: 최대 결과 수
            
        Returns:
            검색 히스토리 리스트
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM search_history 
                    ORDER BY search_date DESC 
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                return [SearchHistory.from_dict(dict(row)) for row in rows]
                
        except Exception as e:
            logger.error(f"검색 히스토리 조회 실패: {e}")
            return []
    
    def get_popular_keywords(self, limit: int = 10) -> List[Dict[str, Any]]:
        """인기 키워드 조회
        
        Args:
            limit: 최대 결과 수
            
        Returns:
            키워드와 검색 횟수 리스트
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT keyword, COUNT(*) as search_count 
                    FROM search_history 
                    GROUP BY keyword 
                    ORDER BY search_count DESC 
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                return [{'keyword': row['keyword'], 'count': row['search_count']} for row in rows]
                
        except Exception as e:
            logger.error(f"인기 키워드 조회 실패: {e}")
            return []
    
    def get_database_stats(self) -> Dict[str, int]:
        """데이터베이스 통계 조회
        
        Returns:
            통계 정보 딕셔너리
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 영상 수
                cursor.execute("SELECT COUNT(*) as count FROM videos")
                video_count = cursor.fetchone()['count']
                
                # 검색 히스토리 수
                cursor.execute("SELECT COUNT(*) as count FROM search_history")
                search_count = cursor.fetchone()['count']
                
                # 고유 키워드 수
                cursor.execute("SELECT COUNT(DISTINCT keyword) as count FROM search_history")
                unique_keywords = cursor.fetchone()['count']
                
                return {
                    'total_videos': video_count,
                    'total_searches': search_count,
                    'unique_keywords': unique_keywords
                }
                
        except Exception as e:
            logger.error(f"데이터베이스 통계 조회 실패: {e}")
            return {'total_videos': 0, 'total_searches': 0, 'unique_keywords': 0}
    
    def cleanup_old_data(self, days: int = 90) -> int:
        """오래된 데이터 정리
        
        Args:
            days: 보관 기간 (일)
            
        Returns:
            삭제된 레코드 수
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 오래된 검색 히스토리 삭제
                cursor.execute("""
                    DELETE FROM search_history 
                    WHERE search_date < datetime('now', '-{} days')
                """.format(days))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                logger.info(f"오래된 데이터 정리 완료: {deleted_count}개 삭제")
                return deleted_count
                
        except Exception as e:
            logger.error(f"데이터 정리 실패: {e}")
            return 0