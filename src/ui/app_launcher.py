import os
import subprocess
import time
import threading
import json
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QListWidget, QListWidgetItem, QFileDialog, 
                            QInputDialog, QMessageBox, QGridLayout, QFrame,
                            QScrollArea, QLineEdit)
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QRect


class AppCard(QFrame):
    clicked = pyqtSignal(object)
    
    def __init__(self, app_data, parent=None):
        super().__init__(parent)
        self.app_data = app_data
        self.setFixedSize(180, 200)
        self.setCursor(Qt.PointingHandCursor)
        
        # 设置圆角和阴影效果
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)
        
        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # 图标
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        # 设置图标
        if app_data.get("icon") and os.path.exists(app_data["icon"]):
            pixmap = QPixmap(app_data["icon"]).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(pixmap)
        else:
            # 默认图标
            self.icon_label.setText("📱")
            self.icon_label.setStyleSheet("font-size: 40px;")
        
        layout.addWidget(self.icon_label)
        
        # 应用名称
        name_label = QLabel(app_data["name"])
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(name_label)
        
        # 路径
        path_label = QLabel(os.path.basename(app_data["path"]))
        path_label.setAlignment(Qt.AlignCenter)
        path_label.setStyleSheet("font-size: 10px; color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(path_label)
        
        # 运行次数
        runs_label = QLabel(f"运行次数: {app_data.get('runs', 0)}")
        runs_label.setAlignment(Qt.AlignCenter)
        runs_label.setStyleSheet("font-size: 10px; color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(runs_label)
        
        # 最后运行时间
        last_run = app_data.get("last_run", "")
        if last_run:
            last_run_label = QLabel(f"上次运行: {last_run}")
            last_run_label.setAlignment(Qt.AlignCenter)
            last_run_label.setStyleSheet("font-size: 10px; color: rgba(255, 255, 255, 0.7);")
            layout.addWidget(last_run_label)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.app_data)
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.geometry())
        
        # 向上移动并放大一点
        new_rect = self.geometry()
        new_rect.setY(new_rect.y() - 5)
        self.animation.setEndValue(new_rect)
        
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        
        # 改变背景色
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
        """)
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.geometry())
        
        # 恢复原位
        new_rect = self.geometry()
        new_rect.setY(new_rect.y() + 5)
        self.animation.setEndValue(new_rect)
        
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        
        # 恢复背景色
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
        """)
        
        super().leaveEvent(event)


