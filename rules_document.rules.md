# YouTube Keyword Analytics Tool - 개발 규칙 및 가이드라인

## 📐 코딩 스타일 가이드

### 1. Python 코딩 컨벤션
- **PEP 8** 표준 엄격 준수
- 들여쓰기: 스페이스 4개 (탭 사용 금지)
- 최대 줄 길이: 88자 (Black 포맷터 기준)
- 인코딩: UTF-8 필수

#### 네이밍 컨벤션
```python
# 변수명 및 함수명: snake_case
user_keyword = "파이썬 강의"
search_results = []

def search_youtube_videos(keyword: str) -> List[Dict]:
    pass

# 클래스명: PascalCase
class YouTubeAnalyzer:
    pass

class DatabaseManager:
    pass

# 상수: UPPER_SNAKE_CASE
API_VERSION = "v3"
MAX_RESULTS_PER_SEARCH = 20
MIN_VIDEO_DURATION = 1200  # 20분 = 1200초

# 비공개 메서드: _underscore_prefix
def _parse_duration(self, duration_str: str) -> int:
    pass
```

#### 타입 힌트 필수 사용
```python
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

def filter_videos_by_criteria(
    videos: List[Dict[str, Any]], 
    max_subscribers: int = 10000,
    min_duration: int = 1200
) -> List[Dict[str, Any]]:
    """영상 필터링 함수
    
    Args:
        videos: 원본 영상 리스트
        max_subscribers: 최대 구독자 수
        min_duration: 최소 영상 길이(초)
    
    Returns:
        필터링된 영상 리스트
    """
    pass
```

### 2. 파일 및 디렉토리 구조

```
youtube-keyword-analytics/
├── main.py                     # 메인 실행 파일
├── requirements.txt            # 패키지 의존성
├── README.md                  # 사용 설명서
├── .gitignore                 # Git 무시 파일
├── .github/                   # GitHub 설정
│   └── workflows/
│       └── ci.yml            # GitHub Actions
├── src/                       # 핵심 소스 코드
│   ├── __init__.py
│   ├── gui/                   # GUI 관련 모듈
│   │   ├── __init__.py
│   │   ├── main_window.py     # 메인 윈도우
│   │   ├── widgets.py         # 커스텀 위젯
│   │   ├── styles.py          # 다크테마 스타일
│   │   └── dialogs.py         # 다이얼로그
│   ├── api/                   # YouTube API 관련
│   │   ├── __init__.py
│   │   ├── client.py          # API 클라이언트
│   │   ├── parser.py          # 데이터 파싱
│   │   └── filters.py         # 검색 필터
│   ├── database/              # 데이터베이스 관련
│   │   ├── __init__.py
│   │   ├── manager.py         # DB 매니저
│   │   ├── models.py          # 데이터 모델
│   │   └── migrations.py      # DB 마이그레이션
│   ├── utils/                 # 유틸리티 함수
│   │   ├── __init__.py
│   │   ├── config.py          # 설정 관리
│   │   ├── logger.py          # 로깅 설정
│   │   ├── helpers.py         # 헬퍼 함수
│   │   └── validators.py      # 데이터 검증
│   └── workers/               # 백그라운드 작업
│       ├── __init__.py
│       ├── search_worker.py   # 검색 워커
│       └── export_worker.py   # 내보내기 워커
├── tests/                     # 테스트 코드
│   ├── __init__.py
│   ├── test_api/
│   ├── test_database/
│   ├── test_gui/
│   └── test_utils/
├── docs/                      # 문서
│   ├── API.md
│   ├── DEVELOPMENT.md
│   └── DEPLOYMENT.md
├── data/                      # 데이터 파일
│   └── youtube_analytics.db   # SQLite DB
├── logs/                      # 로그 파일
│   └── app.log
└── exports/                   # CSV 내보내기
    └── (동적 생성)
```

## 🎨 UI/UX 개발 규칙

