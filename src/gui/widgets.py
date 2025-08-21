"""커스텀 위젯 모듈"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QProgressBar, QGroupBox, QTextEdit,
    QHeaderView, QAbstractItemView, QFrame, QSplitter, QCheckBox, QComboBox
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QFont, QDesktopServices, QPixmap, QIcon
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from ..database.models import Video
from ..utils.helpers import FormatHelper
from .styles import DarkTheme, Typography

logger = logging.getLogger(__name__)


class StatusIndicator(QLabel):
    """상태 표시 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusLabel")
        self.set_status("idle", "준비")
    
    def set_status(self, status_type: str, message: str):
        """상태 설정
        
        Args:
            status_type: 상태 타입 (success, error, warning, info, idle)
            message: 상태 메시지
        """
        self.setText(f"● {message}")
        
        status_classes = {
            'success': 'successStatus',
            'error': 'errorStatus',
            'warning': 'warningStatus',
            'info': 'infoStatus',
            'idle': 'statusLabel'
        }
        
        # 기존 클래스 제거
        for class_name in status_classes.values():
            self.setProperty("class", "")
        
        # 새 클래스 적용
        self.setObjectName(status_classes.get(status_type, 'statusLabel'))
        self.style().polish(self)


class APIKeyWidget(QGroupBox):
    """API 키 입력 위젯"""
    
    api_key_changed = Signal(str)
    api_key_deleted = Signal()
    
    def __init__(self, parent=None):
        super().__init__("YouTube API 설정", parent)
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        layout = QVBoxLayout(self)
        
        # API 키 입력 영역
        input_layout = QHBoxLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("YouTube Data API v3 키를 입력하세요")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.textChanged.connect(self.on_text_changed)
        
        self.save_button = QPushButton("저장")
        self.save_button.clicked.connect(self.save_api_key)
        self.save_button.setEnabled(False)
        
        self.show_button = QPushButton("표시")
        self.show_button.setObjectName("secondaryButton")
        self.show_button.clicked.connect(self.toggle_visibility)
        
        self.clear_button = QPushButton("삭제")
        self.clear_button.setObjectName("dangerButton")
        self.clear_button.clicked.connect(self.clear_api_key)
        
        input_layout.addWidget(self.api_key_input)
        input_layout.addWidget(self.save_button)
        input_layout.addWidget(self.show_button)
        input_layout.addWidget(self.clear_button)
        
        # 상태 표시
        self.status_indicator = StatusIndicator()
        
        # 도움말
        help_label = QLabel(
            "API 키 발급: Google Cloud Console > API 및 서비스 > YouTube Data API v3"
        )
        help_label.setObjectName("captionLabel")
        help_label.setWordWrap(True)
        
        layout.addLayout(input_layout)
        layout.addWidget(self.status_indicator)
        layout.addWidget(help_label)
    
    def save_api_key(self):
        """API 키 저장"""
        api_key = self.api_key_input.text().strip()
        if api_key:
            self.api_key_changed.emit(api_key)
            self.save_button.setEnabled(False)
    
    def toggle_visibility(self):
        """API 키 표시/숨김 토글"""
        if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_button.setText("숨김")
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_button.setText("표시")
    
    def clear_api_key(self):
        """API 키 삭제"""
        self.api_key_input.clear()
        self.api_key_deleted.emit()
        self.set_status("idle", "API 키가 삭제되었습니다")
        
    def on_text_changed(self):
        """텍스트 변경시 저장 버튼 활성화"""
        has_text = bool(self.api_key_input.text().strip())
        self.save_button.setEnabled(has_text)
        if has_text:
            self.set_status("idle", "새 API 키 입력됨")
    
    def set_api_key(self, api_key: str):
        """API 키 설정"""
        self.api_key_input.setText(api_key)
        self.save_button.setEnabled(False)
    
    def set_status(self, status_type: str, message: str):
        """상태 설정"""
        self.status_indicator.set_status(status_type, message)


