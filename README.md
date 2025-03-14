# simple-tamatoclock
# Tomato Clock

一个简单而功能强大的番茄钟应用程序。

## 运行方式

### 方式一：直接运行（推荐）

1. 下载 `dist` 文件夹中的 `TomatoClock.exe`
2. 双击运行即可

### 方式二：从源码运行

1. 确保已安装 Python 3.8 或更高版本
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行程序：
   ```bash
   python main.py
   ```

## 功能特点

- 番茄钟计时器
- 任务列表管理
- 用户统计和图表展示
- 多语言支持（中文/英文）
- 多主题支持（浅色/深色/蓝色）
- 系统托盘支持

## 注意事项

- 首次运行时会自动创建数据库文件
- 程序会在系统托盘显示图标
- 可以通过系统托盘图标控制程序的显示/隐藏

## 文件结构

- `main.py`: 主程序入口
- `main_timer.py`: 计时器界面
- `task_list.py`: 任务清单界面
- `user_profile.py`: 用户信息界面
- `models.py`: 数据库模型
- `translations.py`: 多语言支持
- `themes.py`: 主题配置
- `icon.svg`: 程序图标
- `sounds/notification.wav`: 提示音文件

## 许可证

MIT License 