### 1. 다크 테마 색상 팔레트
```python
# src/gui/styles.py
class DarkTheme:
    """다크 테마 색상 정의"""
    
    # 기본 배경색
    BACKGROUND_PRIMARY = "#2b2b2b"      # 메인 배경
    BACKGROUND_SECONDARY = "#3c3c3c"    # 카드, 패널 배경
    BACKGROUND_TERTIARY = "#404040"     # 입력 필드 배경
    
    # 텍스트 색상
    TEXT_PRIMARY = "#ffffff"            # 주요 텍스트
    TEXT_SECONDARY = "#b3b3b3"          # 보조 텍스트
    TEXT_DISABLED = "#666666"           # 비활성 텍스트
    
    # 브랜드 색상
    PRIMARY = "#bb86fc"                 # 주요 액션 버튼
    PRIMARY_HOVER = "#985eff"           # 호버 상태
    PRIMARY_PRESSED = "#7c4dff"         # 눌린 상태
    
    # 보조 색상
    SECONDARY = "#03dac6"               # 보조 버튼, 링크
    SUCCESS = "#4caf50"                 # 성공 메시지
    WARNING = "#ff9800"                 # 경고 메시지
    ERROR = "#f44336"                   # 오류 메시지
    
    # 경계선 및 구분선
    BORDER = "#555555"                  # 기본 경계선
    BORDER_LIGHT = "#666666"            # 밝은 경계선
    DIVIDER = "#484848"                 # 구분선
```

### 2. 폰트 및 타이포그래피
```python
class Typography:
    """폰트 설정"""
    
    FONT_FAMILY = "Segoe UI, Malgun Gothic, Arial, sans-serif"
    
    # 폰트 크기
    FONT_SIZE_TITLE = 18        # 창 제목
    FONT_SIZE_SUBTITLE = 16     # 섹션 제목
    FONT_SIZE_BODY = 12         # 본문 텍스트
    FONT_SIZE_CAPTION = 10      # 캡션, 도움말
    FONT_SIZE_BUTTON = 11       # 버튼 텍스트
    
    # 폰트 두께
    FONT_WEIGHT_NORMAL = "normal"
    FONT_WEIGHT_BOLD = "bold"
    
    # 줄 간격
    LINE_HEIGHT_NORMAL = 1.4
    LINE_HEIGHT_COMPACT = 1.2
```

### 3. 컴포넌트 스타일링 규칙
```python
# 버튼 스타일 표준
BUTTON_PRIMARY = f"""
QPushButton {{
    background-color: {DarkTheme.PRIMARY};
    color: {DarkTheme.TEXT_PRIMARY};
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    font-size: {Typography.FONT_SIZE_BUTTON}px;
    min-height: 32px;
}}
QPushButton:hover {{
    background-color: {DarkTheme.PRIMARY_HOVER};
}}
QPushButton:pressed {{
    background-color: {DarkTheme.PRIMARY_PRESSED};
}}
QPushButton:disabled {{
    background-color: {DarkTheme.TEXT_DISABLED};
    color: {DarkTheme.TEXT_DISABLED};
}}
"""

# 입력 필드 스타일 표준
INPUT_FIELD = f"""
QLineEdit {{
    background-color: {DarkTheme.BACKGROUND_TERTIARY};
    border: 2px solid {DarkTheme.BORDER};
    border-radius: 4px;
    padding: 8px 12px;
    color: {DarkTheme.TEXT_PRIMARY};
    font-size: {Typography.FONT_SIZE_BODY}px;
    min-height: 20px;
}}
QLineEdit:focus {{
    border-color: {DarkTheme.PRIMARY};
}}
QLineEdit:disabled {{
    background-color: {DarkTheme.TEXT_DISABLED};
    color: {DarkTheme.TEXT_DISABLED};
}}
"""
```

## 🛡️ 보안 및 데이터 처리 규칙

### 1. API 키 보안 관리
```python
import keyring
from cryptography.fernet import Fernet
import os

class SecureConfig:
    """보안 설정 관리"""
    
    SERVICE_NAME = "youtube_analytics"
    KEY_NAME = "api_key"
    
    @classmethod
    def save_api_key(cls, api_key: str) -> bool:
        """API 키를 안전하게 저장"""
        try:
            keyring.set_password(cls.SERVICE_NAME, cls.KEY_NAME, api_key)
            return True
        except Exception as e:
            logger.error(f"API 키 저장 실패: {e}")
            return False
    
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """저장된 API 키 가져오기"""
        try:
            return keyring.get_password(cls.SERVICE_NAME, cls.KEY_NAME)
        except Exception as e:
            logger.error(f"API 키 조회 실패: {e}")
            return None
    
    @classmethod
    def delete_api_key(cls) -> bool:
        """API 키 삭제"""
        try:
            keyring.delete_password(cls.SERVICE_NAME, cls.KEY_NAME)
            return True
        except Exception as e:
            logger.error(f"API 키 삭제 실패: {e}")
            return False
```

