"""GUI 스타일 및 테마 정의"""


class DarkTheme:
    """다크 테마 색상 정의"""
    
    # 기본 배경색
    BACKGROUND_PRIMARY = "#2b2b2b"      # 메인 배경
    BACKGROUND_SECONDARY = "#3c3c3c"    # 카드, 패널 배경
    BACKGROUND_TERTIARY = "#404040"     # 입력 필드 배경
    BACKGROUND_HOVER = "#484848"        # 호버 상태 배경
    
    # 텍스트 색상
    TEXT_PRIMARY = "#ffffff"            # 주요 텍스트
    TEXT_SECONDARY = "#b3b3b3"          # 보조 텍스트
    TEXT_DISABLED = "#666666"           # 비활성 텍스트
    TEXT_PLACEHOLDER = "#888888"        # 플레이스홀더 텍스트
    
    # 브랜드 색상
    PRIMARY = "#bb86fc"                 # 주요 액션 버튼
    PRIMARY_HOVER = "#985eff"           # 호버 상태
    PRIMARY_PRESSED = "#7c4dff"         # 눌린 상태
    PRIMARY_LIGHT = "#d1c4e9"           # 밝은 톤
    
    # 보조 색상
    SECONDARY = "#03dac6"               # 보조 버튼, 링크
    SECONDARY_HOVER = "#00bfa5"         # 보조 색상 호버
    
    # 상태 색상
    SUCCESS = "#4caf50"                 # 성공 메시지
    WARNING = "#ff9800"                 # 경고 메시지
    ERROR = "#f44336"                   # 오류 메시지
    INFO = "#2196f3"                    # 정보 메시지
    
    # 경계선 및 구분선
    BORDER = "#555555"                  # 기본 경계선
    BORDER_LIGHT = "#666666"            # 밝은 경계선
    BORDER_FOCUS = "#bb86fc"            # 포커스 경계선
    DIVIDER = "#484848"                 # 구분선
    
    # 선택 및 강조 색상
    SELECTION = "#bb86fc33"             # 선택 영역 배경
    HIGHLIGHT = "#bb86fc66"             # 강조 배경


class Typography:
    """폰트 설정"""
    
    FONT_FAMILY = "Segoe UI, Malgun Gothic, Arial, sans-serif"
    
    # 폰트 크기
    FONT_SIZE_TITLE = 18        # 창 제목
    FONT_SIZE_SUBTITLE = 16     # 섹션 제목
    FONT_SIZE_BODY = 12         # 본문 텍스트
    FONT_SIZE_CAPTION = 10      # 캡션, 도움말
    FONT_SIZE_BUTTON = 11       # 버튼 텍스트
    FONT_SIZE_TABLE = 11        # 테이블 텍스트
    
    # 폰트 두께
    FONT_WEIGHT_NORMAL = "normal"
    FONT_WEIGHT_BOLD = "bold"
    
    # 줄 간격
    LINE_HEIGHT_NORMAL = 1.4
    LINE_HEIGHT_COMPACT = 1.2


