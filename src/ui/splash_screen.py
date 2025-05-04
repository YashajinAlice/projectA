import os
from PyQt5.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer


class SplashScreen(QSplashScreen):
    def __init__(self):
        # 创建一个透明的QPixmap
        pixmap = QPixmap(600, 400)
        pixmap.fill(Qt.transparent)
        
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        # 创建内容小部件
        content = QWidget(self)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("ProjectA")
        title_label.setStyleSheet("""
            color: #3498db;
            font-size: 36px;
            font-weight: bold;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "../assets/logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        
        # 加载文本
        self.loading_label = QLabel("正在加载...")
        self.loading_label.setStyleSheet("""
            color: #7f8c8d;
            font-size: 14px;
        """)
        self.loading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loading_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #ecf0f1;
                border-radius: 5px;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # 版本信息
        version_label = QLabel("版本 1.0.0")
        version_label.setStyleSheet("""
            color: #7f8c8d;
            font-size: 12px;
        """)
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # 设置内容小部件的位置
        content.setGeometry(0, 0, 600, 400)
        
        # 启动进度条动画
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)
        
        # 更新加载文本
        self.loading_texts = ["正在加载资源...", "正在初始化...", "正在检查更新...", "准备就绪..."]
        self.text_timer = QTimer(self)
        self.text_timer.timeout.connect(self.update_loading_text)
        self.text_timer.start(500)
        self.text_index = 0
    
    def update_progress(self):
        """更新进度条"""
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()
    
    def update_loading_text(self):
        """更新加载文本"""
        self.loading_label.setText(self.loading_texts[self.text_index % len(self.loading_texts)])
        self.text_index += 1
    
    def drawContents(self, painter):
        """绘制内容"""
        # 绘制圆角矩形背景
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(30, 30, 46, 230))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)
