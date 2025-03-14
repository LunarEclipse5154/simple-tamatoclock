from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QLineEdit, QSpinBox, QFormLayout, QProgressBar,
                           QGridLayout, QFrame, QComboBox, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from models import Statistics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta
import numpy as np
from styles import ICONS, COLORS

class UserProfileWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 创建内容容器
        content_widget = QWidget()
        content_widget.setMinimumWidth(600)  # 设置最小宽度
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("用户资料")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Microsoft YaHei', 24, QFont.Weight.Bold))
        content_layout.addWidget(title)
        
        # 用户信息部分
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(15)
        
        # 用户名
        username_layout = QHBoxLayout()
        username_label = QLabel("用户名:")
        username_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont('Microsoft YaHei', 12))
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        info_layout.addLayout(username_layout)
        
        # 邮箱
        email_layout = QHBoxLayout()
        email_label = QLabel("邮箱:")
        email_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        self.email_input = QLineEdit()
        self.email_input.setFont(QFont('Microsoft YaHei', 12))
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        info_layout.addLayout(email_layout)
        
        # 主题选择
        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题:")
        theme_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        self.theme_combo = QComboBox()
        self.theme_combo.setFont(QFont('Microsoft YaHei', 12))
        self.theme_combo.addItems(['浅色', '深色', '蓝色'])
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        info_layout.addLayout(theme_layout)
        
        content_layout.addWidget(info_frame)
        
        # 统计信息部分
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        stats_layout = QVBoxLayout(stats_frame)
        stats_layout.setSpacing(15)
        
        # 统计标题
        stats_title = QLabel("统计信息")
        stats_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_title.setFont(QFont('Microsoft YaHei', 16, QFont.Weight.Bold))
        stats_layout.addWidget(stats_title)
        
        # 总番茄数
        tomatoes_layout = QHBoxLayout()
        tomatoes_label = QLabel("总番茄数:")
        tomatoes_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        self.tomatoes_count = QLabel("0")
        self.tomatoes_count.setFont(QFont('Microsoft YaHei', 12))
        tomatoes_layout.addWidget(tomatoes_label)
        tomatoes_layout.addWidget(self.tomatoes_count)
        stats_layout.addLayout(tomatoes_layout)
        
        # 总专注时间
        focus_layout = QHBoxLayout()
        focus_label = QLabel("总专注时间:")
        focus_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        self.focus_time = QLabel("0 分钟")
        self.focus_time.setFont(QFont('Microsoft YaHei', 12))
        focus_layout.addWidget(focus_label)
        focus_layout.addWidget(self.focus_time)
        stats_layout.addLayout(focus_layout)
        
        content_layout.addWidget(stats_frame)
        
        # 成就部分
        achievements_frame = QFrame()
        achievements_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        achievements_layout = QVBoxLayout(achievements_frame)
        achievements_layout.setSpacing(15)
        
        # 成就标题
        achievements_title = QLabel("成就")
        achievements_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        achievements_title.setFont(QFont('Microsoft YaHei', 16, QFont.Weight.Bold))
        achievements_layout.addWidget(achievements_title)
        
        # 成就列表容器
        achievements_container = QWidget()
        achievements_container.setMinimumHeight(300)  # 设置最小高度
        self.achievements_list = QVBoxLayout(achievements_container)
        self.achievements_list.setSpacing(10)
        achievements_layout.addWidget(achievements_container)
        
        content_layout.addWidget(achievements_frame)
        
        # 按钮部分
        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        save_btn.setIcon(ICONS['save'])
        save_btn.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        save_btn.clicked.connect(self.save_profile)
        reset_btn = QPushButton("重置")
        reset_btn.setIcon(ICONS['refresh'])
        reset_btn.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        reset_btn.clicked.connect(self.reset_profile)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        content_layout.addLayout(button_layout)
        
        # 设置滚动区域的内容
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # 加载用户数据
        self.load_user_data()
        # 立即更新成就显示
        self.update_achievements()
        
    def load_user_data(self):
        if self.parent and self.parent.current_user:
            self.username_input.setText(self.parent.current_user.username)
            self.email_input.setText(self.parent.current_user.email)
            self.update_stats_display()
            
    def update_stats_display(self):
        if self.parent and self.parent.current_user:
            stats = self.parent.current_user.statistics
            if stats:
                self.tomatoes_count.setText(str(stats.total_tomatoes))
                self.focus_time.setText(f"{stats.focus_time} 分钟")
                
    def update_achievements(self):
        # 清除现有成就
        while self.achievements_list.count():
            item = self.achievements_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # 添加成就
        achievements = [
            ("专注新手", "完成第一个番茄", ICONS['star']),
            ("专注达人", "累计专注时间超过100分钟", ICONS['trophy']),
            ("任务完成者", "完成10个任务", ICONS['check']),
            ("坚持不懈", "连续7天使用番茄时钟", ICONS['fire']),
            ("时间管理大师", "累计专注时间超过1000分钟", ICONS['crown'])
        ]
        
        for title, desc, icon in achievements:
            achievement_widget = QFrame()
            achievement_widget.setFrameStyle(QFrame.Shape.StyledPanel)
            achievement_layout = QHBoxLayout(achievement_widget)
            achievement_layout.setContentsMargins(15, 10, 15, 10)
            achievement_layout.setSpacing(15)
            
            icon_label = QLabel()
            icon_label.setPixmap(icon.pixmap(32, 32))
            achievement_layout.addWidget(icon_label)
            
            text_layout = QVBoxLayout()
            title_label = QLabel(title)
            title_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
            desc_label = QLabel(desc)
            desc_label.setFont(QFont('Microsoft YaHei', 10))
            desc_label.setWordWrap(True)
            text_layout.addWidget(title_label)
            text_layout.addWidget(desc_label)
            achievement_layout.addLayout(text_layout)
            
            self.achievements_list.addWidget(achievement_widget)
            
    def save_profile(self):
        if self.parent and self.parent.current_user:
            self.parent.current_user.username = self.username_input.text()
            self.parent.current_user.email = self.email_input.text()
            self.parent.session.commit()
            QMessageBox.information(self, "成功", "用户资料已保存")
            
    def reset_profile(self):
        self.load_user_data()
        QMessageBox.information(self, "成功", "用户资料已重置") 