### 2. 데이터 검증 및 정제
```python
from typing import Dict, Any
import re
from datetime import datetime

class DataValidator:
    """데이터 검증 클래스"""
    
    @staticmethod
    def validate_video_data(video: Dict[str, Any]) -> bool:
        """영상 데이터 유효성 검사"""
        required_fields = ['video_id', 'title', 'channel_name']
        
        # 필수 필드 존재 확인
        for field in required_fields:
            if field not in video or not video[field]:
                return False
        
        # 숫자 필드 검증
        numeric_fields = ['view_count', 'subscriber_count', 'duration_seconds']
        for field in numeric_fields:
            if field in video and not isinstance(video[field], (int, float)):
                try:
                    video[field] = int(video[field])
                except (ValueError, TypeError):
                    video[field] = 0
        
        return True
    
    @staticmethod
    def sanitize_keyword(keyword: str) -> str:
        """키워드 정제"""
        # 특수문자 제거
        keyword = re.sub(r'[^\w\s가-힣]', ' ', keyword)
        # 여러 공백을 하나로
        keyword = re.sub(r'\s+', ' ', keyword)
        # 앞뒤 공백 제거
        return keyword.strip()
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """API 키 형식 검증"""
        # Google API 키 형식: 39자 알파벳 숫자 조합
        pattern = r'^[A-Za-z0-9_-]{39}$'
        return bool(re.match(pattern, api_key))
```

### 3. 에러 처리 표준
```python
import logging
from functools import wraps
from typing import Callable, Any

# 로거 설정
logger = logging.getLogger(__name__)

class YouTubeAPIError(Exception):
    """YouTube API 관련 예외"""
    pass

class DatabaseError(Exception):
    """데이터베이스 관련 예외"""
    pass

class ValidationError(Exception):
    """데이터 검증 관련 예외"""
    pass

def handle_api_errors(func: Callable) -> Callable:
    """API 에러 처리 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"API 오류 발생 in {func.__name__}: {str(e)}"
            logger.error(error_msg)
            raise YouTubeAPIError(error_msg) from e
    return wrapper

def handle_database_errors(func: Callable) -> Callable:
    """데이터베이스 에러 처리 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"DB 오류 발생 in {func.__name__}: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg) from e
    return wrapper
```

## 📊 데이터베이스 설계 규칙

### 1. 스키마 설계 원칙
```sql
-- 테이블 이름: 복수형, snake_case
-- 컬럼 이름: snake_case
-- 인덱스 이름: idx_테이블명_컬럼명

CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT UNIQUE NOT NULL,           -- YouTube 영상 ID
    title TEXT NOT NULL,                     -- 영상 제목
    channel_name TEXT NOT NULL,              -- 채널명
    channel_id TEXT NOT NULL,                -- 채널 ID
    subscriber_count INTEGER DEFAULT 0,      -- 구독자 수
    view_count INTEGER DEFAULT 0,            -- 조회수
    like_count INTEGER DEFAULT 0,            -- 좋아요 수
    comment_count INTEGER DEFAULT 0,         -- 댓글 수
    duration_seconds INTEGER DEFAULT 0,      -- 영상 길이(초)
    duration_formatted TEXT,                 -- 형식화된 길이 (22:15)
    upload_date DATETIME,                    -- 업로드 날짜
    thumbnail_url TEXT,                      -- 썸네일 URL
    video_url TEXT,                          -- 영상 URL
    search_keyword TEXT,                     -- 검색 키워드
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 데이터 생성일
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP   -- 데이터 수정일
);

-- 필수 인덱스
CREATE UNIQUE INDEX idx_videos_video_id ON videos(video_id);
CREATE INDEX idx_videos_view_count ON videos(view_count DESC);
CREATE INDEX idx_videos_upload_date ON videos(upload_date DESC);
CREATE INDEX idx_videos_search_keyword ON videos(search_keyword);
CREATE INDEX idx_videos_subscriber_count ON videos(subscriber_count);

-- 검색 히스토리 테이블
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    results_count INTEGER DEFAULT 0,
    search_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_search_history_keyword ON search_history(keyword);
CREATE INDEX idx_search_history_date ON search_history(search_date DESC);
```

