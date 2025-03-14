import wave
import struct
import math
import os

def generate_notification_sound():
    # 创建sounds目录（如果不存在）
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
    
    # 设置音频参数
    duration = 0.5  # 持续时间（秒）
    sample_rate = 44100  # 采样率
    amplitude = 32767  # 振幅
    
    # 定义多个频率（使用和弦）
    frequencies = [
        523.25,  # C5
        659.25,  # E5
        783.99   # G5
    ]
    
    # 创建WAV文件
    with wave.open('sounds/notification.wav', 'w') as wav_file:
        # 设置参数
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 2字节采样
        wav_file.setframerate(sample_rate)
        
        # 生成音频数据
        for i in range(int(duration * sample_rate)):
            # 组合多个频率
            value = 0
            for freq in frequencies:
                # 使用正弦波作为基础
                sine = math.sin(2 * math.pi * freq * i / sample_rate)
                # 添加一些谐波
                harmonics = 0.5 * math.sin(4 * math.pi * freq * i / sample_rate) + \
                           0.25 * math.sin(6 * math.pi * freq * i / sample_rate)
                value += sine + harmonics
            
            # 归一化
            value = value / len(frequencies)
            
            # 添加淡入淡出效果
            fade_in = min(1.0, i / (0.1 * sample_rate))  # 0.1秒淡入
            fade_out = 1.0 - (i / (duration * sample_rate))  # 淡出
            fade = fade_in * fade_out
            
            # 应用淡入淡出并调整音量
            value = int(amplitude * value * fade)
            
            # 写入数据
            data = struct.pack('<h', value)
            wav_file.writeframes(data)

if __name__ == '__main__':
    generate_notification_sound()
    print("提示音文件已生成：sounds/notification.wav") 