class SearchWidget(QGroupBox):
    """검색 위젯"""
    
    search_requested = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__("검색 설정", parent)
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        layout = QVBoxLayout(self)
        
        # 키워드 입력 영역
        input_layout = QHBoxLayout()
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("검색할 키워드를 입력하세요 (예: 파이썬 강의)")
        self.keyword_input.returnPressed.connect(self.start_search)
        
        self.search_button = QPushButton("🔍 검색 시작")
        self.search_button.clicked.connect(self.start_search)
        
        input_layout.addWidget(self.keyword_input)
        input_layout.addWidget(self.search_button)
        
        # 검색 조건 표시
        self.criteria_label = QLabel("조건: 조회수↓ | 구독자≤10K | 20분+ | 최근 1개월")
        self.criteria_label.setObjectName("captionLabel")
        
        # 진행률 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        layout.addLayout(input_layout)
        layout.addWidget(self.criteria_label)
        layout.addWidget(self.progress_bar)
    
    def start_search(self):
        """검색 시작"""
        keyword = self.keyword_input.text().strip()
        if keyword:
            self.search_requested.emit(keyword)
    
    def set_progress(self, value: int):
        """진행률 설정"""
        self.progress_bar.setValue(value)
        
        if value > 0 and not self.progress_bar.isVisible():
            self.progress_bar.setVisible(True)
        elif value >= 100:
            self.progress_bar.setVisible(False)
    
    def set_search_enabled(self, enabled: bool):
        """검색 버튼 활성화/비활성화"""
        self.search_button.setEnabled(enabled)
        self.keyword_input.setEnabled(enabled)
        
        if enabled:
            self.search_button.setText("🔍 검색 시작")
        else:
            self.search_button.setText("검색 중...")


