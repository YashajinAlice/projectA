import json
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QInputDialog, QMessageBox, QHBoxLayout


class TodoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.todo_file = "src/data/todo.json"
        self.todos = self.load_todos()

        layout = QVBoxLayout()

        # 待辦事項列表
        self.todo_list = QListWidget()
        self.refresh_todo_list()
        layout.addWidget(self.todo_list)

        # 新增、編輯、刪除按鈕
        button_layout = QHBoxLayout()

        add_button = QPushButton("新增")
        add_button.clicked.connect(self.add_todo)
        button_layout.addWidget(add_button)

        edit_button = QPushButton("編輯")
        edit_button.clicked.connect(self.edit_todo)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("刪除")
        delete_button.clicked.connect(self.delete_todo)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_todos(self):
        """從 JSON 文件加載待辦事項"""
        if not os.path.exists(self.todo_file):
            # 如果文件不存在，創建一個空的 JSON 文件
            os.makedirs(os.path.dirname(self.todo_file), exist_ok=True)
            with open(self.todo_file, "w", encoding="utf-8") as file:
                json.dump([], file)

        try:
            with open(self.todo_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    def save_todos(self):
        """將待辦事項保存到 JSON 文件"""
        with open(self.todo_file, "w", encoding="utf-8") as file:
            json.dump(self.todos, file, ensure_ascii=False, indent=4)

    def refresh_todo_list(self):
        """刷新待辦事項列表"""
        self.todo_list.clear()
        for todo in self.todos:
            self.todo_list.addItem(todo)

    def add_todo(self):
        """新增待辦事項"""
        text, ok = QInputDialog.getText(self, "新增待辦事項", "請輸入待辦事項：")
        if ok and text:
            self.todos.append(text)
            self.save_todos()
            self.refresh_todo_list()

    def edit_todo(self):
        """編輯選中的待辦事項"""
        current_row = self.todo_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "錯誤", "請選擇一個待辦事項進行編輯！")
            return

        current_text = self.todos[current_row]
        text, ok = QInputDialog.getText(self, "編輯待辦事項", "修改待辦事項：", text=current_text)
        if ok and text:
            self.todos[current_row] = text
            self.save_todos()
            self.refresh_todo_list()

    def delete_todo(self):
        """刪除選中的待辦事項"""
        current_row = self.todo_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "錯誤", "請選擇一個待辦事項進行刪除！")
            return

        del self.todos[current_row]
        self.save_todos()
        self.refresh_todo_list()
