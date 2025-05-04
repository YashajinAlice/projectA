import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                            QComboBox, QHBoxLayout, QCheckBox, QGroupBox,
                            QSlider, QFileDialog, QColorDialog, QMessageBox,
                            QScrollArea, QLineEdit)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from ui.utils import get_settings, save_settings


class SettingsPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.settings = get_settings()
        self.media_player = QMediaPlayer()
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        
        # 创建内容小部件
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("设置")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 主题设置
        theme_group = QGroupBox("主题设置")
        theme_layout = QVBoxLayout()
        
        # 主题选择
        theme_label = QLabel("选择主题:")
        theme_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["深色主题", "浅色主题"])
        self.theme_combo.setCurrentIndex(0 if self.settings.get("theme") == "dark" else 1)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        theme_layout.addWidget(self.theme_combo)
        
        # 主题按钮
        theme_buttons = QHBoxLayout()
        
        light_button = QPushButton("浅色")
        light_button.clicked.connect(lambda: self.set_theme("light"))
        theme_buttons.addWidget(light_button)
        
        dark_button = QPushButton("深色")
        dark_button.clicked.connect(lambda: self.set_theme("dark"))
        theme_buttons.addWidget(dark_button)
        
        theme_layout.addLayout(theme_buttons)
        
        # 背景设置
        bg_label = QLabel("应用背景:")
        theme_layout.addWidget(bg_label)
        
        bg_buttons = QHBoxLayout()
        
        select_bg_button = QPushButton("选择背景图片")
        select_bg_button.clicked.connect(self.select_background)
        bg_buttons.addWidget(select_bg_button)
        
        clear_bg_button = QPushButton("清除背景")
        clear_bg_button.clicked.connect(self.clear_background)
        bg_buttons.addWidget(clear_bg_button)
        
        theme_layout.addLayout(bg_buttons)
        
        # 背景预览
        self.bg_preview = QLabel("无背景图片")
        self.bg_preview.setAlignment(Qt.AlignCenter)
        self.bg_preview.setMinimumHeight(100)
        self.bg_preview.setStyleSheet("""
            border: 1px dashed;
            border-radius: 5px;
        """)
        
        # 如果有背景图片，显示预览
        bg_path = self.settings.get("background", "")
        if bg_path and os.path.exists(bg_path):
            pixmap = QPixmap(bg_path).scaled(300, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.bg_preview.setPixmap(pixmap)
        
        theme_layout.addWidget(self.bg_preview)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # 音乐设置
        music_group = QGroupBox("音乐设置")
        music_layout = QVBoxLayout()
        
        # 启用音乐
        self.enable_music = QCheckBox("启用背景音乐")
        self.enable_music.setChecked(self.settings.get("enable_music", True))
        self.enable_music.stateChanged.connect(self.toggle_music)
        music_layout.addWidget(self.enable_music)
        
        # 音量控制
        volume_layout = QHBoxLayout()
        volume_label = QLabel("音量:")
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.settings.get("music_volume", 50))
        self.volume_slider.valueChanged.connect(self.change_volume)
        volume_layout.addWidget(self.volume_slider)
        
        volume_value = QLabel(f"{self.settings.get('music_volume', 50)}%")
        self.volume_slider.valueChanged.connect(lambda v: volume_value.setText(f"{v}%"))
        volume_layout.addWidget(volume_value)
        
        music_layout.addLayout(volume_layout)
        
        # 选择音乐文件
        music_file_layout = QHBoxLayout()
        music_file_label = QLabel("音乐文件:")
        music_file_layout.addWidget(music_file_label)
        
        self.music_file_path = QLabel(self.settings.get("music_file", "默认音乐"))
        self.music_file_path.setWordWrap(True)
        music_file_layout.addWidget(self.music_file_path)
        
        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self.browse_music_file)
        music_file_layout.addWidget(browse_button)
        
        music_layout.addLayout(music_file_layout)
        
        # 播放/停止按钮
        play_layout = QHBoxLayout()
        
        play_button = QPushButton("播放")
        play_button.clicked.connect(self.play_music)
        play_layout.addWidget(play_button)
        
        stop_button = QPushButton("停止")
        stop_button.clicked.connect(self.stop_music)
        play_layout.addWidget(stop_button)
        
        music_layout.addLayout(play_layout)
        
        music_group.setLayout(music_layout)
        layout.addWidget(music_group)
        
        # 其他设置
        other_group = QGroupBox("其他设置")
        other_layout = QVBoxLayout()
        
        # 自动检查更新
        self.auto_check_update = QCheckBox("启动时自动检查更新")
        self.auto_check_update.setChecked(self.settings.get("auto_check_update", True))
        other_layout.addWidget(self.auto_check_update)
        
        # 显示运行时间
        self.show_runtime = QCheckBox("显示应用运行时间")
        self.show_runtime.setChecked(self.settings.get("show_runtime", True))
        other_layout.addWidget(self.show_runtime)
        
        other_group.setLayout(other_layout)
        layout.addWidget(other_group)
        
        # GitHub更新设置
        github_group = QGroupBox("GitHub更新设置")
        github_layout = QVBoxLayout()
        
        # 注释说明
        github_note = QLabel("注意: 以下设置用于GitHub更新检查，目前处于注释状态，需要时可以取消注释使用。")
        github_note.setWordWrap(True)
        github_note.setStyleSheet("color: #e74c3c;")
        github_layout.addWidget(github_note)
        
        # 仓库设置
        repo_layout = QHBoxLayout()
        repo_label = QLabel("GitHub仓库:")
        repo_layout.addWidget(repo_label)
        
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("用户名/仓库名")
        self.repo_input.setText(self.settings.get("github_repo", ""))
        self.repo_input.setEnabled(True)  # 暂时禁用
        repo_layout.addWidget(self.repo_input)
        
        github_layout.addLayout(repo_layout)
        
        # 分支设置
        branch_layout = QHBoxLayout()
        branch_label = QLabel("分支:")
        branch_layout.addWidget(branch_label)
        
        self.branch_input = QLineEdit()
        self.branch_input.setPlaceholderText("main")
        self.branch_input.setText(self.settings.get("github_branch", "main"))
        self.branch_input.setEnabled(False)  # 暂时禁用
        branch_layout.addWidget(self.branch_input)
        
        github_layout.addLayout(branch_layout)
        
        github_group.setLayout(github_layout)
        layout.addWidget(github_group)
        
        # 保存按钮
        save_button = QPushButton("保存设置")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
    
    def change_theme(self, index):
        """切换主题"""
        themes = ["dark", "light"]
        if index < len(themes):
            self.set_theme(themes[index])
    
    def set_theme(self, theme):
        """设置主题"""
        if self.main_window:
            self.main_window.apply_stylesheet(theme)
    
    def toggle_music(self, state):
        """切换音乐开关"""
        self.settings["enable_music"] = bool(state)
        if not state:
            self.stop_music()
    
    def change_volume(self, value):
        """调整音量"""
        self.settings["music_volume"] = value
        self.media_player.setVolume(value)
    
    def browse_music_file(self):
        """浏览音乐文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择音乐文件", "", "音频文件 (*.mp3 *.wav *.ogg);;所有文件 (*.*)"
        )
        
        if file_path:
            self.settings["music_file"] = file_path
            self.music_file_path.setText(file_path)
    
    def play_music(self):
        """播放音乐"""
        music_file = self.settings.get("music_file", "")
        if music_file and os.path.exists(music_file):
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(music_file)))
            self.media_player.setVolume(self.settings.get("music_volume", 50))
            self.media_player.play()
    
    def stop_music(self):
        """停止音乐"""
        self.media_player.stop()
    
    def select_background(self):
        """选择背景图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择背景图片", "", "图片文件 (*.jpg *.jpeg *.png);;所有文件 (*.*)"
        )
        
        if file_path:
            self.settings["background"] = file_path
            pixmap = QPixmap(file_path).scaled(300, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.bg_preview.setPixmap(pixmap)
    
    def clear_background(self):
        """清除背景图片"""
        self.settings["background"] = ""
        self.bg_preview.setText("无背景图片")
        self.bg_preview.setPixmap(QPixmap())
    
    def save_settings(self):
        """保存设置"""
        # 更新设置
        self.settings["enable_music"] = self.enable_music.isChecked()
        self.settings["music_volume"] = self.volume_slider.value()
        self.settings["auto_check_update"] = self.auto_check_update.isChecked()
        self.settings["show_runtime"] = self.show_runtime.isChecked()
        self.settings["theme"] = "dark" if self.theme_combo.currentIndex() == 0 else "light"
        
        # 保存设置
        if save_settings(self.settings):
            QMessageBox.information(self, "设置", "设置已保存")
        else:
            QMessageBox.warning(self, "设置", "保存设置失败")