class StyleSheets:
    """QSS 스타일시트 정의"""
    
    @staticmethod
    def get_main_window_style() -> str:
        """메인 윈도우 스타일"""
        return f"""
        QMainWindow {{
            background-color: {DarkTheme.BACKGROUND_PRIMARY};
            color: {DarkTheme.TEXT_PRIMARY};
            font-family: {Typography.FONT_FAMILY};
            font-size: {Typography.FONT_SIZE_BODY}px;
        }}
        
        QWidget {{
            background-color: {DarkTheme.BACKGROUND_PRIMARY};
            color: {DarkTheme.TEXT_PRIMARY};
            font-family: {Typography.FONT_FAMILY};
        }}
        """
    
    @staticmethod
    def get_button_style() -> str:
        """버튼 스타일"""
        return f"""
        QPushButton {{
            background-color: {DarkTheme.PRIMARY};
            color: {DarkTheme.TEXT_PRIMARY};
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            font-size: {Typography.FONT_SIZE_BUTTON}px;
            min-height: 20px;
            min-width: 80px;
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
        
        QPushButton#secondaryButton {{
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
            color: {DarkTheme.TEXT_PRIMARY};
            border: 1px solid {DarkTheme.BORDER};
        }}
        
        QPushButton#secondaryButton:hover {{
            background-color: {DarkTheme.BACKGROUND_HOVER};
            border-color: {DarkTheme.BORDER_LIGHT};
        }}
        
        QPushButton#dangerButton {{
            background-color: {DarkTheme.ERROR};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        QPushButton#dangerButton:hover {{
            background-color: #d32f2f;
        }}
        """
    
    @staticmethod
    def get_input_style() -> str:
        """입력 필드 스타일"""
        return f"""
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
            border-color: {DarkTheme.BORDER_FOCUS};
        }}
        
        QLineEdit:disabled {{
            background-color: {DarkTheme.TEXT_DISABLED};
            color: {DarkTheme.TEXT_DISABLED};
        }}
        
        QLineEdit::placeholder {{
            color: {DarkTheme.TEXT_PLACEHOLDER};
        }}
        
        QTextEdit {{
            background-color: {DarkTheme.BACKGROUND_TERTIARY};
            border: 2px solid {DarkTheme.BORDER};
            border-radius: 4px;
            padding: 8px;
            color: {DarkTheme.TEXT_PRIMARY};
            font-size: {Typography.FONT_SIZE_BODY}px;
        }}
        
        QTextEdit:focus {{
            border-color: {DarkTheme.BORDER_FOCUS};
        }}
        """
    
    @staticmethod
    def get_table_style() -> str:
        """테이블 스타일"""
        return f"""
        QTableWidget {{
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
            color: {DarkTheme.TEXT_PRIMARY};
            border: 1px solid {DarkTheme.BORDER};
            border-radius: 4px;
            gridline-color: {DarkTheme.BORDER};
            font-size: {Typography.FONT_SIZE_TABLE}px;
            selection-background-color: {DarkTheme.SELECTION};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {DarkTheme.DIVIDER};
        }}
        
        QTableWidget::item:selected {{
            background-color: {DarkTheme.SELECTION};
            color: {DarkTheme.TEXT_PRIMARY};
        }}
        
        QTableWidget::item:hover {{
            background-color: {DarkTheme.BACKGROUND_HOVER};
        }}
        
        QHeaderView::section {{
            background-color: {DarkTheme.BACKGROUND_PRIMARY};
            color: {DarkTheme.TEXT_PRIMARY};
            padding: 8px;
            border: none;
            border-bottom: 2px solid {DarkTheme.PRIMARY};
            font-weight: bold;
            font-size: {Typography.FONT_SIZE_BODY}px;
        }}
        
        QHeaderView::section:hover {{
            background-color: {DarkTheme.BACKGROUND_HOVER};
        }}
        
        QScrollBar:vertical {{
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {DarkTheme.BORDER_LIGHT};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {DarkTheme.PRIMARY};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        """
    
    @staticmethod
    def get_progress_bar_style() -> str:
        """진행률 바 스타일"""
        return f"""
        QProgressBar {{
            background-color: {DarkTheme.BACKGROUND_TERTIARY};
            border: 1px solid {DarkTheme.BORDER};
            border-radius: 4px;
            text-align: center;
            color: {DarkTheme.TEXT_PRIMARY};
            font-size: {Typography.FONT_SIZE_BODY}px;
            min-height: 20px;
        }}
        
        QProgressBar::chunk {{
            background-color: {DarkTheme.PRIMARY};
            border-radius: 3px;
        }}
        """
    
    @staticmethod
    def get_label_style() -> str:
        """라벨 스타일"""
        return f"""
        QLabel {{
            color: {DarkTheme.TEXT_PRIMARY};
            font-size: {Typography.FONT_SIZE_BODY}px;
        }}
        
        QLabel#titleLabel {{
            font-size: {Typography.FONT_SIZE_TITLE}px;
            font-weight: bold;
            color: {DarkTheme.PRIMARY};
            padding: 10px 0;
        }}
        
        QLabel#subtitleLabel {{
            font-size: {Typography.FONT_SIZE_SUBTITLE}px;
            font-weight: bold;
            color: {DarkTheme.TEXT_PRIMARY};
            padding: 8px 0;
        }}
        
        QLabel#captionLabel {{
            font-size: {Typography.FONT_SIZE_CAPTION}px;
            color: {DarkTheme.TEXT_SECONDARY};
        }}
        
        QLabel#statusLabel {{
            font-size: {Typography.FONT_SIZE_CAPTION}px;
            padding: 4px 8px;
            border-radius: 3px;
        }}
        
        QLabel#successStatus {{
            background-color: {DarkTheme.SUCCESS};
            color: white;
        }}
        
        QLabel#errorStatus {{
            background-color: {DarkTheme.ERROR};
            color: white;
        }}
        
        QLabel#warningStatus {{
            background-color: {DarkTheme.WARNING};
            color: white;
        }}
        
        QLabel#infoStatus {{
            background-color: {DarkTheme.INFO};
            color: white;
        }}
        """
    
    @staticmethod
    def get_group_box_style() -> str:
        """그룹 박스 스타일"""
        return f"""
        QGroupBox {{
            color: {DarkTheme.TEXT_PRIMARY};
            border: 2px solid {DarkTheme.BORDER};
            border-radius: 6px;
            margin-top: 1ex;
            font-weight: bold;
            font-size: {Typography.FONT_SIZE_BODY}px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            background-color: {DarkTheme.BACKGROUND_PRIMARY};
            color: {DarkTheme.PRIMARY};
        }}
        """
    
    @staticmethod
    def get_combo_box_style() -> str:
        """콤보박스 스타일"""
        return f"""
        QComboBox {{
            background-color: {DarkTheme.BACKGROUND_TERTIARY};
            border: 2px solid {DarkTheme.BORDER};
            border-radius: 4px;
            padding: 6px 12px;
            color: {DarkTheme.TEXT_PRIMARY};
            font-size: {Typography.FONT_SIZE_BODY}px;
            min-height: 20px;
        }}
        
        QComboBox:focus {{
            border-color: {DarkTheme.BORDER_FOCUS};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {DarkTheme.TEXT_SECONDARY};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {DarkTheme.BACKGROUND_SECONDARY};
            border: 1px solid {DarkTheme.BORDER};
            color: {DarkTheme.TEXT_PRIMARY};
            selection-background-color: {DarkTheme.SELECTION};
        }}
        """
    
    @staticmethod
    def get_checkbox_style() -> str:
        """체크박스 스타일"""
        return f"""
        QCheckBox {{
            color: {DarkTheme.TEXT_PRIMARY};
            font-size: {Typography.FONT_SIZE_BODY}px;
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 2px solid {DarkTheme.BORDER};
            border-radius: 3px;
            background-color: {DarkTheme.BACKGROUND_TERTIARY};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {DarkTheme.PRIMARY};
            border-color: {DarkTheme.PRIMARY};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {DarkTheme.BORDER_LIGHT};
        }}
        """
    
    @staticmethod
    def get_splitter_style() -> str:
        """스플리터 스타일"""
        return f"""
        QSplitter::handle {{
            background-color: {DarkTheme.BORDER};
        }}
        
        QSplitter::handle:horizontal {{
            width: 3px;
        }}
        
        QSplitter::handle:vertical {{
            height: 3px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {DarkTheme.PRIMARY};
        }}
        """
    
    @staticmethod
    def get_all_styles() -> str:
        """모든 스타일 통합"""
        return (
            StyleSheets.get_main_window_style() +
            StyleSheets.get_button_style() +
            StyleSheets.get_input_style() +
            StyleSheets.get_table_style() +
            StyleSheets.get_progress_bar_style() +
            StyleSheets.get_label_style() +
            StyleSheets.get_group_box_style() +
            StyleSheets.get_combo_box_style() +
            StyleSheets.get_checkbox_style() +
            StyleSheets.get_splitter_style()
        )