### 2. 데이터 정규화 규칙
```python
class DatabaseNormalizer:
    """데이터 정규화 클래스"""
    
    @staticmethod
    def normalize_view_count(view_count: Any) -> int:
        """조회수 정규화"""
        if isinstance(view_count, str):
            # "1.2K" -> 1200, "1.5M" -> 1500000
            view_count = view_count.replace(',', '')
            if 'K' in view_count:
                return int(float(view_count.replace('K', '')) * 1000)
            elif 'M' in view_count:
                return int(float(view_count.replace('M', '')) * 1000000)
        return int(view_count) if view_count else 0
    
    @staticmethod
    def normalize_duration(duration_str: str) -> tuple[int, str]:
        """영상 길이 정규화"""
        # PT20M15S -> (1215, "20:15")
        import re
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        
        if not match:
            return 0, "0:00"
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        total_seconds = hours * 3600 + minutes * 60 + seconds
        
        if hours > 0:
            formatted = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            formatted = f"{minutes}:{seconds:02d}"
        
        return total_seconds, formatted
```

## 🧪 테스트 작성 규칙

### 1. 테스트 구조
```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.api.client import YouTubeAPIClient
from src.database.manager import DatabaseManager

class TestYouTubeAPIClient:
    """YouTube API 클라이언트 테스트"""
    
    @pytest.fixture
    def api_client(self):
        """테스트용 API 클라이언트"""
        return YouTubeAPIClient("test_api_key")
    
    @pytest.fixture
    def mock_youtube_service(self):
        """Mock YouTube 서비스"""
        with patch('googleapiclient.discovery.build') as mock_build:
            yield mock_build.return_value
    
    def test_validate_api_key_success(self, api_client, mock_youtube_service):
        """API 키 유효성 검사 성공 테스트"""
        # Arrange
        mock_youtube_service.search().list().execute.return_value = {'items': []}
        
        # Act
        result = api_client.validate_api_key()
        
        # Assert
        assert result is True
        mock_youtube_service.search().list.assert_called_once()
    
    def test_validate_api_key_failure(self, api_client, mock_youtube_service):
        """API 키 유효성 검사 실패 테스트"""
        # Arrange
        from googleapiclient.errors import HttpError
        mock_youtube_service.search().list().execute.side_effect = HttpError(
            resp=Mock(status=403), content=b'{"error": {"message": "API key not valid"}}'
        )
        
        # Act
        result = api_client.validate_api_key()
        
        # Assert
        assert result is False
    
    @pytest.mark.parametrize("keyword,expected_count", [
        ("python", 20),
        ("javascript", 15),
        ("", 0),
    ])
    def test_search_videos_various_keywords(self, api_client, keyword, expected_count):
        """다양한 키워드로 검색 테스트"""
        with patch.object(api_client, '_fetch_videos') as mock_fetch:
            mock_fetch.return_value = [{'video_id': f'test_{i}'} for i in range(expected_count)]
            
            results = api_client.search_videos(keyword)
            
            assert len(results) == expected_count
```

### 2. 테스트 커버리지 요구사항
- **최소 커버리지**: 80%
- **핵심 모듈 커버리지**: 95% 이상
- **GUI 테스트 커버리지**: 60% 이상

### 3. 테스트 실행 규칙
```bash
# 모든 테스트 실행
pytest tests/ -v

# 커버리지 포함 테스트
pytest tests/ --cov=src --cov-report=html --cov-report=term

# 특정 모듈 테스트
pytest tests/test_api/ -v

# 마커별 테스트 실행
pytest -m "not slow" -v  # 빠른 테스트만
pytest -m "integration" -v  # 통합 테스트만

# 병렬 테스트 실행
pytest tests/ -n auto  # CPU 코어 수만큼 병렬 실행
```

## 🚀 성능 최적화 규칙

### 1. API 호출 최적화
```python
import time
import asyncio
from functools import wraps
from typing import Callable

class APIRateLimiter:
    """API 호출 속도 제한"""
    
    def __init__(self, max_calls_per_second: int = 5):
        self.max_calls = max_calls_per_second
        self.calls = []
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 1초 이내의 호출 기록만 유지
            self.calls = [call_time for call_time in self.calls if now - call_time < 1.0]
            
            if len(self.calls) >= self.max_calls:
                sleep_time = 1.0 - (now - self.calls[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper

# 사용 예시
@APIRateLimiter(max_calls_per_second=5)
def search_youtube_videos(keyword: str):
    # API 호출 로직
    pass
```

