import os
import json


def load_stylesheet(theme="dark"):
    """加载主题样式表"""
    stylesheet_path = os.path.join(os.path.dirname(__file__), f"../assets/styles/{theme}.qss")
    
    # 如果样式表文件不存在，创建默认样式表
    if not os.path.exists(stylesheet_path):
        os.makedirs(os.path.dirname(stylesheet_path), exist_ok=True)
        
        if theme == "dark":
            stylesheet = """
                QWidget {
                    background-color: #1e1e2e;
                    color: #cdd6f4;
                }
                
                QMainWindow {
                    background-color: #1e1e2e;
                }
                
                QPushButton {
                    background-color: #89b4fa;
                    color: #1e1e2e;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                
                QPushButton:hover {
                    background-color: #b4befe;
                }
                
                QPushButton:pressed {
                    background-color: #74c7ec;
                }
                
                QLineEdit, QTextEdit, QComboBox, QSpinBox {
                    background-color: #313244;
                    border: 1px solid #45475a;
                    border-radius: 5px;
                    padding: 5px;
                    color: #cdd6f4;
                }
                
                QListWidget, QTreeWidget, QTableWidget {
                    background-color: #313244;
                    border: 1px solid #45475a;
                    border-radius: 5px;
                    color: #cdd6f4;
                }
                
                QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {
                    background-color: #89b4fa;
                    color: #1e1e2e;
                }
                
                QTabWidget::pane {
                    border: 1px solid #45475a;
                    border-radius: 5px;
                }
                
                QTabBar::tab {
                    background-color: #313244;
                    color: #cdd6f4;
                    border-top-left-radius: 5px;
                    border-top-right-radius: 5px;
                    padding: 8px 16px;
                }
                
                QTabBar::tab:selected {
                    background-color: #89b4fa;
                    color: #1e1e2e;
                }
                
                QScrollBar:vertical {
                    border: none;
                    background-color: #313244;
                    width: 10px;
                    margin: 0px;
                }
                
                QScrollBar::handle:vertical {
                    background-color: #45475a;
                    border-radius: 5px;
                }
                
                QScrollBar:horizontal {
                    border: none;
                    background-color: #313244;
                    height: 10px;
                    margin: 0px;
                }
                
                QScrollBar::handle:horizontal {
                    background-color: #45475a;
                    border-radius: 5px;
                }
                
                QLabel {
                    color: #cdd6f4;
                }
                
                QGroupBox {
                    border: 1px solid #45475a;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                }
                
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    left: 10px;
                    padding: 0 5px;
                }
            """
        else:  # light theme
            stylesheet = """
                QWidget {
                    background-color: #eff1f5;
                    color: #4c4f69;
                }
                
                QMainWindow {
                    background-color: #eff1f5;
                }
                
                QPushButton {
                    background-color: #1e66f5;
                    color: #eff1f5;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                
                QPushButton:hover {
                    background-color: #7287fd;
                }
                
                QPushButton:pressed {
                    background-color: #209fb5;
                }
                
                QLineEdit, QTextEdit, QComboBox, QSpinBox {
                    background-color: #e6e9ef;
                    border: 1px solid #ccd0da;
                    border-radius: 5px;
                    padding: 5px;
                    color: #4c4f69;
                }
                
                QListWidget, QTreeWidget, QTableWidget {
                    background-color: #e6e9ef;
                    border: 1px solid #ccd0da;
                    border-radius: 5px;
                    color: #4c4f69;
                }
                
                QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {
                    background-color: #1e66f5;
                    color: #eff1f5;
                }
                
                QTabWidget::pane {
                    border: 1px solid #ccd0da;
                    border-radius: 5px;
                }
                
                QTabBar::tab {
                    background-color: #e6e9ef;
                    color: #4c4f69;
                    border-top-left-radius: 5px;
                    border-top-right-radius: 5px;
                    padding: 8px 16px;
                }
                
                QTabBar::tab:selected {
                    background-color: #1e66f5;
                    color: #eff1f5;
                }
                
                QScrollBar:vertical {
                    border: none;
                    background-color: #e6e9ef;
                    width: 10px;
                    margin: 0px;
                }
                
                QScrollBar::handle:vertical {
                    background-color: #ccd0da;
                    border-radius: 5px;
                }
                
                QScrollBar:horizontal {
                    border: none;
                    background-color: #e6e9ef;
                    height: 10px;
                    margin: 0px;
                }
                
                QScrollBar::handle:horizontal {
                    background-color: #ccd0da;
                    border-radius: 5px;
                }
                
                QLabel {
                    color: #4c4f69;
                }
                
                QGroupBox {
                    border: 1px solid #ccd0da;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                }
                
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    left: 10px;
                    padding: 0 5px;
                }
            """
        
        with open(stylesheet_path, "w", encoding="utf-8") as f:
            f.write(stylesheet)
    
    # 读取样式表
    try:
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"加载样式表失败: {e}")
        return ""


def get_settings():
    """获取应用设置"""
    settings_path = os.path.join(os.path.dirname(__file__), "../data/settings.json")
    
    # 默认设置
    default_settings = {
        "theme": "dark",
        "background": "",
        "enable_music": True,
        "music_volume": 50,
        "music_file": "",
        "auto_check_update": True,
        "show_runtime": True
    }
    
    # 如果设置文件不存在，创建默认设置
    if not os.path.exists(settings_path):
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=4)
        return default_settings
    
    # 读取设置
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
            # 确保所有默认设置都存在
            for key, value in default_settings.items():
                if key not in settings:
                    settings[key] = value
            return settings
    except Exception as e:
        print(f"加载设置失败: {e}")
        return default_settings


def save_settings(settings):
    """保存应用设置"""
    settings_path = os.path.join(os.path.dirname(__file__), "../data/settings.json")
    
    try:
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存设置失败: {e}")
        return False