class VideoTableWidget(QTableWidget):
    """영상 결과 테이블 위젯"""
    
    video_selected = Signal(Video)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.videos = []
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        # 컬럼 설정
        columns = ["순위", "제목", "채널명", "구독자", "조회수", "길이", "업로드", "URL"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        
        # 테이블 설정
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        
        # 컬럼 크기 조정
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # 순위
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # 제목
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # 채널명
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # 구독자
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # 조회수
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # 길이
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # 업로드
        
        self.setColumnWidth(0, 50)  # 순위 컬럼 고정 너비
        
        # 이벤트 연결
        self.cellClicked.connect(self.on_cell_clicked)
        self.cellDoubleClicked.connect(self.on_cell_double_clicked)
    
    def update_videos(self, videos: List[Video]):
        """영상 데이터 업데이트"""
        self.videos = videos
        self.setRowCount(len(videos))
        
        for row, video in enumerate(videos):
            self.set_video_row(row, video, row + 1)
        
        # 첫 번째 컬럼(순위)로 정렬
        self.sortItems(0, Qt.SortOrder.AscendingOrder)
    
    def set_video_row(self, row: int, video: Video, rank: int):
        """행에 영상 데이터 설정"""
        items = [
            QTableWidgetItem(str(rank)),
            QTableWidgetItem(video.title[:50] + "..." if len(video.title) > 50 else video.title),
            QTableWidgetItem(video.channel_name),
            QTableWidgetItem(FormatHelper.format_number(video.subscriber_count)),
            QTableWidgetItem(FormatHelper.format_number(video.view_count)),
            QTableWidgetItem(video.duration_formatted),
            QTableWidgetItem(FormatHelper.format_date(video.upload_date, relative=False) if video.upload_date else ""),
            QTableWidgetItem("링크")
        ]
        
        # 숫자 정렬을 위한 데이터 설정
        items[0].setData(Qt.ItemDataRole.UserRole, rank)
        items[3].setData(Qt.ItemDataRole.UserRole, video.subscriber_count)
        items[4].setData(Qt.ItemDataRole.UserRole, video.view_count)
        items[5].setData(Qt.ItemDataRole.UserRole, video.duration_seconds)
        if video.upload_date:
            items[6].setData(Qt.ItemDataRole.UserRole, video.upload_date.timestamp())
        
        # URL 아이템 스타일 설정
        url_item = items[7]
        url_item.setForeground(DarkTheme.SECONDARY)
        
        # 아이템을 테이블에 추가
        for col, item in enumerate(items):
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 편집 불가
            self.setItem(row, col, item)
    
    def on_cell_clicked(self, row: int, column: int):
        """셀 클릭 이벤트"""
        if 0 <= row < len(self.videos):
            video = self.videos[row]
            
            # URL 컬럼 클릭 시 링크 열기
            if column == 7:  # URL 컬럼
                QDesktopServices.openUrl(video.video_url)
            
            self.video_selected.emit(video)
    
    def on_cell_double_clicked(self, row: int, column: int):
        """셀 더블클릭 이벤트"""
        if 0 <= row < len(self.videos):
            video = self.videos[row]
            # 영상 링크 열기
            QDesktopServices.openUrl(video.video_url)
    
    def get_selected_video(self) -> Optional[Video]:
        """선택된 영상 반환"""
        current_row = self.currentRow()
        if 0 <= current_row < len(self.videos):
            return self.videos[current_row]
        return None


class ExportWidget(QGroupBox):
    """데이터 내보내기 위젯"""
    
    export_requested = Signal(str, bool)  # filename, include_stats
    
    def __init__(self, parent=None):
        super().__init__("데이터 내보내기", parent)
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        layout = QVBoxLayout(self)
        
        # 옵션 영역
        options_layout = QHBoxLayout()
        
        self.include_stats_checkbox = QCheckBox("상세 통계 포함")
        self.include_stats_checkbox.setChecked(True)
        
        options_layout.addWidget(self.include_stats_checkbox)
        options_layout.addStretch()
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        self.export_csv_button = QPushButton("📊 CSV 내보내기")
        self.export_csv_button.clicked.connect(self.export_csv)
        
        self.export_summary_button = QPushButton("📋 요약 내보내기")
        self.export_summary_button.setObjectName("secondaryButton")
        self.export_summary_button.clicked.connect(self.export_summary)
        
        button_layout.addWidget(self.export_csv_button)
        button_layout.addWidget(self.export_summary_button)
        button_layout.addStretch()
        
        layout.addLayout(options_layout)
        layout.addLayout(button_layout)
    
    def export_csv(self):
        """CSV 내보내기"""
        include_stats = self.include_stats_checkbox.isChecked()
        self.export_requested.emit("csv", include_stats)
    
    def export_summary(self):
        """요약 내보내기"""
        self.export_requested.emit("summary", False)
    
    def set_export_enabled(self, enabled: bool):
        """내보내기 버튼 활성화/비활성화"""
        self.export_csv_button.setEnabled(enabled)
        self.export_summary_button.setEnabled(enabled)


class StatsWidget(QGroupBox):
    """통계 정보 위젯"""
    
    def __init__(self, parent=None):
        super().__init__("검색 통계", parent)
        self.setup_ui()
    
    def setup_ui(self):
        """UI 설정"""
        layout = QVBoxLayout(self)
        
        self.stats_label = QLabel("검색 결과가 없습니다.")
        self.stats_label.setObjectName("captionLabel")
        self.stats_label.setWordWrap(True)
        
        layout.addWidget(self.stats_label)
    
    def update_stats(self, videos: List[Video], keyword: str):
        """통계 정보 업데이트"""
        if not videos:
            self.stats_label.setText("검색 결과가 없습니다.")
            return
        
        total_videos = len(videos)
        total_views = sum(v.view_count for v in videos)
        avg_views = total_views // total_videos if total_videos > 0 else 0
        avg_subscribers = sum(v.subscriber_count for v in videos) // total_videos if total_videos > 0 else 0
        avg_duration = sum(v.duration_seconds for v in videos) // total_videos if total_videos > 0 else 0
        
        # 최고 조회수 영상
        top_video = max(videos, key=lambda x: x.view_count) if videos else None
        
        stats_text = f"""
        <b>키워드:</b> {keyword}<br>
        <b>결과 수:</b> {total_videos}개<br>
        <b>평균 조회수:</b> {FormatHelper.format_number(avg_views)}<br>
        <b>평균 구독자:</b> {FormatHelper.format_number(avg_subscribers)}<br>
        <b>평균 길이:</b> {FormatHelper.format_duration(avg_duration)}<br>
        """
        
        if top_video:
            stats_text += f"<b>최고 조회수:</b> {FormatHelper.format_number(top_video.view_count)} ({top_video.channel_name})"
        
        self.stats_label.setText(stats_text)


class LogWidget(QTextEdit):
    """로그 표시 위젯"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumHeight(150)
        self.setReadOnly(True)
        self.setPlaceholderText("작업 로그가 여기에 표시됩니다...")
    
    def add_log(self, message: str, level: str = "INFO"):
        """로그 메시지 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 로그 레벨에 따른 색상 설정
        colors = {
            "DEBUG": DarkTheme.TEXT_SECONDARY,
            "INFO": DarkTheme.TEXT_PRIMARY,
            "WARNING": DarkTheme.WARNING,
            "ERROR": DarkTheme.ERROR,
            "SUCCESS": DarkTheme.SUCCESS
        }
        
        color = colors.get(level, DarkTheme.TEXT_PRIMARY)
        log_entry = f'<span style="color: {color};">[{timestamp}] {level}: {message}</span><br>'
        
        self.insertHtml(log_entry)
        
        # 자동 스크롤
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_logs(self):
        """로그 지우기"""
        self.clear()