# YouTube Keyword Analytics Tool - PRD (Product Requirements Document)

## 1. 프로젝트 개요

### 1.1 프로젝트명
YouTube Keyword Analytics Tool

### 1.2 목적
키워드 기반 YouTube 영상 분석을 통한 콘텐츠 트렌드 파악 및 경쟁 분석 자동화 도구

### 1.3 배경
- 매일 반복되는 키워드별 YouTube 검색 작업의 자동화 필요
- 조회수 대비 구독자 수가 낮은 채널 발굴을 통한 기회 분석
- 긴 영상 콘텐츠 트렌드 파악 및 최신 업로드 영상 모니터링

## 2. 핵심 기능 요구사항

### 2.1 메인 기능
1. **키워드 기반 검색**
   - 사용자가 입력한 키워드로 YouTube 영상 검색
   - 복수 키워드 지원 (쉼표로 구분)

2. **4가지 필터링 조건 자동 적용**
   - 조회수 높은 영상 우선 정렬
   - 구독자 수 10,000명 이하 채널만 필터링
   - 영상 길이 20분 이상만 필터링
   - 최근 1개월 이내 업로드 영상만 필터링

3. **결과 출력**
   - 조건에 맞는 영상 20개 추출
   - 조회수 순으로 정렬하여 표시

### 2.2 데이터 관리 기능
1. **로컬 저장**
   - SQLite 데이터베이스에 검색 결과 저장
   - 중복 데이터 자동 제거
   - 검색 히스토리 관리

2. **CSV 내보내기**
   - Pandas를 활용한 CSV 파일 생성
   - 사용자 지정 파일명으로 저장
   - 엑셀 호환 형식 지원

### 2.3 사용자 인터페이스
1. **다크 모드 GUI (PySide6)**
   - 모던하고 직관적인 인터페이스
   - 눈의 피로감 최소화를 위한 다크 테마

2. **주요 UI 구성 요소**
   - YouTube API 키 입력 필드
   - 키워드 입력 필드
   - 검색 실행 버튼
   - 진행 상황 표시바
   - 결과 테이블 뷰
   - CSV 내보내기 버튼

## 3. 기술 스펙

### 3.1 개발 환경
- **언어**: Python 3.8+
- **GUI 프레임워크**: PySide6
- **데이터 처리**: Pandas
- **데이터베이스**: SQLite
- **API**: YouTube Data API v3

### 3.2 필수 라이브러리
```
PySide6==6.6.0
pandas==2.1.3
requests==2.31.0
google-api-python-client==2.108.0
google-auth-oauthlib==1.1.0
keyring==24.3.0
```

## 4. 데이터 구조

### 4.1 수집 데이터 필드
| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| video_id | str | YouTube 영상 고유 ID | "dQw4w9WgXcQ" |
| title | str | 영상 제목 | "Amazing Tutorial Video" |
| channel_name | str | 채널명 | "Tech Channel" |
| channel_id | str | 채널 고유 ID | "UCxxxxxx" |
| subscriber_count | int | 구독자 수 | 5000 |
| view_count | int | 조회수 | 50000 |
| like_count | int | 좋아요 수 | 1200 |
| comment_count | int | 댓글 수 | 150 |
| duration_seconds | int | 영상 길이(초) | 1320 |
| duration_formatted | str | 영상 길이(포맷) | "22:00" |
| upload_date | datetime | 업로드 날짜 | "2024-01-15 10:30:00" |
| thumbnail_url | str | 썸네일 URL | "https://i.ytimg.com/vi/xxx.jpg" |
| video_url | str | 영상 URL | "https://youtube.com/watch?v=xxx" |
| search_keyword | str | 검색 키워드 | "python tutorial" |

### 4.2 데이터베이스 스키마
```sql
CREATE TABLE videos (
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_video_id ON videos(video_id);
CREATE INDEX idx_view_count ON videos(view_count DESC);
CREATE INDEX idx_upload_date ON videos(upload_date DESC);
CREATE INDEX idx_search_keyword ON videos(search_keyword);
```

## 5. 사용자 워크플로우

### 5.1 초기 설정 플로우
```
앱 실행 → API 키 입력 → 유효성 검사 → 설정 완료
```

### 5.2 검색 플로우
```
키워드 입력 → 검색 시작 → 진행률 표시 → 결과 표시 → 자동 저장
```

### 5.3 데이터 내보내기 플로우
```
검색 완료 → CSV 내보내기 선택 → 저장 위치 지정 → 파일 생성
```

## 6. 검색 조건 상세

### 6.1 필터링 조건
1. **조회수 기준**: 높은 순으로 정렬
2. **구독자 수**: 10,000명 이하 채널만 포함
3. **영상 길이**: 20분(1200초) 이상
4. **업로드 날짜**: 최근 30일 이내