### 2. 메모리 사용량 최적화
```python
import gc
from typing import Generator, List, Dict, Any

class MemoryOptimizer:
    """메모리 최적화 도구"""
    
    @staticmethod
    def process_large_dataset(data: List[Dict[str, Any]], 
                            batch_size: int = 100) -> Generator[List[Dict], None, None]:
        """대용량 데이터를 배치 단위로 처리"""
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            yield batch
            
            # 배치 처리 후 가비지 컬렉션
            if i % (batch_size * 5) == 0:
                gc.collect()
    
    @staticmethod
    def cleanup_memory():
        """메모리 정리"""
        gc.collect()
    
    @staticmethod
    def get_memory_usage() -> float:
        """현재 메모리 사용량 반환 (MB)"""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024

# 사용 예시
def process_search_results(videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """검색 결과 처리"""
    processed_videos = []
    
    for batch in MemoryOptimizer.process_large_dataset(videos, batch_size=50):
        for video in batch:
            processed_video = process_single_video(video)
            processed_videos.append(processed_video)
    
    MemoryOptimizer.cleanup_memory()
    return processed_videos
```

### 3. 데이터베이스 성능 최적화
```python
import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any

class DatabaseOptimizer:
    """데이터베이스 성능 최적화"""
    
    @staticmethod
    @contextmanager
    def optimized_connection(db_path: str):
        """최적화된 데이터베이스 연결"""
        conn = sqlite3.connect(db_path)
        try:
            # 성능 최적화 설정
            conn.execute("PRAGMA journal_mode=WAL")          # Write-Ahead Logging
            conn.execute("PRAGMA synchronous=NORMAL")        # 동기화 모드
            conn.execute("PRAGMA cache_size=10000")          # 캐시 크기
            conn.execute("PRAGMA temp_store=MEMORY")         # 임시 저장소
            conn.execute("PRAGMA mmap_size=268435456")       # 메모리 맵 크기 (256MB)
            
            yield conn
        finally:
            conn.close()
    
    @staticmethod
    def bulk_insert(db_path: str, table: str, data: List[Dict[str, Any]], 
                   batch_size: int = 1000):
        """배치 단위 대량 삽입"""
        if not data:
            return
        
        # 컬럼명 추출
        columns = list(data[0].keys())
        placeholders = ','.join(['?' for _ in columns])
        
        insert_sql = f"""
            INSERT OR REPLACE INTO {table} 
            ({','.join(columns)}) 
            VALUES ({placeholders})
        """
        
        with DatabaseOptimizer.optimized_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # 배치 단위로 삽입
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                batch_values = [
                    [row[col] for col in columns] 
                    for row in batch
                ]
                
                cursor.executemany(insert_sql, batch_values)
                
                if i % (batch_size * 5) == 0:  # 5배치마다 커밋
                    conn.commit()
            
            conn.commit()
```

## 📝 로깅 및 모니터링 규칙

### 1. 로깅 설정 표준
```python
import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

class LoggerSetup:
    """로깅 설정 클래스"""
    
    @staticmethod
    def setup_logging(log_level: str = "INFO", 
                     log_dir: str = "logs",
                     max_file_size: int = 10 * 1024 * 1024,  # 10MB
                     backup_count: int = 5):
        """로깅 설정 초기화"""
        
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
        
        # 파일 핸들러 (크기 기반 로테이션)
        file_handler = RotatingFileHandler(
            filename=f"{log_dir}/app.log",
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        # 에러 로그 별도 파일
        error_handler = RotatingFileHandler(
            filename=f"{log_dir}/error.log",
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        
        # 핸들러 추가
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(error_handler)
        
        # 외부 라이브러리 로그 레벨 조정
        logging.getLogger('googleapiclient').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)

# 사용 예시
LoggerSetup.setup_logging(log_level="DEBUG")
logger = logging.getLogger(__name__)
```

### 2. 모니터링 및 디버깅
```python
import time
import functools
from typing import Callable, Any

def monitor_performance(func: Callable) -> Callable:
    """함수 실행 시간 모니터링 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        logger.debug(f"Starting {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.info(f"{func.__name__} completed in {execution_time:.2f}s")
            
            # 성능 임계값 검사
            if execution_time > 10.0:  # 10초 이상
                logger.warning(f"{func.__name__} took too long: {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f}s: {str(e)}")
            raise
    
    return wrapper

def log_function_calls(func: Callable) -> Callable:
    """함수 호출 로깅 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # 민감한 정보 필터링
        safe_args = [str(arg)[:100] if isinstance(arg, str) else str(type(arg)) for arg in args]
        safe_kwargs = {k: str(v)[:100] if isinstance(v, str) else str(type(v)) for k, v in kwargs.items()}
        
        logger.debug(f"Calling {func.__name__} with args={safe_args}, kwargs={safe_kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned {type(result)}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {type(e).__name__}: {str(e)}")
            raise
    
    return wrapper
```

