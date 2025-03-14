from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QSpinBox, QListWidget, QListWidgetItem, QColorDialog,
                           QDialog, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QTime, QUrl, QSize
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtMultimedia import QSoundEffect
import os
from styles import ICONS, COLORS

class MainTimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.remaining_time = 25 * 60  # 默认25分钟
        self.is_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        # 初始化提示音
        self.notification = QSoundEffect()
        sound_path = os.path.join("sounds", "notification.wav")
        if os.path.exists(sound_path):
            self.notification.setSource(QUrl.fromLocalFile(sound_path))
            self.notification.setVolume(1.0)
        
        self.init_ui()
        
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建左右布局
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # 左侧布局（计时器部分）
        left_layout = QVBoxLayout()
        content_layout.addLayout(left_layout)
        
        # 创建计时器显示
        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont("Arial", 72))
        left_layout.addWidget(self.time_label)
        
        # 创建控制按钮布局
        control_layout = QHBoxLayout()
        left_layout.addLayout(control_layout)
        
        # 创建开始/暂停按钮
        self.start_btn = QPushButton()
        self.start_btn.setIcon(ICONS['play'])
        self.start_btn.setIconSize(QSize(32, 32))
        self.start_btn.clicked.connect(self.toggle_timer)
        control_layout.addWidget(self.start_btn)
        
        # 创建重置按钮
        self.reset_btn = QPushButton()
        self.reset_btn.setIcon(ICONS['refresh'])
        self.reset_btn.setIconSize(QSize(32, 32))
        self.reset_btn.clicked.connect(self.reset_timer)
        control_layout.addWidget(self.reset_btn)
        
        # 创建设置按钮
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(ICONS['settings'])
        self.settings_btn.setIconSize(QSize(32, 32))
        self.settings_btn.clicked.connect(self.show_settings)
        control_layout.addWidget(self.settings_btn)
        
        # 创建时间设置布局
        time_layout = QHBoxLayout()
        left_layout.addLayout(time_layout)
        
        # 工作时间设置
        work_layout = QVBoxLayout()
        work_label = QLabel("工作时间")
        work_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.work_spin = QSpinBox()
        self.work_spin.setRange(1, 60)
        self.work_spin.setValue(25)
        self.work_spin.setSuffix(" 分钟")
        work_layout.addWidget(work_label)
        work_layout.addWidget(self.work_spin)
        time_layout.addLayout(work_layout)
        
        # 休息时间设置
        break_layout = QVBoxLayout()
        break_label = QLabel("休息时间")
        break_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 30)
        self.break_spin.setValue(5)
        self.break_spin.setSuffix(" 分钟")
        break_layout.addWidget(break_label)
        break_layout.addWidget(self.break_spin)
        time_layout.addLayout(break_layout)
        
        # 右侧布局（任务清单）
        right_layout = QVBoxLayout()
        content_layout.addLayout(right_layout)
        
        # 任务清单标题
        task_title = QLabel("今日任务")
        task_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        task_title.setFont(QFont('Arial', 16))
        right_layout.addWidget(task_title)
        
        # 任务清单
        self.task_list = QListWidget()
        self.task_list.setMaximumWidth(300)
        right_layout.addWidget(self.task_list)
        
        # 添加任务按钮
        add_task_button = QPushButton("添加任务")
        add_task_button.clicked.connect(self.add_task)
        right_layout.addWidget(add_task_button)
        
        # 添加初始示例任务
        self.add_sample_tasks()
        
        # 更新显示
        self.update_timer_display()
        
    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_display()
        else:
            self.timer.stop()
            self.is_running = False
            self.start_btn.setIcon(ICONS['play'])
            self.update_timer_display()
            QMessageBox.information(self, "计时完成", "时间到！")
            
    def update_timer_display(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")
        
    def toggle_timer(self):
        if self.is_running:
            self.timer.stop()
            self.start_btn.setIcon(ICONS['play'])
        else:
            self.timer.start(1000)  # 每秒更新一次
            self.start_btn.setIcon(ICONS['pause'])
        self.is_running = not self.is_running
        
    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.start_btn.setIcon(ICONS['play'])
        self.remaining_time = self.work_spin.value() * 60
        self.update_timer_display()
        
    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.work_spin.setValue(dialog.work_time.value())
            self.break_spin.setValue(dialog.break_time.value())
            self.reset_timer()
            
    def add_sample_tasks(self):
        sample_tasks = [
            ("完成项目报告", QColor("#FF6B6B")),
            ("代码审查", QColor("#4ECDC4")),
            ("团队会议", QColor("#45B7D1")),
            ("邮件回复", QColor("#96CEB4")),
            ("文档整理", QColor("#FFEEAD"))
        ]
        
        for task_name, color in sample_tasks:
            item = QListWidgetItem(task_name)
            item.setBackground(color)
            self.task_list.addItem(item)
            
    def add_task(self):
        dialog = TaskDialog(self)
        if dialog.exec():
            task_name, color = dialog.get_task_info()
            item = QListWidgetItem(task_name)
            item.setBackground(color)
            self.task_list.addItem(item)
            
            # 同步到任务列表界面
            if self.parent and hasattr(self.parent, 'task_list_widget'):
                self.parent.task_list_widget.add_task(task_name, color)
                
    def update_task_status(self, task_name, completed):
        # 更新主界面的任务状态
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            if item.text() == task_name:
                if completed:
                    item.setBackground(QColor("#90EE90"))  # 浅绿色表示完成
                break
                
    def load_tasks(self):
        # 从任务列表界面加载任务
        if self.parent and hasattr(self.parent, 'task_list_widget'):
            tasks = self.parent.task_list_widget.get_tasks()
            self.task_list.clear()
            for task_name, color in tasks:
                item = QListWidgetItem(task_name)
                item.setBackground(color)
                self.task_list.addItem(item)

class TaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加任务")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # 任务名称输入
        self.task_name = QLineEdit()
        layout.addWidget(QLabel("任务名称:"))
        layout.addWidget(self.task_name)
        
        # 颜色选择
        self.color_button = QPushButton("选择颜色")
        self.color_button.clicked.connect(self.choose_color)
        layout.addWidget(self.color_button)
        
        self.selected_color = QColor("#FF6B6B")  # 默认颜色
        
        # 确定和取消按钮
        buttons = QHBoxLayout()
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        
    def choose_color(self):
        color = QColorDialog.getColor(self.selected_color, self)
        if color.isValid():
            self.selected_color = color
            
    def get_task_info(self):
        return self.task_name.text(), self.selected_color

    def update_statistics(self):
        if self.parent and self.parent.current_user:
            session = self.parent.session
            stats = self.parent.current_user.statistics
            if not stats:
                stats = Statistics(user_id=self.parent.current_user.id)
                session.add(stats)
            
            stats.total_tomatoes += 1
            stats.focus_time += self.work_spin.value()
            session.commit()
            
            # 更新用户界面上的统计信息
            self.parent.user_profile.update_stats_display()

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("设置")
        layout = QVBoxLayout(self)
        
        # 工作时间设置
        work_layout = QHBoxLayout()
        work_label = QLabel("工作时间:")
        self.work_time = QSpinBox()
        self.work_time.setRange(1, 60)
        self.work_time.setValue(25)
        self.work_time.setSuffix(" 分钟")
        work_layout.addWidget(work_label)
        work_layout.addWidget(self.work_time)
        layout.addLayout(work_layout)
        
        # 休息时间设置
        break_layout = QHBoxLayout()
        break_label = QLabel("休息时间:")
        self.break_time = QSpinBox()
        self.break_time.setRange(1, 30)
        self.break_time.setValue(5)
        self.break_time.setSuffix(" 分钟")
        break_layout.addWidget(break_label)
        break_layout.addWidget(self.break_time)
        layout.addLayout(break_layout)
        
        # 确定和取消按钮
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