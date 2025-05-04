import os
import platform
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QDateTime


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.version = "1.0.3"
        self.running_apps = []
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部区域 - Logo和标题
        top_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/logo.png"))
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        else:
            print(f"无法加载图片：{logo_path}")
            logo_label.setText("Logo")
            logo_label.setStyleSheet("font-size: 24px; color: #3498db;")
        
        logo_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(logo_label)
        
        # 标题和版本信息
        title_info = QVBoxLayout()
        
        title_label = QLabel("ProjectA")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #3498db;")
        title_info.addWidget(title_label)
        
        version_label = QLabel(f"版本: {self.version}")
        version_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        title_info.addWidget(version_label)
        
        # 系统信息
        system_info = QLabel(f"操作系统: {platform.system()} {platform.version()}")
        system_info.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        title_info.addWidget(system_info)
        
        title_info.setAlignment(Qt.AlignLeft)
        top_layout.addLayout(title_info)
        
        main_layout.addLayout(top_layout)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #3498db;")
        main_layout.addWidget(separator)
        
        # 中间区域 - 运行信息和公告
        middle_layout = QVBoxLayout()
        
        # 运行信息
        self.run_info_label = QLabel("目前无应用程序运行")
        self.run_info_label.setAlignment(Qt.AlignCenter)
        self.run_info_label.setStyleSheet("font-size: 18px; color: #7f8c8d; margin: 20px 0;")
        middle_layout.addWidget(self.run_info_label)
        
        # 公告
        announcement_title = QLabel("公告")
        announcement_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        middle_layout.addWidget(announcement_title)
        
        self.announcement_label = QLabel("欢迎使用 ProjectA！")
        self.announcement_label.setWordWrap(True)
        self.announcement_label.setStyleSheet("""
            font-size: 16px; 
            color: #7f8c8d; 
            background-color: #f5f5f5; 
            padding: 15px; 
            border-radius: 5px;
        """)
        middle_layout.addWidget(self.announcement_label)
        
        # 加载公告
        self.load_announcement()
        
        main_layout.addLayout(middle_layout)
        
        # 底部区域 - 时间
        bottom_layout = QVBoxLayout()
        
        self.time_label = QLabel("")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 18px; color: #3498db; margin-top: 20px;")
        bottom_layout.addWidget(self.time_label)
        
        main_layout.addLayout(bottom_layout)
        
        # 更新时间
        self.update_time()
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        
        self.setLayout(main_layout)
    
    def update_time(self):
        """更新当前时间"""
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.time_label.setText(f"当前时间: {current_time}")
    
    def update_running_app(self, app_name, is_running=True):
        """更新运行中的应用信息"""
        if is_running:
            if app_name not in self.running_apps:
                self.running_apps.append(app_name)
        else:
            if app_name in self.running_apps:
                self.running_apps.remove(app_name)
        
        if self.running_apps:
            self.run_info_label.setText(f"正在运行: {', '.join(self.running_apps)}")
        else:
            self.run_info_label.setText("目前无应用程序运行")
    
    def load_announcement(self):
        """加载公告内容"""
        announcement_path = os.path.join(os.path.dirname(__file__), "../assets/announcements.md")
        try:
            if os.path.exists(announcement_path):
                with open(announcement_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # 简单处理Markdown格式
                    content = content.replace('# ', '<b>').replace('\n## ', '</b><br><b>')
                    content = content.replace('\n- ', '<br>• ')
                    content = content.replace('\n\n', '<br><br>')
                    self.announcement_label.setText(content)
        except Exception as e:
            print(f"加载公告时出错: {e}")
    
    def update_announcement(self, text):
        """更新公告内容"""
        self.announcement_label.setText(text)
