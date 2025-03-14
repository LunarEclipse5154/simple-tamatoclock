from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QListWidget, QListWidgetItem, QInputDialog, QMessageBox,
                           QLabel, QLineEdit, QColorDialog, QComboBox, QSpinBox, QCheckBox,
                           QDialog, QDateEdit, QTextEdit)
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QColor, QFont
from models import Task, Statistics
from datetime import datetime
from styles import ICONS, COLORS

class TaskListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timers)
        self.timer.start(1000)  # 每秒更新一次计时器
        self.init_ui()
        self.load_tasks()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 创建标题
        title_label = QLabel("任务清单")
        title_label.setFont(QFont("Arial", 24))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建任务列表
        self.task_list = QListWidget()
        self.task_list.setFont(QFont("Arial", 12))
        layout.addWidget(self.task_list)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        # 添加任务按钮
        self.add_btn = QPushButton("添加任务")
        self.add_btn.setIcon(ICONS['add'])
        self.add_btn.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_btn)
        
        # 删除任务按钮
        self.delete_btn = QPushButton("删除任务")
        self.delete_btn.setIcon(ICONS['delete'])
        self.delete_btn.clicked.connect(self.delete_task)
        button_layout.addWidget(self.delete_btn)
        
        # 完成任务按钮
        self.complete_btn = QPushButton("完成任务")
        self.complete_btn.setIcon(ICONS['check'])
        self.complete_btn.clicked.connect(self.complete_task)
        button_layout.addWidget(self.complete_btn)
        
    def load_tasks(self):
        if self.parent and hasattr(self.parent, 'main_timer'):
            self.task_list.clear()
            for i in range(self.parent.main_timer.task_list.count()):
                item = self.parent.main_timer.task_list.item(i)
                new_item = QListWidgetItem(item.text())
                new_item.setBackground(item.background())
                new_item.setFlags(item.flags())
                self.task_list.addItem(new_item)
                
    def add_task(self, task_name, color):
        item = QListWidgetItem(task_name)
        item.setBackground(color)
        self.task_list.addItem(item)
        
        # 同步到主界面
        if self.parent and hasattr(self.parent, 'main_timer'):
            self.parent.main_timer.add_task(task_name, color)
            
    def delete_task(self):
        current_item = self.task_list.currentItem()
        if current_item:
            reply = QMessageBox.question(self, "确认删除",
                                       "确定要删除这个任务吗？",
                                       QMessageBox.StandardButton.Yes |
                                       QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                row = self.task_list.row(current_item)
                self.task_list.takeItem(row)
                if self.parent and hasattr(self.parent, 'main_timer'):
                    self.parent.main_timer.task_list.takeItem(row)
                
    def complete_task(self, item):
        task_name = item.text()
        item.setBackground(QColor("#90EE90"))  # 浅绿色表示完成
        
        # 同步到主界面
        if self.parent and hasattr(self.parent, 'main_timer'):
            self.parent.main_timer.update_task_status(task_name, True)
            
    def update_timers(self):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            widget = self.task_list.itemWidget(item)
            if widget and widget.is_running:
                widget.update_timer()

    def get_tasks(self):
        tasks = []
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            tasks.append((item.text(), item.background().color()))
        return tasks

class TaskItemWidget(QWidget):
    def __init__(self, task_data):
        super().__init__()
        self.task_data = task_data
        self.is_running = False
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # 任务名称
        name_label = QLabel(self.task_data["name"])
        name_label.setStyleSheet(f"background-color: {self.task_data['color'].name()}; padding: 5px;")
        layout.addWidget(name_label)
        
        # 计时器类型
        timer_type = QLabel(self.task_data["timer_type"])
        layout.addWidget(timer_type)
        
        # 时间显示
        self.time_label = QLabel()
        self.update_time_display()
        layout.addWidget(self.time_label)
        
        # 控制按钮
        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.toggle_timer)
        layout.addWidget(self.start_button)
        
        # 删除按钮
        delete_button = QPushButton("删除")
        delete_button.clicked.connect(self.delete_task)
        layout.addWidget(delete_button)
        
    def toggle_timer(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.start_button.setText("暂停")
            if self.task_data["timer_type"] == "正计时":
                self.task_data["start_time"] = datetime.now()
        else:
            self.start_button.setText("开始")
            
    def update_timer(self):
        if self.task_data["timer_type"] == "倒计时":
            if self.task_data["duration"] > 0:
                self.task_data["duration"] -= 1
                self.update_time_display()
            else:
                self.is_running = False
                self.start_button.setText("开始")
        else:  # 正计时
            elapsed = (datetime.now() - self.task_data["start_time"]).total_seconds()
            self.update_time_display(elapsed)
            
    def update_time_display(self, elapsed=None):
        if self.task_data["timer_type"] == "倒计时":
            minutes = self.task_data["duration"] // 60
            seconds = self.task_data["duration"] % 60
            self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
        else:
            if elapsed is not None:
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                self.time_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
                
    def delete_task(self):
        self.parent().task_list.takeItem(self.parent().task_list.row(self))

class TaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加任务")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 任务名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("任务名称:"))
        self.task_name = QLineEdit()
        name_layout.addWidget(self.task_name)
        layout.addLayout(name_layout)
        
        # 任务描述
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("任务描述:"))
        self.task_desc = QTextEdit()
        self.task_desc.setMaximumHeight(100)
        desc_layout.addWidget(self.task_desc)
        layout.addLayout(desc_layout)
        
        # 任务优先级
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("优先级:"))
        self.priority = QComboBox()
        self.priority.addItems(["低", "中", "高"])
        priority_layout.addWidget(self.priority)
        layout.addLayout(priority_layout)
        
        # 截止日期
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("截止日期:"))
        self.due_date = QDateEdit()
        self.due_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.due_date)
        layout.addLayout(date_layout)
        
        # 预计番茄数
        tomato_layout = QHBoxLayout()
        tomato_layout.addWidget(QLabel("预计番茄数:"))
        self.tomato_count = QSpinBox()
        self.tomato_count.setRange(1, 20)
        self.tomato_count.setValue(1)
        tomato_layout.addWidget(self.tomato_count)
        layout.addLayout(tomato_layout)
        
        # 任务标签
        tag_layout = QHBoxLayout()
        tag_layout.addWidget(QLabel("任务标签:"))
        self.task_tag = QLineEdit()
        tag_layout.addWidget(self.task_tag)
        layout.addLayout(tag_layout)
        
        # 提醒选项
        self.reminder = QCheckBox("启用提醒")
        layout.addWidget(self.reminder)
        
        # 按钮
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        ok_button.setIcon(ICONS['check'])
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("取消")
        cancel_button.setIcon(ICONS['close'])
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
    def get_task_info(self):
        return {
            'name': self.task_name.text(),
            'description': self.task_desc.toPlainText(),
            'priority': self.priority.currentText(),
            'due_date': self.due_date.date(),
            'tomato_count': self.tomato_count.value(),
            'tag': self.task_tag.text(),
            'reminder': self.reminder.isChecked(),
            'color': QColor(COLORS['primary'])
        } 