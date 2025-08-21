# 썸네일 자동 생성기

유튜버들을 위한 간단한 썸네일 생성 MVP.
영상 제목과 키워드만 입력하면 3~5개의 썸네일을 자동으로 생성합니다.

## 주요 기능
- 텍스트 입력 기반 썸네일 자동 생성 (Google Gemini API)
- 썸네일 선택 후 PNG/JPG 다운로드
- 구글 애드센스 광고 영역 내장
  - 자동광고: 좌/우 사이드바
  - 수동광고: 상단, 중간, 하단
- 다크모드 UI + 로고/파비콘 적용
- Vercel 배포

## API 설정
1. Google Gemini API KEY 발급
   - [Google Cloud Console](https://console.cloud.google.com) 접속
   - “API 키 생성” 버튼 클릭
2. 사이트 상단의 **API KEY 안내 버튼** 클릭 시, 상세 가이드 페이지로 이동

## 실행 방법
```bash
npm install
npm run dev
