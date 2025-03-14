from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtCore import Qt
import qtawesome as qta

# 定义图标
ICONS = {
    'timer': qta.icon('fa5s.clock'),
    'play': qta.icon('fa5s.play'),
    'pause': qta.icon('fa5s.pause'),
    'refresh': qta.icon('fa5s.sync'),
    'settings': qta.icon('fa5s.cog'),
    'add': qta.icon('fa5s.plus'),
    'delete': qta.icon('fa5s.trash'),
    'check': qta.icon('fa5s.check'),
    'close': qta.icon('fa5s.times'),
    'save': qta.icon('fa5s.save'),
    'user': qta.icon('fa5s.user'),
    'task': qta.icon('fa5s.tasks'),
    'chart': qta.icon('fa5s.chart-bar'),
    'trophy': qta.icon('fa5s.trophy'),
    'bell': qta.icon('fa5s.bell'),
    'calendar': qta.icon('fa5s.calendar'),
    'star': qta.icon('fa5s.star'),
    'medal': qta.icon('fa5s.medal'),
    'target': qta.icon('fa5s.bullseye'),
    'fire': qta.icon('fa5s.fire'),
    'heart': qta.icon('fa5s.heart'),
    'lightbulb': qta.icon('fa5s.lightbulb'),
    'rocket': qta.icon('fa5s.rocket'),
    'crown': qta.icon('fa5s.crown'),
    'gem': qta.icon('fa5s.gem'),
    'award': qta.icon('fa5s.award')
}

# 定义颜色
COLORS = {
    'primary': '#4CAF50',
    'primary_dark': '#388E3C',
    'primary_light': '#81C784',
    'accent': '#FFC107',
    'accent_dark': '#FFA000',
    'accent_light': '#FFD54F',
    'success': '#4CAF50',
    'warning': '#FFC107',
    'error': '#F44336',
    'info': '#2196F3',
    'text': '#333333',
    'text_light': '#666666',
    'background': '#FFFFFF',
    'background_dark': '#F5F5F5',
    'border': '#E0E0E0',
    'button': '#E0E0E0',
    'button_hover': '#D0D0D0'
}

# 定义全局样式表
STYLE_SHEET = f"""
    QMainWindow {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}
    
    QPushButton {{
        background-color: {COLORS['button']};
        color: {COLORS['text']};
        border: 1px solid {COLORS['border']};
        padding: 8px 16px;
        border-radius: 4px;
        font-size: 14px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['button_hover']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['primary_light']};
    }}
    
    QLabel {{
        color: {COLORS['text']};
    }}
    
    QSpinBox {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
        border: 1px solid {COLORS['border']};
        padding: 4px;
        border-radius: 4px;
    }}
    
    QLineEdit {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
        border: 1px solid {COLORS['border']};
        padding: 4px;
        border-radius: 4px;
    }}
    
    QListWidget {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
    }}
    
    QListWidget::item {{
        padding: 8px;
    }}
    
    QListWidget::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['text']};
    }}
    
    QComboBox {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
        border: 1px solid {COLORS['border']};
        padding: 4px;
        border-radius: 4px;
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox::down-arrow {{
        image: url(down_arrow.png);
        width: 12px;
        height: 12px;
    }}
    
    QProgressBar {{
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        text-align: center;
        background-color: {COLORS['background']};
    }}
    
    QProgressBar::chunk {{
        background-color: {COLORS['primary']};
        border-radius: 3px;
    }}
    
    QFrame {{
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
    }}
"""

def apply_style(app):
    """应用全局样式到应用程序"""
    app.setStyleSheet(STYLE_SHEET)
    app.setWindowIcon(ICONS['timer']) 