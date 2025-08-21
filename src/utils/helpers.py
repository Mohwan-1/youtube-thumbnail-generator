"""헬퍼 함수 모듈"""

import re
import logging
from datetime import datetime, timedelta
from typing import Union, Tuple
import isodate

logger = logging.getLogger(__name__)


class FormatHelper:
    """형식 변환 헬퍼 클래스"""
    
    @staticmethod
    def format_number(number: Union[int, float], korean_style: bool = True) -> str:
        """숫자를 읽기 쉬운 형태로 변환
        
        Args:
            number: 변환할 숫자
            korean_style: 한국식 표기 사용 여부
            
        Returns:
            형식화된 문자열 (예: 1234 -> "1.2K")
        """
        if not isinstance(number, (int, float)) or number < 0:
            return "0"
        
        if number < 1000:
            return str(int(number))
        elif number < 10000:
            if korean_style:
                return f"{number/1000:.1f}K"
            else:
                return f"{int(number):,}"
        elif number < 100000:
            if korean_style:
                return f"{number/10000:.1f}만"
            else:
                return f"{number/1000:.0f}K"
        elif number < 1000000:
            if korean_style:
                return f"{number/10000:.0f}만"
            else:
                return f"{number/1000:.0f}K"
        elif number < 100000000:
            if korean_style:
                return f"{number/10000:.0f}만"
            else:
                return f"{number/1000000:.1f}M"
        else:
            if korean_style:
                return f"{number/100000000:.1f}억"
            else:
                return f"{number/1000000:.0f}M"
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """초를 시:분:초 형식으로 변환
        
        Args:
            seconds: 총 초 수
            
        Returns:
            형식화된 시간 문자열 (예: "1:23:45" 또는 "23:45")
        """
        if not isinstance(seconds, int) or seconds < 0:
            return "0:00"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    @staticmethod
    def parse_iso_duration(duration_str: str) -> Tuple[int, str]:
        """ISO 8601 duration을 초와 형식화된 문자열로 변환
        
        Args:
            duration_str: ISO 8601 형식 (예: "PT20M15S")
            
        Returns:
            (총 초 수, 형식화된 문자열) 튜플
        """
        try:
            duration = isodate.parse_duration(duration_str)
            total_seconds = int(duration.total_seconds())
            formatted = FormatHelper.format_duration(total_seconds)
            return total_seconds, formatted
        except Exception as e:
            logger.warning(f"Duration 파싱 실패: {duration_str} - {e}")
            return 0, "0:00"
    
    @staticmethod
    def format_date(date: datetime, relative: bool = True) -> str:
        """날짜를 읽기 쉬운 형태로 변환
        
        Args:
            date: 변환할 날짜
            relative: 상대적 시간 표시 여부
            
        Returns:
            형식화된 날짜 문자열
        """
        if not isinstance(date, datetime):
            return "알 수 없음"
        
        now = datetime.now()
        
        if relative and date.date() == now.date():
            return f"오늘 {date.strftime('%H:%M')}"
        elif relative and date.date() == (now - timedelta(days=1)).date():
            return f"어제 {date.strftime('%H:%M')}"
        elif relative and (now - date).days < 7:
            days_ago = (now - date).days
            return f"{days_ago}일 전"
        elif relative and (now - date).days < 30:
            weeks_ago = (now - date).days // 7
            return f"{weeks_ago}주 전"
        else:
            return date.strftime('%Y-%m-%d')
    
    @staticmethod
    def format_percentage(value: float, decimal_places: int = 1) -> str:
        """백분율 형식으로 변환
        
        Args:
            value: 0-1 사이의 값
            decimal_places: 소수점 자릿수
            
        Returns:
            백분율 문자열 (예: "85.5%")
        """
        if not isinstance(value, (int, float)):
            return "0%"
        
        percentage = value * 100
        return f"{percentage:.{decimal_places}f}%"


class TextHelper:
    """텍스트 처리 헬퍼 클래스"""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
        """텍스트를 지정된 길이로 자르기
        
        Args:
            text: 원본 텍스트
            max_length: 최대 길이
            suffix: 생략 표시
            
        Returns:
            잘린 텍스트
        """
        if not text or len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def clean_html(text: str) -> str:
        """HTML 태그 제거
        
        Args:
            text: HTML이 포함된 텍스트
            
        Returns:
            정리된 텍스트
        """
        if not text:
            return ""
        
        # HTML 태그 제거
        clean = re.sub(r'<[^>]+>', '', text)
        
        # HTML 엔티티 변환
        html_entities = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#39;': "'",
            '&nbsp;': ' '
        }
        
        for entity, char in html_entities.items():
            clean = clean.replace(entity, char)
        
        # 여러 공백을 하나로
        clean = re.sub(r'\s+', ' ', clean)
        
        return clean.strip()
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 5) -> list:
        """텍스트에서 키워드 추출
        
        Args:
            text: 분석할 텍스트
            max_keywords: 최대 키워드 수
            
        Returns:
            키워드 리스트
        """
        if not text:
            return []
        
        # 텍스트 정리
        clean_text = TextHelper.clean_html(text.lower())
        
        # 불용어 제거 (간단한 한국어/영어 불용어)
        stop_words = {
            '그', '이', '그것', '저것', '것', '수', '등', '및', '또는', '하지만', '그러나',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        # 단어 추출 (한글, 영문, 숫자만)
        words = re.findall(r'[a-zA-Z가-힣]+', clean_text)
        
        # 불용어 제거 및 길이 필터링
        keywords = [word for word in words 
                   if word not in stop_words and len(word) >= 2]
        
        # 빈도수 계산
        word_count = {}
        for word in keywords:
            word_count[word] = word_count.get(word, 0) + 1
        
        # 빈도순 정렬
        sorted_keywords = sorted(word_count.items(), 
                               key=lambda x: x[1], reverse=True)
        
        return [word for word, count in sorted_keywords[:max_keywords]]


class URLHelper:
    """URL 처리 헬퍼 클래스"""
    
    @staticmethod
    def build_youtube_url(video_id: str) -> str:
        """YouTube 영상 URL 생성
        
        Args:
            video_id: YouTube 영상 ID
            
        Returns:
            완전한 YouTube URL
        """
        if not video_id:
            return ""
        
        return f"https://www.youtube.com/watch?v={video_id}"
    
    @staticmethod
    def build_channel_url(channel_id: str) -> str:
        """YouTube 채널 URL 생성
        
        Args:
            channel_id: YouTube 채널 ID
            
        Returns:
            완전한 채널 URL
        """
        if not channel_id:
            return ""
        
        return f"https://www.youtube.com/channel/{channel_id}"
    
    @staticmethod
    def extract_video_id(url: str) -> str:
        """YouTube URL에서 영상 ID 추출
        
        Args:
            url: YouTube URL
            
        Returns:
            영상 ID 또는 빈 문자열
        """
        if not url:
            return ""
        
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return ""