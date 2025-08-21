"""데이터 내보내기 모듈"""

import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import os

from ..database.models import Video
from .helpers import FormatHelper

logger = logging.getLogger(__name__)


class CSVExporter:
    """CSV 내보내기 클래스"""
    
    def __init__(self, export_dir: str = "exports"):
        """CSV 내보내기 초기화
        
        Args:
            export_dir: 내보내기 디렉토리
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
    
    def export_videos(
        self, 
        videos: List[Video], 
        filename: Optional[str] = None,
        keyword: str = "",
        include_stats: bool = True
    ) -> str:
        """영상 데이터를 CSV로 내보내기
        
        Args:
            videos: 내보낼 영상 리스트
            filename: 파일명 (기본값: 자동 생성)
            keyword: 검색 키워드 (파일명 생성용)
            include_stats: 통계 정보 포함 여부
            
        Returns:
            생성된 파일 경로
        """
        if not videos:
            raise ValueError("내보낼 영상 데이터가 없습니다")
        
        try:
            # 파일명 생성
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_keyword = self._sanitize_filename(keyword or "search")
                filename = f"youtube_search_{safe_keyword}_{timestamp}.csv"
            
            # 파일 경로
            filepath = self.export_dir / filename
            
            # 데이터프레임 생성
            df = self._create_dataframe(videos, include_stats)
            
            # CSV 저장
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"CSV 내보내기 완료: {filepath} ({len(videos)}개 영상)")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"CSV 내보내기 실패: {e}")
            raise
    
    def _create_dataframe(self, videos: List[Video], include_stats: bool = True) -> pd.DataFrame:
        """영상 데이터로 데이터프레임 생성
        
        Args:
            videos: 영상 리스트
            include_stats: 통계 정보 포함 여부
            
        Returns:
            pandas DataFrame
        """
        data = []
        
        for i, video in enumerate(videos, 1):
            row = {
                '순위': i,
                '영상제목': video.title,
                '채널명': video.channel_name,
                '구독자수': FormatHelper.format_number(video.subscriber_count),
                '조회수': FormatHelper.format_number(video.view_count),
                '영상길이': video.duration_formatted,
                '업로드날짜': FormatHelper.format_date(video.upload_date, relative=False) if video.upload_date else '',
                '영상URL': video.video_url,
                '검색키워드': video.search_keyword
            }
            
            # 상세 통계 정보 추가
            if include_stats:
                row.update({
                    '좋아요수': FormatHelper.format_number(video.like_count),
                    '댓글수': FormatHelper.format_number(video.comment_count),
                    '구독자수_숫자': video.subscriber_count,
                    '조회수_숫자': video.view_count,
                    '영상길이_초': video.duration_seconds,
                    '채널ID': video.channel_id,
                    '영상ID': video.video_id,
                    '썸네일URL': video.thumbnail_url
                })
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def export_search_summary(
        self,
        videos: List[Video],
        keyword: str,
        search_criteria: Dict[str, Any],
        filename: Optional[str] = None
    ) -> str:
        """검색 요약 정보를 CSV로 내보내기
        
        Args:
            videos: 영상 리스트
            keyword: 검색 키워드
            search_criteria: 검색 조건
            filename: 파일명
            
        Returns:
            생성된 파일 경로
        """
        try:
            # 파일명 생성
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_keyword = self._sanitize_filename(keyword)
                filename = f"search_summary_{safe_keyword}_{timestamp}.csv"
            
            filepath = self.export_dir / filename
            
            # 요약 데이터 생성
            summary_data = self._create_summary_data(videos, keyword, search_criteria)
            
            # CSV 저장
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"검색 요약 내보내기 완료: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"검색 요약 내보내기 실패: {e}")
            raise
    
    def _create_summary_data(
        self, 
        videos: List[Video], 
        keyword: str, 
        search_criteria: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """검색 요약 데이터 생성
        
        Args:
            videos: 영상 리스트
            keyword: 검색 키워드
            search_criteria: 검색 조건
            
        Returns:
            요약 데이터 리스트
        """
        if not videos:
            return []
        
        # 기본 통계
        total_views = sum(v.view_count for v in videos)
        avg_views = total_views // len(videos) if videos else 0
        avg_subscribers = sum(v.subscriber_count for v in videos) // len(videos) if videos else 0
        avg_duration = sum(v.duration_seconds for v in videos) // len(videos) if videos else 0
        
        # 상위 영상들
        top_videos = sorted(videos, key=lambda x: x.view_count, reverse=True)[:5]
        
        summary_data = [
            {'항목': '검색 키워드', '값': keyword},
            {'항목': '검색 일시', '값': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'항목': '총 결과 수', '값': len(videos)},
            {'항목': '평균 조회수', '값': FormatHelper.format_number(avg_views)},
            {'항목': '평균 구독자수', '값': FormatHelper.format_number(avg_subscribers)},
            {'항목': '평균 영상길이', '값': FormatHelper.format_duration(avg_duration)},
            {'항목': '', '값': ''},  # 구분선
            {'항목': '검색 조건', '값': ''},
            {'항목': '최대 구독자수', '값': FormatHelper.format_number(search_criteria.get('max_subscribers', 0))},
            {'항목': '최소 영상길이', '값': f"{search_criteria.get('min_duration_seconds', 0) // 60}분"},
            {'항목': '검색 기간', '값': f"최근 {search_criteria.get('days_back', 30)}일"},
            {'항목': '', '값': ''},  # 구분선
            {'항목': '상위 5개 영상', '값': ''},
        ]
        
        # 상위 영상 정보 추가
        for i, video in enumerate(top_videos, 1):
            summary_data.append({
                '항목': f'{i}위',
                '값': f"{video.title[:50]}... | {FormatHelper.format_number(video.view_count)} 조회수"
            })
        
        return summary_data
    
    def export_channel_analysis(self, videos: List[Video], filename: Optional[str] = None) -> str:
        """채널별 분석 데이터를 CSV로 내보내기
        
        Args:
            videos: 영상 리스트
            filename: 파일명
            
        Returns:
            생성된 파일 경로
        """
        try:
            # 파일명 생성
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"channel_analysis_{timestamp}.csv"
            
            filepath = self.export_dir / filename
            
            # 채널별 데이터 집계
            channel_data = self._aggregate_by_channel(videos)
            
            # 데이터프레임 생성 및 저장
            df = pd.DataFrame(channel_data)
            df = df.sort_values('총_조회수', ascending=False)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"채널별 분석 내보내기 완료: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"채널별 분석 내보내기 실패: {e}")
            raise
    
    def _aggregate_by_channel(self, videos: List[Video]) -> List[Dict[str, Any]]:
        """채널별 데이터 집계
        
        Args:
            videos: 영상 리스트
            
        Returns:
            채널별 집계 데이터
        """
        channel_stats = {}
        
        for video in videos:
            channel_id = video.channel_id
            
            if channel_id not in channel_stats:
                channel_stats[channel_id] = {
                    '채널명': video.channel_name,
                    '구독자수': video.subscriber_count,
                    '영상수': 0,
                    '총_조회수': 0,
                    '평균_조회수': 0,
                    '최고_조회수': 0,
                    '총_좋아요수': 0,
                    '평균_영상길이': 0,
                    '채널URL': f"https://www.youtube.com/channel/{channel_id}"
                }
            
            stats = channel_stats[channel_id]
            stats['영상수'] += 1
            stats['총_조회수'] += video.view_count
            stats['총_좋아요수'] += video.like_count
            stats['최고_조회수'] = max(stats['최고_조회수'], video.view_count)
        
        # 평균값 계산
        for stats in channel_stats.values():
            if stats['영상수'] > 0:
                stats['평균_조회수'] = stats['총_조회수'] // stats['영상수']
        
        # 포맷팅
        result = []
        for stats in channel_stats.values():
            formatted_stats = {
                '채널명': stats['채널명'],
                '구독자수': FormatHelper.format_number(stats['구독자수']),
                '영상수': stats['영상수'],
                '총_조회수': stats['총_조회수'],  # 정렬용 숫자값 유지
                '총조회수': FormatHelper.format_number(stats['총_조회수']),
                '평균조회수': FormatHelper.format_number(stats['평균_조회수']),
                '최고조회수': FormatHelper.format_number(stats['최고_조회수']),
                '총좋아요수': FormatHelper.format_number(stats['총_좋아요수']),
                '채널URL': stats['채널URL']
            }
            result.append(formatted_stats)
        
        return result
    
    def _sanitize_filename(self, filename: str) -> str:
        """파일명에서 유효하지 않은 문자 제거
        
        Args:
            filename: 원본 파일명
            
        Returns:
            정리된 파일명
        """
        # Windows에서 유효하지 않은 문자들 제거
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 공백을 언더스코어로 변경
        filename = filename.replace(' ', '_')
        
        # 연속된 언더스코어 정리
        while '__' in filename:
            filename = filename.replace('__', '_')
        
        # 길이 제한 (50자)
        if len(filename) > 50:
            filename = filename[:50]
        
        return filename.strip('_')
    
    def get_export_history(self) -> List[Dict[str, Any]]:
        """내보내기 히스토리 조회
        
        Returns:
            내보내기 파일 리스트
        """
        try:
            files = []
            for file_path in self.export_dir.glob("*.csv"):
                stat = file_path.stat()
                files.append({
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'size': stat.st_size,
                    'size_formatted': f"{stat.st_size / 1024:.1f} KB",
                    'created_at': datetime.fromtimestamp(stat.st_ctime),
                    'modified_at': datetime.fromtimestamp(stat.st_mtime)
                })
            
            # 수정일 기준 내림차순 정렬
            files.sort(key=lambda x: x['modified_at'], reverse=True)
            return files
            
        except Exception as e:
            logger.error(f"내보내기 히스토리 조회 실패: {e}")
            return []
    
    def cleanup_old_exports(self, days: int = 30) -> int:
        """오래된 내보내기 파일 정리
        
        Args:
            days: 보관 기간 (일)
            
        Returns:
            삭제된 파일 수
        """
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 3600)
            deleted_count = 0
            
            for file_path in self.export_dir.glob("*.csv"):
                if file_path.stat().st_mtime < cutoff_date:
                    file_path.unlink()
                    deleted_count += 1
            
            logger.info(f"오래된 내보내기 파일 정리 완료: {deleted_count}개 삭제")
            return deleted_count
            
        except Exception as e:
            logger.error(f"내보내기 파일 정리 실패: {e}")
            return 0