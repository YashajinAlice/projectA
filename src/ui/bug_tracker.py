import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, 
                            QLabel, QDialog, QFormLayout, QLineEdit, QComboBox, 
                            QMessageBox, QListWidgetItem, QTabWidget)
from PyQt5.QtCore import Qt


class BugDialog(QDialog):
    def __init__(self, parent=None, bug=None):
        super().__init__(parent)
        self.setWindowTitle("BUG记录")
        self.setMinimumWidth(500)
        
        layout = QFormLayout()
        
        # 项目名称
        self.project_name = QLineEdit()
        layout.addRow("项目名称:", self.project_name)
        
        # 错误内容
        self.error_content = QLineEdit()
        layout.addRow("错误内容:", self.error_content)
        
        # 严重度
        self.severity = QComboBox()
        self.severity.addItems(["低", "中", "高", "致命"])
        layout.addRow("严重度:", self.severity)
        
        # 优先级
        self.priority = QComboBox()
        self.priority.addItems(["低", "中", "高", "紧急"])
        layout.addRow("优先级:", self.priority)
        
        # 如果是编辑模式，填充现有数据
        if bug:
            self.project_name.setText(bug['project_name'])
            self.error_content.setText(bug['error_content'])
            self.severity.setCurrentText(bug['severity'])
            self.priority.setCurrentText(bug['priority'])
        
        # 按钮
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addRow("", button_layout)
        
        self.setLayout(layout)
    
    def get_bug_data(self):
        return {
            'project_name': self.project_name.text(),
            'error_content': self.error_content.text(),
            'severity': self.severity.currentText(),
            'priority': self.priority.currentText(),
            'completed': False,
            'created_at': datetime.now().isoformat()
        }


class BugTrackerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.bug_file = os.path.join(os.path.dirname(__file__), "../data/bugs.json")
        self.bugs = self.load_bugs()
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("BUG跟踪器")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        layout.addWidget(title_label)
        
        # 创建选项卡
        self.tabs = QTabWidget()
        
        # 待修复BUG选项卡
        active_tab = QWidget()
        active_layout = QVBoxLayout()
        
        self.active_bug_list = QListWidget()
        self.active_bug_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                border-bottom: 1px solid #ecf0f1;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        active_layout.addWidget(self.active_bug_list)
        active_tab.setLayout(active_layout)
        
        # 已修复BUG选项卡
        completed_tab = QWidget()
        completed_layout = QVBoxLayout()
        
        self.completed_bug_list = QListWidget()
        self.completed_bug_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                border-bottom: 1px solid #ecf0f1;
                padding: 5px;
                color: #7f8c8d;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        completed_layout.addWidget(self.completed_bug_list)
        completed_tab.setLayout(completed_layout)
        
        # 添加选项卡
        self.tabs.addTab(active_tab, "待修复")
        self.tabs.addTab(completed_tab, "已修复")
        layout.addWidget(self.tabs)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("新增")
        add_button.setStyleSheet("""
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
        add_button.clicked.connect(self.add_bug)
        button_layout.addWidget(add_button)
        
        edit_button = QPushButton("编辑")
        edit_button.setStyleSheet("""
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
        edit_button.clicked.connect(self.edit_bug)
        button_layout.addWidget(edit_button)
        
        complete_button = QPushButton("完成")
        complete_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        complete_button.clicked.connect(self.complete_bug)
        button_layout.addWidget(complete_button)
        
        delete_button = QPushButton("删除")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_button.clicked.connect(self.delete_bug)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # 刷新列表
        self.refresh_bug_list()
    
    def load_bugs(self):
        """从 JSON 文件加载BUG"""
        os.makedirs(os.path.dirname(self.bug_file), exist_ok=True)
        
        # 检查文件是否存在，如果不存在或损坏，创建一个新的空文件
        try:
            if os.path.exists(self.bug_file):
                try:
                    with open(self.bug_file, "r", encoding="utf-8") as file:
                        return json.load(file)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    print(f"警告: 无法读取BUG文件，将创建新文件")
                    # 文件存在但无法读取，备份并创建新文件
                    if os.path.exists(self.bug_file):
                        backup_file = f"{self.bug_file}.bak"
                        try:
                            import shutil
                            shutil.copy2(self.bug_file, backup_file)
                            print(f"已将原文件备份为 {backup_file}")
                        except Exception as e:
                            print(f"备份文件失败: {e}")
            
            # 创建新的空文件
            with open(self.bug_file, "w", encoding="utf-8") as file:
                json.dump([], file)
            return []
        except Exception as e:
            print(f"加载BUG记录时出错: {e}")
            return []
    
    def save_bugs(self):
        """将BUG保存到 JSON 文件"""
        with open(self.bug_file, "w", encoding="utf-8") as file:
            json.dump(self.bugs, file, ensure_ascii=False, indent=4)
    
    def refresh_bug_list(self):
        """刷新BUG列表"""
        self.active_bug_list.clear()
        self.completed_bug_list.clear()
        
        # 按优先级和严重度排序
        priority_order = {"紧急": 0, "高": 1, "中": 2, "低": 3}
        severity_order = {"致命": 0, "高": 1, "中": 2, "低": 3}
        
        self.bugs.sort(key=lambda x: (
            priority_order.get(x.get('priority', "低"), 3),
            severity_order.get(x.get('severity', "低"), 3)
        ))
        
        for bug in self.bugs:
            item_text = f"[{bug['project_name']}] {bug['error_content']} - 严重度:{bug['severity']} 优先级:{bug['priority']}"
            if bug.get('completed', False):
                self.completed_bug_list.addItem(item_text)
            else:
                self.active_bug_list.addItem(item_text)
    
    def add_bug(self):
        """新增BUG"""
        dialog = BugDialog(self)
        if dialog.exec_():
            bug_data = dialog.get_bug_data()
            self.bugs.append(bug_data)
            self.save_bugs()
            self.refresh_bug_list()
    
    def edit_bug(self):
        """编辑选中的BUG"""
        current_tab = self.tabs.currentIndex()
        bug_list = self.active_bug_list if current_tab == 0 else self.completed_bug_list
        
        if bug_list.currentRow() < 0:
            QMessageBox.warning(self, "错误", "请选择一个BUG进行编辑！")
            return
        
        current_item = bug_list.currentItem()
        current_index = self.get_bug_index(current_item.text(), current_tab == 1)
        
        if current_index < 0:
            QMessageBox.warning(self, "错误", "找不到选中的BUG！")
            return
        
        dialog = BugDialog(self, self.bugs[current_index])
        if dialog.exec_():
            new_data = dialog.get_bug_data()
            # 保持完成状态
            new_data['completed'] = self.bugs[current_index].get('completed', False)
            if 'completed_at' in self.bugs[current_index]:
                new_data['completed_at'] = self.bugs[current_index]['completed_at']
            
            self.bugs[current_index] = new_data
            self.save_bugs()
            self.refresh_bug_list()
    
    def complete_bug(self):
        """将BUG标记为已修复"""
        if self.tabs.currentIndex() != 0 or self.active_bug_list.currentRow() < 0:
            QMessageBox.warning(self, "错误", "请在待修复选项卡中选择一个BUG标记为已修复！")
            return
        
        current_item = self.active_bug_list.currentItem()
        current_index = self.get_bug_index(current_item.text(), False)
        
        if current_index >= 0:
            self.bugs[current_index]['completed'] = True
            self.bugs[current_index]['completed_at'] = datetime.now().isoformat()
            self.save_bugs()
            self.refresh_bug_list()
    
    def delete_bug(self):
        """删除选中的BUG"""
        current_tab = self.tabs.currentIndex()
        bug_list = self.active_bug_list if current_tab == 0 else self.completed_bug_list
        
        if bug_list.currentRow() < 0:
            QMessageBox.warning(self, "错误", "请选择一个BUG进行删除！")
            return
        
        current_item = bug_list.currentItem()
        current_index = self.get_bug_index(current_item.text(), current_tab == 1)
        
        if current_index < 0:
            QMessageBox.warning(self, "错误", "找不到选中的BUG！")
            return
        
        reply = QMessageBox.question(self, "确认删除", 
                                    "确定要删除这个BUG记录吗？", 
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            del self.bugs[current_index]
            self.save_bugs()
            self.refresh_bug_list()
    
    def get_bug_index(self, item_text, is_completed):
        """根据列表项文本获取BUG索引"""
        # 从文本中提取项目名称和错误内容
        try:
            project_name = item_text.split(']')[0].strip('[')
            error_content = item_text.split(']')[1].split('-')[0].strip()
            
            # 查找匹配的BUG
            for i, bug in enumerate(self.bugs):
                if (bug.get('project_name') == project_name and 
                    bug.get('error_content') in error_content and 
                    bug.get('completed', False) == is_completed):
                    return i
        except:
            pass
        
        return -1
