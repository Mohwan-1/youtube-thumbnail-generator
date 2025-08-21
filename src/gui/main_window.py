"""메인 윈도우 모듈"""

import logging
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QStatusBar, QMessageBox, QFileDialog, QApplication
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon, QPixmap, QAction
import sys
import os
from typing import List, Optional

from .widgets import (
    APIKeyWidget, SearchWidget, VideoTableWidget, ExportWidget,
    StatsWidget, LogWidget
)
from .styles import StyleSheets, DarkTheme
from ..utils.config import Config
from ..utils.logger import LoggerSetup
from ..utils.exporter import CSVExporter
from ..database.manager import DatabaseManager
from ..database.models import Video
from ..api.client import YouTubeAPIClient
from ..workers.search_worker import SearchWorker

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """메인 윈도우 클래스"""
    
    def __init__(self):
        super().__init__()
        
        # 설정 및 매니저 초기화
        self.config = Config()
        self.db_manager = DatabaseManager(self.config.get("database.filename", "data/youtube_analytics.db"))
        self.exporter = CSVExporter(self.config.get("export.default_dir", "exports"))
        self.youtube_client = None
        self.search_worker = None
        
        # 현재 검색 결과
        self.current_videos = []
        self.current_keyword = ""
        
        self.setup_ui()
        self.setup_connections()
        self.load_settings()
        
        logger.info("메인 윈도우 초기화 완료")
    
    def setup_ui(self):
        """UI 설정"""
        self.setWindowTitle("YouTube Keyword Analytics Tool v1.0")
        self.setMinimumSize(1200, 800)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 상단 컨트롤 영역
        controls_layout = QVBoxLayout()
        
        # API 키 위젯
        self.api_key_widget = APIKeyWidget()
        controls_layout.addWidget(self.api_key_widget)
        
        # 검색 위젯
        self.search_widget = SearchWidget()
        controls_layout.addWidget(self.search_widget)
        
        # 스플리터로 메인 콘텐츠 영역 구성
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 왼쪽 패널 (결과 테이블)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # 결과 테이블
        self.video_table = VideoTableWidget()
        left_layout.addWidget(self.video_table)
        
        # 내보내기 위젯
        self.export_widget = ExportWidget()
        left_layout.addWidget(self.export_widget)
        
        # 오른쪽 패널 (통계 및 로그)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 통계 위젯
        self.stats_widget = StatsWidget()
        right_layout.addWidget(self.stats_widget)
        
        # 로그 위젯
        self.log_widget = LogWidget()
        right_layout.addWidget(self.log_widget)
        
        # 스플리터에 패널 추가
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([800, 400])  # 기본 비율 설정
        
        # 메인 레이아웃에 추가
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(main_splitter)
        
        # 메뉴바 설정
        self.setup_menubar()
        
        # 상태바 설정
        self.setup_statusbar()
        
        # 스타일 적용
        self.setStyleSheet(StyleSheets.get_all_styles())
        
        # 초기 상태 설정
        self.export_widget.set_export_enabled(False)
    
    def setup_menubar(self):
        """메뉴바 설정"""
        menubar = self.menuBar()
        
        # 파일 메뉴
        file_menu = menubar.addMenu("파일")
        
        export_action = QAction("CSV 내보내기", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_csv)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("종료", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 도구 메뉴
        tools_menu = menubar.addMenu("도구")
        
        clear_logs_action = QAction("로그 지우기", self)
        clear_logs_action.triggered.connect(self.log_widget.clear_logs)
        tools_menu.addAction(clear_logs_action)
        
        db_stats_action = QAction("데이터베이스 통계", self)
        db_stats_action.triggered.connect(self.show_database_stats)
        tools_menu.addAction(db_stats_action)
        
        # 도움말 메뉴
        help_menu = menubar.addMenu("도움말")
        
        about_action = QAction("정보", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_statusbar(self):
        """상태바 설정"""
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("준비")
    
    def setup_connections(self):
        """시그널-슬롯 연결"""
        # API 키 위젯
        self.api_key_widget.api_key_changed.connect(self.on_api_key_changed)
        self.api_key_widget.api_key_deleted.connect(self.on_api_key_deleted)
        
        # 검색 위젯
        self.search_widget.search_requested.connect(self.start_search)
        
        # 내보내기 위젯
        self.export_widget.export_requested.connect(self.on_export_requested)
        
        # 비디오 테이블
        self.video_table.video_selected.connect(self.on_video_selected)
    
    def load_settings(self):
        """설정 로드"""
        try:
            # 윈도우 크기 설정
            width = self.config.get("app.window_width", 1200)
            height = self.config.get("app.window_height", 800)
            self.resize(width, height)
            
            # 저장된 API 키 로드
            api_key = self.config.get_api_key()
            if api_key:
                self.api_key_widget.set_api_key(api_key)
                self.youtube_client = YouTubeAPIClient(api_key)
                
                # API 키 유효성 검사
                if self.youtube_client.validate_api_key():
                    self.api_key_widget.set_status("success", "API 연결됨")
                    self.log_widget.add_log("저장된 API 키로 연결되었습니다.", "SUCCESS")
                else:
                    self.api_key_widget.set_status("error", "API 키 오류")
                    self.log_widget.add_log("저장된 API 키가 유효하지 않습니다.", "ERROR")
                    
        except Exception as e:
            logger.error(f"설정 로드 실패: {e}")
            self.log_widget.add_log(f"설정 로드 중 오류: {e}", "ERROR")
    
    def save_settings(self):
        """설정 저장"""
        try:
            # 윈도우 크기 저장
            self.config.set("app.window_width", self.width())
            self.config.set("app.window_height", self.height())
            
            logger.info("설정 저장 완료")
            
        except Exception as e:
            logger.error(f"설정 저장 실패: {e}")
    
    def on_api_key_changed(self, api_key: str):
        """API 키 변경 이벤트"""
        try:
            # API 키 저장
            if self.config.save_api_key(api_key):
                self.log_widget.add_log("API 키가 저장되었습니다.", "INFO")
                
                # YouTube 클라이언트 초기화
                self.youtube_client = YouTubeAPIClient(api_key)
                
                # API 키 유효성 검사
                if self.youtube_client.validate_api_key():
                    self.api_key_widget.set_status("success", "API 연결됨")
                    self.log_widget.add_log("API 키 검증이 완료되었습니다.", "SUCCESS")
                else:
                    self.api_key_widget.set_status("error", "API 키 오류")
                    self.log_widget.add_log("API 키가 유효하지 않습니다.", "ERROR")
                    self.youtube_client = None
            else:
                self.api_key_widget.set_status("error", "저장 실패")
                self.log_widget.add_log("API 키 저장에 실패했습니다.", "ERROR")
                
        except Exception as e:
            logger.error(f"API 키 처리 실패: {e}")
            self.api_key_widget.set_status("error", f"오류: {str(e)}")
            self.log_widget.add_log(f"API 키 처리 중 오류: {e}", "ERROR")
    
    def on_api_key_deleted(self):
        """API 키 삭제 이벤트"""
        try:
            # 저장된 API 키 삭제
            if self.config.delete_api_key():
                self.youtube_client = None
                self.log_widget.add_log("저장된 API 키가 삭제되었습니다.", "INFO")
            else:
                self.log_widget.add_log("API 키 삭제에 실패했습니다.", "ERROR")
                
        except Exception as e:
            logger.error(f"API 키 삭제 실패: {e}")
            self.log_widget.add_log(f"API 키 삭제 중 오류: {e}", "ERROR")
    
    def start_search(self, keyword: str):
        """검색 시작"""
        if not self.youtube_client:
            QMessageBox.warning(self, "경고", "먼저 유효한 API 키를 설정해주세요.")
            return
        
        if self.search_worker and self.search_worker.isRunning():
            QMessageBox.information(self, "알림", "이미 검색이 진행 중입니다.")
            return
        
        try:
            self.current_keyword = keyword
            self.log_widget.add_log(f"검색 시작: '{keyword}'", "INFO")
            
            # UI 상태 변경
            self.search_widget.set_search_enabled(False)
            self.search_widget.set_progress(0)
            self.statusbar.showMessage(f"검색 중: {keyword}")
            
            # 검색 워커 시작
            self.search_worker = SearchWorker(self.youtube_client, keyword)
            self.search_worker.progress_updated.connect(self.search_widget.set_progress)
            self.search_worker.log_message.connect(self.log_widget.add_log)
            self.search_worker.search_completed.connect(self.on_search_completed)
            self.search_worker.search_failed.connect(self.on_search_failed)
            self.search_worker.start()
            
        except Exception as e:
            logger.error(f"검색 시작 실패: {e}")
            self.log_widget.add_log(f"검색 시작 중 오류: {e}", "ERROR")
            self.search_widget.set_search_enabled(True)
            self.statusbar.showMessage("준비")
    
    def on_search_completed(self, videos: List[Video]):
        """검색 완료 이벤트"""
        try:
            self.current_videos = videos
            
            # 테이블 업데이트
            self.video_table.update_videos(videos)
            
            # 통계 업데이트
            self.stats_widget.update_stats(videos, self.current_keyword)
            
            # 데이터베이스에 저장
            saved_count = self.db_manager.save_videos_batch(videos)
            self.db_manager.add_search_history(self.current_keyword, len(videos))
            
            # UI 상태 복원
            self.search_widget.set_search_enabled(True)
            self.search_widget.set_progress(100)
            self.export_widget.set_export_enabled(len(videos) > 0)
            
            # 완료 메시지
            self.log_widget.add_log(f"검색 완료: {len(videos)}개 영상 발견", "SUCCESS")
            self.log_widget.add_log(f"데이터베이스 저장: {saved_count}개", "INFO")
            self.statusbar.showMessage(f"검색 완료: {len(videos)}개 결과")
            
        except Exception as e:
            logger.error(f"검색 완료 처리 실패: {e}")
            self.log_widget.add_log(f"검색 결과 처리 중 오류: {e}", "ERROR")
    
    def on_search_failed(self, error_message: str):
        """검색 실패 이벤트"""
        self.search_widget.set_search_enabled(True)
        self.search_widget.set_progress(0)
        self.statusbar.showMessage("검색 실패")
        
        QMessageBox.critical(self, "검색 실패", f"검색 중 오류가 발생했습니다:\\n{error_message}")
    
    def on_video_selected(self, video: Video):
        """영상 선택 이벤트"""
        self.log_widget.add_log(f"영상 선택: {video.title}", "INFO")
    
    def on_export_requested(self, export_type: str, include_stats: bool):
        """내보내기 요청 이벤트"""
        if not self.current_videos:
            QMessageBox.warning(self, "경고", "내보낼 데이터가 없습니다.")
            return
        
        try:
            if export_type == "csv":
                filename = self.exporter.export_videos(
                    self.current_videos,
                    keyword=self.current_keyword,
                    include_stats=include_stats
                )
                self.log_widget.add_log(f"CSV 내보내기 완료: {filename}", "SUCCESS")
                QMessageBox.information(self, "완료", f"CSV 파일이 저장되었습니다:\\n{filename}")
                
            elif export_type == "summary":
                search_criteria = {
                    "max_subscribers": 10000,
                    "min_duration_seconds": 1200,
                    "days_back": 30
                }
                filename = self.exporter.export_search_summary(
                    self.current_videos,
                    self.current_keyword,
                    search_criteria
                )
                self.log_widget.add_log(f"요약 내보내기 완료: {filename}", "SUCCESS")
                QMessageBox.information(self, "완료", f"요약 파일이 저장되었습니다:\\n{filename}")
                
        except Exception as e:
            logger.error(f"내보내기 실패: {e}")
            self.log_widget.add_log(f"내보내기 중 오류: {e}", "ERROR")
            QMessageBox.critical(self, "오류", f"내보내기 중 오류가 발생했습니다:\\n{e}")
    
    def export_csv(self):
        """메뉴에서 CSV 내보내기"""
        self.on_export_requested("csv", True)
    
    def show_database_stats(self):
        """데이터베이스 통계 표시"""
        try:
            stats = self.db_manager.get_database_stats()
            popular_keywords = self.db_manager.get_popular_keywords(5)
            
            stats_text = f"""
            총 영상 수: {stats['total_videos']:,}개
            총 검색 횟수: {stats['total_searches']:,}회
            고유 키워드 수: {stats['unique_keywords']:,}개
            
            인기 키워드:
            """
            
            for i, kw in enumerate(popular_keywords, 1):
                stats_text += f"{i}. {kw['keyword']} ({kw['count']}회)\\n"
            
            QMessageBox.information(self, "데이터베이스 통계", stats_text)
            
        except Exception as e:
            logger.error(f"데이터베이스 통계 조회 실패: {e}")
            QMessageBox.critical(self, "오류", f"통계 조회 중 오류가 발생했습니다:\\n{e}")
    
    def show_about(self):
        """정보 다이얼로그 표시"""
        about_text = """
        <h3>YouTube Keyword Analytics Tool v1.0</h3>
        <p>YouTube 키워드 기반 영상 분석 도구</p>
        
        <p><b>주요 기능:</b></p>
        <ul>
        <li>키워드 기반 YouTube 영상 검색</li>
        <li>구독자 10,000명 이하 채널 필터링</li>
        <li>20분 이상 영상 길이 필터링</li>
        <li>최근 1개월 업로드 영상 필터링</li>
        <li>조회수 순 정렬 및 표시</li>
        <li>CSV 파일 내보내기</li>
        <li>로컬 데이터베이스 자동 저장</li>
        </ul>
        
        <p><b>개발:</b> YouTube Analytics Team</p>
        <p><b>라이선스:</b> MIT License</p>
        """
        
        QMessageBox.about(self, "YouTube Keyword Analytics Tool", about_text)
    
    def closeEvent(self, event):
        """윈도우 종료 이벤트"""
        try:
            # 실행 중인 검색 중지
            if self.search_worker and self.search_worker.isRunning():
                self.search_worker.terminate()
                self.search_worker.wait(3000)  # 3초 대기
            
            # 설정 저장
            self.save_settings()
            
            logger.info("애플리케이션 종료")
            event.accept()
            
        except Exception as e:
            logger.error(f"종료 처리 실패: {e}")
            event.accept()  # 오류가 있어도 종료