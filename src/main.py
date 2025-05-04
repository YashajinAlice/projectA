import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QListWidget, 
                           QStackedWidget, QWidget, QLabel, QVBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QSize
import requests
import json
from ui.home import HomePage
from ui.todo import TodoPage
from ui.bug_tracker import BugTrackerPage
from ui.app_launcher import AppLauncherPage
from ui.game_launcher import GameLauncherPage
from ui.about import AboutPage
from ui.settings import SettingsPage
from ui.update_checker import check_for_updates
from ui.splash_screen import SplashScreen
from ui.utils import load_stylesheet, get_settings


class SidebarItem(QWidget):
    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 图标
        self.icon_label = QLabel()
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(pixmap)
        else:
            self.icon_label.setText("•")
        
        self.icon_label.setFixedSize(30, 30)
        layout.addWidget(self.icon_label)
        
        # 文本
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.text_label)
        
        # 默认未选中状态
        self.setSelected(False)
    
    def setSelected(self, selected):
        """设置选中状态"""
        if selected:
            self.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 5px;
            """)
        else:
            self.setStyleSheet("""
                background-color: transparent;
                border-radius: 5px;
            """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 加载设置
        self.settings = get_settings()
        
        # 设置窗口属性
        self.setWindowTitle("ProjectA")
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置应用图标
        icon_path = os.path.join(os.path.dirname(__file__), "assets/logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"警告: 图标文件不存在: {icon_path}")
        
        # 创建必要的目录
        self.create_directories()
        
        # 应用样式表
        theme = self.settings.get("theme", "dark")
        self.apply_stylesheet(theme)
        
        # 主布局
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 左侧导航栏
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            background-color: #1e1e2e;
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        # 应用标题
        app_title = QLabel("ProjectA")
        app_title.setStyleSheet("color: white; font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        app_title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(app_title)
        
        # 导航项目
        self.nav_items = []
        
        # 创建导航项
        nav_data = [
            {"icon": "assets/icons/home.png", "text": "首页"},
            {"icon": "assets/icons/todo.png", "text": "待办事项"},
            {"icon": "assets/icons/bug.png", "text": "BUG待修正"},
            {"icon": "assets/icons/app.png", "text": "应用启动"},
            {"icon": "assets/icons/game.png", "text": "游戏启动"},
            {"icon": "assets/icons/about.png", "text": "关于"},
            {"icon": "assets/icons/settings.png", "text": "设置"}
        ]
        
        for i, item_data in enumerate(nav_data):
            icon_path = os.path.join(os.path.dirname(__file__), item_data["icon"])
            item = SidebarItem(icon_path, item_data["text"])
            item.mousePressEvent = lambda event, idx=i: self.display_page(idx)
            sidebar_layout.addWidget(item)
            self.nav_items.append(item)
        
        # 添加弹性空间
        sidebar_layout.addStretch()
        
        # 版本信息
        version_label = QLabel("版本 v1.4.0")
        version_label.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 12px;")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        main_layout.addWidget(self.sidebar)
        
        # 右侧内容区域
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 内容区域
        self.pages = QStackedWidget()
        self.home_page = HomePage()
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(TodoPage())
        self.pages.addWidget(BugTrackerPage())
        self.pages.addWidget(AppLauncherPage(self.home_page))
        self.pages.addWidget(GameLauncherPage(self.home_page))
        self.pages.addWidget(AboutPage())
        
        # 设置页面需要传入主窗口引用以便应用主题
        self.settings_page = SettingsPage(self)
        self.pages.addWidget(self.settings_page)
        
        content_layout.addWidget(self.pages)
        main_layout.addWidget(content_container)
        
        self.setCentralWidget(central_widget)
        
        # 设置初始选中项
        self.display_page(0)
        
        # 检查更新
        QTimer.singleShot(1000, self.check_updates)
    
    def create_directories(self):
        """创建必要的目录结构"""
        directories = [
            "src/data",
            "src/assets",
            "src/assets/icons",
            "src/assets/backgrounds",
            "src/logs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def display_page(self, index):
        """切换页面"""
        # 更新导航项选中状态
        for i, item in enumerate(self.nav_items):
            item.setSelected(i == index)
        
        # 切换页面前先创建动画
        self.page_transition(index)
    
    def page_transition(self, index):
        """页面切换动画"""
        # 获取当前页面和目标页面
        current_widget = self.pages.currentWidget()
        target_widget = self.pages.widget(index)
        
        if current_widget == target_widget:
            return
        
        # 设置目标页面为可见
        target_widget.setVisible(True)
        
        # 创建动画
        current_opacity_anim = QPropertyAnimation(current_widget, b"windowOpacity")
        current_opacity_anim.setDuration(300)
        current_opacity_anim.setStartValue(1.0)
        current_opacity_anim.setEndValue(0.0)
        current_opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        target_opacity_anim = QPropertyAnimation(target_widget, b"windowOpacity")
        target_opacity_anim.setDuration(300)
        target_opacity_anim.setStartValue(0.0)
        target_opacity_anim.setEndValue(1.0)
        target_opacity_anim.setEasingCurve(QEasingCurve.InCubic)
        
        # 开始动画
        current_opacity_anim.start()
        target_opacity_anim.start()
        
        # 切换页面
        self.pages.setCurrentIndex(index)
    
    def check_updates(self):
        """检查GitHub更新"""
        # 如果设置为自动检查更新
        if self.settings.get("auto_check_update", True):
            try:
                has_update, version, announcement = check_for_updates()
                if has_update:
                    self.home_page.update_announcement(f"发现新版本: {version}\n{announcement}")
            except Exception as e:
                print(f"检查更新时出错: {e}")
    
    def apply_stylesheet(self, theme="dark"):
        """应用主题样式表"""
        stylesheet = load_stylesheet(theme)
        if stylesheet:
            self.setStyleSheet(stylesheet)
            # 更新设置
            self.settings["theme"] = theme
            # 保存设置
            with open(os.path.join(os.path.dirname(__file__), "data/settings.json"), "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 显示启动画面
    splash = SplashScreen()
    splash.show()
    
    # 主窗口
    window = MainWindow()
    
    # 在启动画面显示2秒后显示主窗口
    def show_main_window():
        splash.finish(window)
        window.show()
    
    QTimer.singleShot(2000, show_main_window)
    
    sys.exit(app.exec_())
