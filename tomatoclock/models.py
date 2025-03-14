from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    daily_goal = Column(Integer, default=480)  # 默认8小时
    created_at = Column(DateTime, default=datetime.now)
    
    statistics = relationship("Statistics", back_populates="user", uselist=False)
    tasks = relationship("Task", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")

class Statistics(Base):
    __tablename__ = 'statistics'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_pomodoros = Column(Integer, default=0)
    total_focus_time = Column(Integer, default=0)  # 总专注时间（分钟）
    daily_focus_time = Column(Integer, default=0)  # 今日专注时间（分钟）
    streak = Column(Integer, default=0)  # 连续使用天数
    current_streak = Column(Integer, default=0)  # 当前连续完成番茄钟数
    last_active_date = Column(DateTime)
    
    user = relationship("User", back_populates="statistics")
    
    def get_daily_focus_time(self, date):
        # 这里应该从数据库获取指定日期的专注时间
        # 暂时返回当前日期的专注时间
        if date == datetime.now().strftime('%m-%d'):
            return self.daily_focus_time
        return 0
        
    def get_daily_pomodoros(self, date):
        # 这里应该从数据库获取指定日期的番茄钟数量
        # 暂时返回当前日期的番茄钟数量
        if date == datetime.now().strftime('%m-%d'):
            return self.total_pomodoros
        return 0

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String(200), nullable=False)
    color = Column(String(7), default="#FF6B6B")  # 任务标签颜色
    timer_type = Column(String(10), default="倒计时")  # 倒计时或正计时
    duration = Column(Integer, default=0)  # 倒计时时长（秒）
    is_running = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    
    user = relationship("User", back_populates="tasks")

class Achievement(Base):
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    icon = Column(String(10))
    unlocked_at = Column(DateTime)
    
    user = relationship("User", back_populates="achievements")

# 创建数据库引擎
engine = create_engine('sqlite:///tomato_clock.db')
Base.metadata.create_all(engine)

# 创建会话工厂
Session = sessionmaker(bind=engine) 