## 🔄 CI/CD 및 배포 규칙

### 1. GitHub Actions 워크플로우
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

env:
  PYTHON_VERSION: '3.11'

jobs:
  test:
    name: Test on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503
        black --check src/ tests/
        mypy src/ --ignore-missing-imports
    
    - name: Run tests with coverage
      run: |
        pytest tests/ --cov=src --cov-report=xml --cov-report=term-missing --cov-fail-under=80
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Bandit security scan
      run: |
        pip install bandit[toml]
        bandit -r src/ -f json -o bandit-report.json
    
    - name: Run Safety check
      run: |
        pip install safety
        safety check --json --output safety-report.json
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

  build:
    name: Build Application
    needs: [test, security]
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build executable
      run: |
        pyinstaller --onefile --windowed --name="YouTubeAnalytics" main.py
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: youtube-analytics-${{ matrix.os }}
        path: dist/

  release:
    name: Create Release
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    
    steps:
    - name: Download all artifacts
      uses: actions/download-artifact@v3
    
    - name: Create release assets
      run: |
        zip -r youtube-analytics-windows.zip youtube-analytics-windows-latest/
        zip -r youtube-analytics-macos.zip youtube-analytics-macos-latest/
        zip -r youtube-analytics-linux.zip youtube-analytics-ubuntu-latest/
    
    - name: Upload release assets
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ github.event.release.upload_url }}
        asset_path: ./youtube-analytics-windows.zip
        asset_name: youtube-analytics-windows.zip
        asset_content_type: application/zip
```

### 2. 버전 관리 규칙
```python
# src/utils/version.py
"""버전 관리"""

__version__ = "1.0.0"

# 시맨틱 버저닝 규칙
# MAJOR.MINOR.PATCH
# MAJOR: 호환되지 않는 API 변경
# MINOR: 하위 호환되는 기능 추가
# PATCH: 하위 호환되는 버그 수정

VERSION_INFO = {
    "major": 1,
    "minor": 0,
    "patch": 0,
    "pre_release": None,  # alpha, beta, rc
    "build": None
}

def get_version_string() -> str:
    """버전 문자열 반환"""
    version = f"{VERSION_INFO['major']}.{VERSION_INFO['minor']}.{VERSION_INFO['patch']}"
    
    if VERSION_INFO['pre_release']:
        version += f"-{VERSION_INFO['pre_release']}"
    
    if VERSION_INFO['build']:
        version += f"+{VERSION_INFO['build']}"
    
    return version

def compare_versions(version1: str, version2: str) -> int:
    """버전 비교 (-1: v1 < v2, 0: v1 == v2, 1: v1 > v2)"""
    from packaging import version
    v1 = version.parse(version1)
    v2 = version.parse(version2)
    
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0
```

### 3. 배포 설정
```python
# setup.py
from setuptools import setup, find_packages
from src.utils.version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="youtube-keyword-analytics",
    version=__version__,
    author="YouTube Creator",
    author_email="creator@example.com",
    description="YouTube 키워드 기반 영상 분석 도구",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/youtube-keyword-analytics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "youtube-analytics=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["gui/styles/*.qss", "gui/icons/*.png"],
    },
)
```

## 🛡️ 보안 검사 체크리스트

### 1. 코드 보안 검사
```bash
# Bandit 보안 스캔
bandit -r src/ -f json -o security-report.json

# Safety 의존성 취약점 검사
safety check --json --output safety-report.json

# 코드 품질 검사
sonar-scanner \
  -Dsonar.projectKey=youtube-analytics \
  -Dsonar.sources=src/ \
  -Dsonar.host.url=http://localhost:9000
```

### 2. 배포 전 체크리스트
- [ ] 모든 테스트 통과
- [ ] 코드 커버리지 80% 이상
- [ ] 보안 스캔 통과
- [ ] 의존성 취약점 없음
- [ ] 문서 업데이트 완료
- [ ] 버전 번호 업데이트
- [ ] 체인지로그 작성
- [ ] 빌드 테스트 완료

---

이 개발 규칙과 가이드라인을 준수하여 안정적이고 유지보수가 용이한 YouTube Keyword Analytics Tool을 개발할 수 있습니다. 모든 개발자는 이 문서를 참고하여 일관된 코드 품질을 유지해야 합니다.