### 6.2 검색 로직
```python
def search_criteria():
    return {
        'order': 'viewCount',  # 조회수 순 정렬
        'publishedAfter': (datetime.now() - timedelta(days=30)),
        'videoDuration': 'long',  # 20분 이상
        'maxResults': 50,  # 1차 검색 결과
        'type': 'video'
    }

def filter_results(videos):
    filtered = []
    for video in videos:
        if (video['subscriber_count'] <= 10000 and 
            video['duration_seconds'] >= 1200 and
            video['view_count'] > 0):
            filtered.append(video)
    
    return sorted(filtered, key=lambda x: x['view_count'], reverse=True)[:20]
```

## 7. UI/UX 요구사항

### 7.1 다크 테마 디자인
- **배경색**: #2b2b2b (진한 회색)
- **서페이스**: #3c3c3c (중간 회색)
- **주요 색상**: #bb86fc (보라색)
- **보조 색상**: #03dac6 (청록색)
- **텍스트**: #ffffff (흰색)

### 7.2 레이아웃 구성
```
┌─────────────────────────────────────────┐
│ YouTube Keyword Analytics Tool v1.0     │
├─────────────────────────────────────────┤
│ API 설정                                │
│ [API 키 입력____________________] [저장] │
│ 상태: ● 연결됨                           │
├─────────────────────────────────────────┤
│ 검색 설정                               │
│ [키워드 입력____________________] [검색] │
│ 조건: 조회수↓ | 구독자≤10K | 20분+ | 1개월 │
├─────────────────────────────────────────┤
│ [███████████████████░░░] 85% 검색 중... │
├─────────────────────────────────────────┤
│ 검색 결과 (20개)                        │
│ ┌─────┬─────┬─────┬─────┬─────┬─────┐  │
│ │순위 │제목 │채널 │구독자│조회수│길이 │  │
│ │ 1   │...  │...  │5.2K │125K │22:15│  │
│ │ 2   │...  │...  │8.9K │98K  │25:30│  │
│ └─────┴─────┴─────┴─────┴─────┴─────┘  │
├─────────────────────────────────────────┤
│ [📊 CSV 내보내기] [🔄 새로고침] [ℹ️ 정보] │
└─────────────────────────────────────────┘
```

## 8. 성능 요구사항

### 8.1 응답 시간
- API 호출당 최대 3초
- 20개 영상 검색 완료: 최대 15초
- UI 반응성: 100ms 이내

### 8.2 메모리 사용량
- 최대 메모리 사용량: 300MB 이하
- 데이터베이스 크기: 100MB 이하 (10,000개 레코드 기준)

### 8.3 API 사용량 최적화
- 일일 할당량: 10,000 units
- 검색당 사용량: 약 105 units
- 일일 최대 검색 횟수: 약 95회

## 9. 에러 처리 및 예외 상황

### 9.1 API 관련 에러
- **할당량 초과**: 사용자에게 알림 및 재시도 시간 안내
- **API 키 오류**: 즉시 알림 및 재입력 요청
- **네트워크 오류**: 자동 재시도 (최대 3회)

### 9.2 데이터 관련 에러
- **중복 데이터**: 자동으로 업데이트
- **손상된 데이터**: 검증 후 제외
- **빈 검색 결과**: 다른 키워드 제안

## 10. 보안 및 프라이버시

### 10.1 API 키 보안
- 로컬 키링(keyring)을 통한 암호화 저장
- 메모리에서 키 정보 자동 삭제
- 로그에 API 키 노출 방지

### 10.2 데이터 프라이버시
- 모든 데이터 로컬 저장
- 개인정보 수집하지 않음
- 공개 데이터만 수집

## 11. 향후 확장 계획

### 11.1 Phase 2 기능
- 키워드별 트렌드 분석 차트
- 자동 스케줄링 기능
- 이메일 리포트 발송

### 11.2 Phase 3 기능
- AI 기반 키워드 추천
- 경쟁사 분석 기능
- 다중 플랫폼 지원 (TikTok, Instagram)

## 12. 성공 기준

### 12.1 기능적 성공 기준
- 키워드 검색 정확도 95% 이상
- 4가지 필터 조건 100% 적용
- 데이터 중복률 1% 이하

### 12.2 사용성 성공 기준
- 사용자 학습 시간 5분 이내
- 일일 검색 시간 30분 → 5분 단축
- 사용자 만족도 4.5/5 이상

---

이 PRD를 바탕으로 사용자의 요구사항을 정확히 충족하는 YouTube 키워드 분석 도구를 개발할 예정입니다.