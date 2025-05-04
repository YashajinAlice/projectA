import os
import subprocess
import time
import threading
import json
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QFileDialog, QInputDialog, QMessageBox,
                            QGridLayout, QFrame, QScrollArea, QMenu)
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QRect


class GameCard(QFrame):
    clicked = pyqtSignal(object)
    
    def __init__(self, game_data, parent=None):
        super().__init__(parent)
        self.game_data = game_data
        self.setFixedSize(200, 250)
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
        self.icon_label.setMinimumHeight(100)
        
        # 设置图标
        if game_data.get("icon") and os.path.exists(game_data["icon"]):
            pixmap = QPixmap(game_data["icon"]).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(pixmap)
        else:
            # 默认图标
            self.icon_label.setText("🎮")
            self.icon_label.setStyleSheet("font-size: 50px;")
        
        layout.addWidget(self.icon_label)
        
        # 游戏名称
        name_label = QLabel(game_data["name"])
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(name_label)
        
        # 路径
        path_label = QLabel(os.path.basename(game_data["path"]))
        path_label.setAlignment(Qt.AlignCenter)
        path_label.setStyleSheet("font-size: 10px; color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(path_label)
        
        # 运行次数
        runs_label = QLabel(f"运行次数: {game_data.get('runs', 0)}")
        runs_label.setAlignment(Qt.AlignCenter)
        runs_label.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(runs_label)
        
        # 总运行时间
        total_time = game_data.get("total_time", 0)
        hours, remainder = divmod(total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{int(hours)}小时{int(minutes)}分钟"
        
        time_label = QLabel(f"总运行时间: {time_str}")
        time_label.setAlignment(Qt.AlignCenter)
        time_label.setStyleSheet("font-size: 12px; color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(time_label)
        
        # 最后运行时间
        last_run = game_data.get("last_run", "")
        if last_run:
            last_run_label = QLabel(f"上次运行: {last_run}")
            last_run_label.setAlignment(Qt.AlignCenter)
            last_run_label.setStyleSheet("font-size: 10px; color: rgba(255, 255, 255, 0.7);")
            layout.addWidget(last_run_label)
        
        # 启动按钮
        launch_button = QPushButton("启动游戏")
        launch_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(52, 152, 219, 0.8);
                color: white;
                border: none;
                border-radius:152,219,0.8);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 1.0);
            }
        """)
        launch_button.clicked.connect(lambda: self.clicked.emit(self.game_data))
        layout.addWidget(launch_button)
    
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


class GameLauncherPage(QWidget):
    game_started = pyqtSignal(str, bool)
    
    def __init__(self, home_page=None):
        super().__init__()
        self.home_page = home_page
        self.game_file = os.path.join(os.path.dirname(__file__), "../data/games.json")
        self.games = []
        self.running_processes = {}
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 标题
        title_layout = QHBoxLayout()
        
        title_label = QLabel("游戏启动器")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # 添加游戏按钮
        add_button = QPushButton("添加游戏")
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
        add_button.clicked.connect(self.add_game)
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
        
        # 游戏网格容器
        self.game_container = QWidget()
        self.game_grid = QGridLayout(self.game_container)
        self.game_grid.setContentsMargins(10, 10, 10, 10)
        self.game_grid.setSpacing(20)
        self.game_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        scroll_area.setWidget(self.game_container)
        main_layout.addWidget(scroll_area)
        
        # 运行信息
        self.run_info = QLabel("点击游戏卡片启动游戏")
        self.run_info.setAlignment(Qt.AlignCenter)
        self.run_info.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.7); margin-top: 10px;")
        main_layout.addWidget(self.run_info)
        
        # 加载游戏列表
        self.load_games()
        
        # 连接信号
        self.game_started.connect(self.update_home_page)
    
    def load_games(self):
        """加载游戏列表"""
        try:
            if os.path.exists(self.game_file):
                with open(self.game_file, "r", encoding="utf-8") as f:
                    self.games = json.load(f)
            else:
                # 示例游戏
                self.games = [
                    {"name": "记事本游戏", "path": "notepad.exe", "icon": "", "runs": 0, "total_time": 0, "last_run": ""},
                    {"name": "计算器游戏", "path": "calc.exe", "icon": "", "runs": 0, "total_time": 0, "last_run": ""}
                ]
                self.save_games()
        except Exception as e:
            print(f"加载游戏列表失败: {e}")
            # 示例游戏
            self.games = [
                {"name": "记事本游戏", "path": "notepad.exe", "icon": "", "runs": 0, "total_time": 0, "last_run": ""},
                {"name": "计算器游戏", "path": "calc.exe", "icon": "", "runs": 0, "total_time": 0, "last_run": ""}
            ]
        
        self.refresh_game_grid()
    
    def save_games(self):
        """保存游戏列表"""
        try:
            os.makedirs(os.path.dirname(self.game_file), exist_ok=True)
            with open(self.game_file, "w", encoding="utf-8") as f:
                json.dump(self.games, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存游戏列表失败: {e}")
    
    def refresh_game_grid(self):
        """刷新游戏网格"""
        # 清除现有项目
        while self.game_grid.count():
            item = self.game_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 添加游戏卡片
        for i, game in enumerate(self.games):
            row = i // 3
            col = i % 3
            
            game_card = GameCard(game)
            game_card.clicked.connect(self.launch_game)
            
            self.game_grid.addWidget(game_card, row, col)
    
    def add_game(self):
        """添加游戏"""
        game_path, _ = QFileDialog.getOpenFileName(
            self, "选择游戏", "", "可执行文件 (*.exe);;所有文件 (*.*)"
        )
        
        if not game_path:
            return
        
        game_name, ok = QInputDialog.getText(
            self, "游戏名称", "请输入游戏名称:", text=os.path.basename(game_path).split('.')[0]
        )
        
        if not ok or not game_name:
            return
        
        # 可选：选择图标
        icon_path, _ = QFileDialog.getOpenFileName(
            self, "选择图标（可选）", "", "图标文件 (*.ico *.png *.jpg);;所有文件 (*.*)"
        )
        
        self.games.append({
            "name": game_name,
            "path": game_path,
            "icon": icon_path,
            "runs": 0,
            "total_time": 0,
            "last_run": ""
        })
        
        self.save_games()
        self.refresh_game_grid()
    
    def launch_game(self, game_data):
        """启动游戏"""
        game_name = game_data["name"]
        game_path = game_data["path"]
        
        # 检查游戏是否已在运行
        if game_name in self.running_processes:
            QMessageBox.information(self, "提示", f"{game_name} 已经在运行中")
            return
        
        try:
            # 启动游戏
            process = subprocess.Popen(game_path)
            self.running_processes[game_name] = {
                "process": process,
                "start_time": time.time()
            }
            
            # 更新运行信息
            self.run_info.setText(f"{game_name} 正在运行中...")
            
            # 更新游戏数据
            for game in self.games:
                if game["name"] == game_name:
                    game["runs"] = game.get("runs", 0) + 1
                    game["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break
            
            self.save_games()
            self.refresh_game_grid()
            
            # 通知首页
            self.game_started.emit(game_name, True)
            
            # 启动监控线程
            threading.Thread(
                target=self.monitor_process,
                args=(game_name, process),
                daemon=True
            ).start()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动游戏失败: {str(e)}")
    
    def monitor_process(self, game_name, process):
        """监控游戏进程"""
        process.wait()
        
        # 计算运行时间
        if game_name in self.running_processes:
            start_time = self.running_processes[game_name]["start_time"]
            run_time = time.time() - start_time
            
            # 更新游戏总运行时间
            for game in self.games:
                if game["name"] == game_name:
                    game["total_time"] = game.get("total_time", 0) + run_time
                    break
            
            self.save_games()
            
            # 格式化运行时间
            hours, remainder = divmod(run_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒"
            
            # 更新UI（需要在主线程中执行）
            self.game_started.emit(game_name, False)
            
            # 从运行列表中移除
            del self.running_processes[game_name]
            
            # 刷新游戏网格
            self.refresh_game_grid()
    
    def remove_game(self, game_name):
        """移除游戏"""
        # 检查游戏是否在运行
        if game_name in self.running_processes:
            QMessageBox.warning(self, "错误", f"{game_name} 正在运行中，无法移除！")
            return
        
        reply = QMessageBox.question(
            self, "确认移除", f"确定要移除 {game_name} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 查找并移除游戏
            for i, game in enumerate(self.games):
                if game["name"] == game_name:
                    del self.games[i]
                    break
            
            self.save_games()
            self.refresh_game_grid()
    
    def update_home_page(self, game_name, is_running):
        """更新首页的运行信息"""
        if self.home_page:
            self.home_page.update_running_app(game_name, is_running)
        
        # 更新运行信息
        if is_running:
            self.run_info.setText(f"{game_name} 正在运行中...")
        else:
            self.run_info.setText("点击游戏卡片启动游戏")
    
    def contextMenuEvent(self, event):
        """右键菜单事件"""
        # 获取点击位置的小部件
        child = self.childAt(event.pos())
        
        # 查找父级GameCard
        game_card = None
        while child:
            if isinstance(child, GameCard):
                game_card = child
                break
            child = child.parent()
        
        if game_card:
            menu = QMenu(self)
            
            # 启动游戏
            launch_action = menu.addAction("启动")
            launch_action.triggered.connect(lambda: self.launch_game(game_card.game_data))
            
            # 移除游戏
            remove_action = menu.addAction("移除")
            remove_action.triggered.connect(lambda: self.remove_game(game_card.game_data["name"]))
            
            # 显示菜单
            menu.exec_(event.globalPos())
