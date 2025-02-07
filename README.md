# 视频语音自动中文化工具

本程序实现了将视频中的语音内容自动转换为中文的功能，可生成带中文配音的新视频文件，助力跨语言内容无障碍传播。

## 主要功能
- 🎙️ 语音识别：自动提取视频音频并转写为原文文本
- 🌍 智能翻译：支持多语种翻译（英/日/韩等→中文）
- 🔊 语音合成：生成自然流畅的中文配音音频
- 🎬 视频合成：自动对齐时间轴，保留原视频画面与背景音

## 快速开始
### 环境要求
- Python>=3.8
- ffmpeg
- torch>=1.13
- torchaudio

**需提前安装[FFmpeg](https://ffmpeg.org//download.html)并加入系统路径**

### 安装基本依赖
```bash
pip install -r requirements.txt
```

### 语音识别模块配置
```bash
pip install -U openai-whisper
```

## 支持格式
| 输入格式 | 输出格式 | 备注       |
|------|------|----------|
| MP4  | MP4  | 推荐 H.264 |

### 依赖组件
语音识别：Whisper V3

机器翻译：Qwen2.5

语音合成：GPT-SoVits

视频处理：FFmpeg + MoviePy

## 许可协议
MIT License - 免费用于个人及商业用途，需保留版权声明
