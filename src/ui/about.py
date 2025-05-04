import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                            QDialog, QTextBrowser, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ui.update_checker import check_for_updates


class AnnouncementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("公告")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        # 公告内容
        self.announcement_browser = QTextBrowser()
        self.announcement_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #f5f5f5;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.announcement_browser)
        
        # 加载公告
        self.load_announcement()
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_announcement(self):
        """加载公告内容"""
        announcement_path = os.path.join(os.path.dirname(__file__), "../assets/announcements.md")
        try:
            if os.path.exists(announcement_path):
                with open(announcement_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.announcement_browser.setMarkdown(content)
            else:
                self.announcement_browser.setPlainText("暂无公告")
        except Exception as e:
            self.announcement_browser.setPlainText(f"加载公告时出错: {e}")


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.version = "1.0.3"
        self.update_date = "2025-05-04"
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("关于")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title_label)
        
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
        layout.addWidget(logo_label)
        
        # 关于信息
        info_layout = QVBoxLayout()
        
        about_text = QLabel(f"作者: FuLin\n版本: {self.version}\n更新日期: {self.update_date}")
        about_text.setAlignment(Qt.AlignCenter)
        about_text.setStyleSheet("font-size: 18px; color: #7f8c8d; margin: 20px 0;")
        info_layout.addWidget(about_text)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        check_update_button = QPushButton("检查更新")
        check_update_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        check_update_button.clicked.connect(self.check_update)
        button_layout.addWidget(check_update_button)
        
        show_announcement_button = QPushButton("查看公告")
        show_announcement_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        show_announcement_button.clicked.connect(self.show_announcement)
        button_layout.addWidget(show_announcement_button)
        
        info_layout.addLayout(button_layout)
        layout.addLayout(info_layout)
        
        # 版权信息
        copyright_label = QLabel("© 2025 FuLin. 保留所有权利。")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-top: 20px;")
        layout.addWidget(copyright_label)
        
        self.setLayout(layout)
    
    def check_update(self):
        """检查更新"""
        try:
            has_update, version, announcement = check_for_updates()
            if has_update:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "更新可用", f"发现新版本: {version}\n\n{announcement}")
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "检查更新", "当前已是最新版本")
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "检查更新失败", f"无法检查更新: {str(e)}")
    
    def show_announcement(self):
        """显示公告"""
        dialog = AnnouncementDialog(self)
        dialog.exec_()
