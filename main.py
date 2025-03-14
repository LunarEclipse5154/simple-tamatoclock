import sys
import os
# 设置环境变量来隐藏 FFmpeg 调试信息
os.environ['QT_LOGGING_RULES'] = 'qt.multimedia.ffmpeg=false'

from PyQt6.QtWidgets import QApplication

# 首先创建 QApplication 实例
app = QApplication(sys.argv)

# 然后导入其他依赖
from PyQt6.QtWidgets import (QMainWindow, QStackedWidget, 
                           QWidget, QVBoxLayout, QPushButton, QHBoxLayout,
                           QComboBox, QSystemTrayIcon, QMenu)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon
from main_timer import MainTimerWidget
from task_list import TaskListWidget
from user_profile import UserProfileWidget
from models import Session, User, Statistics
from translations import translations
from themes import themes
from styles import apply_style, ICONS

# 应用全局样式
apply_style(app)

class TomatoClock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.current_user = None
        self.current_language = 'zh_CN'
        self.current_theme = 'light'
        
        self.init_ui()
        self.setup_tray()
        self.load_user()
        
    def init_ui(self):
        self.setWindowTitle(self.get_text('timer', 'title'))
        self.setMinimumSize(800, 600)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QVBoxLayout(main_widget)
        
        # 创建顶部工具栏
        toolbar_layout = QHBoxLayout()
        layout.addLayout(toolbar_layout)
        
        # 创建语言选择器
        self.language_combo = QComboBox()
        self.language_combo.addItems(['中文', 'English'])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        toolbar_layout.addWidget(self.language_combo)
        
        # 创建主题选择器
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['浅色', '深色', '蓝色'])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        toolbar_layout.addWidget(self.theme_combo)
        
        # 创建堆叠窗口部件
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # 创建导航按钮布局
        nav_layout = QHBoxLayout()
        layout.addLayout(nav_layout)
        
        # 创建各个页面
        self.main_timer = MainTimerWidget(self)
        self.task_list = TaskListWidget(self)
        self.user_profile = UserProfileWidget(self)
        
        # 添加页面到堆叠窗口
        self.stacked_widget.addWidget(self.main_timer)
        self.stacked_widget.addWidget(self.task_list)
        self.stacked_widget.addWidget(self.user_profile)
        
        # 创建导航按钮
        self.timer_btn = QPushButton(self.get_text('timer', 'title'))
        self.timer_btn.setIcon(ICONS['timer'])
        self.timer_btn.setIconSize(QSize(24, 24))
        self.task_btn = QPushButton(self.get_text('task_list', 'title'))
        self.task_btn.setIcon(ICONS['task'])
        self.task_btn.setIconSize(QSize(24, 24))
        self.profile_btn = QPushButton(self.get_text('user_profile', 'title'))
        self.profile_btn.setIcon(ICONS['user'])
        self.profile_btn.setIconSize(QSize(24, 24))
        
        # 添加按钮到导航布局
        nav_layout.addWidget(self.timer_btn)
        nav_layout.addWidget(self.task_btn)
        nav_layout.addWidget(self.profile_btn)
        
        # 连接按钮信号
        self.timer_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.task_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.profile_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        # 应用当前主题
        self.apply_theme()
        
    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(ICONS['timer'])
        
        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = tray_menu.addAction("显示")
        show_action.setIcon(ICONS['user'])
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("退出")
        quit_action.setIcon(ICONS['close'])
        quit_action.triggered.connect(self.quit_application)
        self.tray_icon.setContextMenu(tray_menu)
        
    def load_user(self):
        # 这里应该实现用户登录逻辑
        # 暂时使用默认用户
        self.current_user = self.session.query(User).first()
        if not self.current_user:
            self.current_user = User(username="default", email="default@example.com")
            self.session.add(self.current_user)
            self.session.commit()
            
    def get_text(self, section, key):
        return translations[self.current_language][section][key]
        
    def change_language(self, index):
        languages = ['zh_CN', 'en_US']
        self.current_language = languages[index]
        self.update_texts()
        
    def change_theme(self, index):
        themes_list = ['light', 'dark', 'blue']
        self.current_theme = themes_list[index]
        self.apply_theme()
        
    def apply_theme(self):
        theme = themes[self.current_theme]
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme['background']};
                color: {theme['text']};
            }}
            QPushButton {{
                background-color: {theme['button']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                padding: 5px;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
            }}
            QLabel {{
                color: {theme['text']};
            }}
            QSpinBox {{
                background-color: {theme['background']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
            }}
            QLineEdit {{
                background-color: {theme['background']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
            }}
            QListWidget {{
                background-color: {theme['background']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
            }}
        """)
        
    def update_texts(self):
        self.setWindowTitle(self.get_text('timer', 'title'))
        self.timer_btn.setText(self.get_text('timer', 'title'))
        self.task_btn.setText(self.get_text('task_list', 'title'))
        self.profile_btn.setText(self.get_text('user_profile', 'title'))
        
    def quit_application(self):
        self.session.close()
        QApplication.quit()

if __name__ == '__main__':
    window = TomatoClock()
    window.show()
    sys.exit(app.exec()) 