class AppLauncherPage(QWidget):
    app_started = pyqtSignal(str, bool)
    
    def __init__(self, home_page=None):
        super().__init__()
        self.home_page = home_page
        self.app_file = os.path.join(os.path.dirname(__file__), "../data/apps.json")
        self.apps = []
        self.running_processes = {}
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 标题
        title_layout = QHBoxLayout()
        
        title_label = QLabel("应用启动器")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # 添加应用按钮
        add_button = QPushButton("添加应用")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(46, 204, 113, 0.8);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(46, 204, 113, 1.0);
            }
        """)
        add_button.clicked.connect(self.add_app)
        title_layout.addWidget(add_button)
        
        main_layout.addLayout(title_layout)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # 应用网格容器
        self.app_container = QWidget()
        self.app_grid = QGridLayout(self.app_container)
        self.app_grid.setContentsMargins(10, 10, 10, 10)
        self.app_grid.setSpacing(20)
        self.app_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        scroll_area.setWidget(self.app_container)
        main_layout.addWidget(scroll_area)
        
        # 运行信息
        self.run_info = QLabel("选择一个应用程序启动")
        self.run_info.setAlignment(Qt.AlignCenter)
        self.run_info.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.7); margin-top: 10px;")
        main_layout.addWidget(self.run_info)
        
        # 加载应用列表
        self.load_apps()
        
        # 连接信号
        self.app_started.connect(self.update_home_page)
    
    def load_apps(self):
        """加载应用列表"""
        try:
            if os.path.exists(self.app_file):
                with open(self.app_file, "r", encoding="utf-8") as f:
                    self.apps = json.load(f)
            else:
                self.save_apps()
        except Exception as e:
            print(f"加载应用列表失败: {e}")
            # 示例应用
            self.apps = [
                {"name": "记事本", "path": "notepad.exe", "icon": "", "runs": 0, "last_run": ""},
                {"name": "计算器", "path": "calc.exe", "icon": "", "runs": 0, "last_run": ""}
            ]
        
        self.refresh_app_grid()
    
    def save_apps(self):
        """保存应用列表"""
        try:
            os.makedirs(os.path.dirname(self.app_file), exist_ok=True)
            with open(self.app_file, "w", encoding="utf-8") as f:
                json.dump(self.apps, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存应用列表失败: {e}")
    
    def refresh_app_grid(self):
        """刷新应用网格"""
        # 清除现有项目
        while self.app_grid.count():
            item = self.app_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 添加应用卡片
        for i, app in enumerate(self.apps):
            row = i // 4
            col = i % 4
            
            app_card = AppCard(app)
            app_card.clicked.connect(self.launch_app)
            
            self.app_grid.addWidget(app_card, row, col)
    
    def add_app(self):
        """添加应用"""
        app_path, _ = QFileDialog.getOpenFileName(
            self, "选择应用程序", "", "可执行文件 (*.exe);;所有文件 (*.*)"
        )
        
        if not app_path:
            return
        
        app_name, ok = QInputDialog.getText(
            self, "应用名称", "请输入应用名称:", text=os.path.basename(app_path).split('.')[0]
        )
        
        if not ok or not app_name:
            return
        
        # 可选：选择图标
        icon_path, _ = QFileDialog.getOpenFileName(
            self, "选择图标（可选）", "", "图标文件 (*.ico *.png *.jpg);;所有文件 (*.*)"
        )
        
        self.apps.append({
            "name": app_name,
            "path": app_path,
            "icon": icon_path,
            "runs": 0,
            "last_run": ""
        })
        
        self.save_apps()
        self.refresh_app_grid()
    
    def launch_app(self, app_data):
        """启动应用"""
        app_name = app_data["name"]
        app_path = app_data["path"]
        
        # 检查应用是否已在运行
        if app_name in self.running_processes:
            QMessageBox.information(self, "提示", f"{app_name} 已经在运行中")
            return
        
        try:
            # 启动应用
            process = subprocess.Popen(app_path)
            self.running_processes[app_name] = {
                "process": process,
                "start_time": time.time()
            }
            
            # 更新运行信息
            self.run_info.setText(f"{app_name} 正在运行中...")
            
            # 更新应用数据
            for app in self.apps:
                if app["name"] == app_name:
                    app["runs"] = app.get("runs", 0) + 1
                    app["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break
            
            self.save_apps()
            self.refresh_app_grid()
            
            # 通知首页
            self.app_started.emit(app_name, True)
            
            # 启动监控线程
            threading.Thread(
                target=self.monitor_process,
                args=(app_name, process),
                daemon=True
            ).start()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动应用失败: {str(e)}")
    
    def monitor_process(self, app_name, process):
        """监控应用进程"""
        process.wait()
        
        # 计算运行时间
        if app_name in self.running_processes:
            start_time = self.running_processes[app_name]["start_time"]
            run_time = time.time() - start_time
            
            # 格式化运行时间
            hours, remainder = divmod(run_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒"
            
            # 更新UI（需要在主线程中执行）
            self.app_started.emit(app_name, False)
            
            # 从运行列表中移除
            del self.running_processes[app_name]
    
    def remove_app(self, app_name):
        """移除应用"""
        # 检查应用是否在运行
        if app_name in self.running_processes:
            QMessageBox.warning(self, "错误", f"{app_name} 正在运行中，无法移除！")
            return
        
        reply = QMessageBox.question(
            self, "确认移除", f"确定要移除 {app_name} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 查找并移除应用
            for i, app in enumerate(self.apps):
                if app["name"] == app_name:
                    del self.apps[i]
                    break
            
            self.save_apps()
            self.refresh_app_grid()
    
    def update_home_page(self, app_name, is_running):
        """更新首页的运行信息"""
        if self.home_page:
            self.home_page.update_running_app(app_name, is_running)
        
        # 更新运行信息
        if is_running:
            self.run_info.setText(f"{app_name} 正在运行中...")
        else:
            self.run_info.setText("选择一个应用程序启动")
    
    def contextMenuEvent(self, event):
        """右键菜单事件"""
        # 获取点击位置的小部件
        child = self.childAt(event.pos())
        
        # 查找父级AppCard
        app_card = None
        while child:
            if isinstance(child, AppCard):
                app_card = child
                break
            child = child.parent()
        
        if app_card:
            from PyQt5.QtWidgets import QMenu
            
            menu = QMenu(self)
            
            # 启动应用
            launch_action = menu.addAction("启动")
            launch_action.triggered.connect(lambda: self.launch_app(app_card.app_data))
            
            # 移除应用
            remove_action = menu.addAction("移除")
            remove_action.triggered.connect(lambda: self.remove_app(app_card.app_data["name"]))
            
            # 显示菜单
            menu.exec_(event.globalPos())
