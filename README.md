# 视频语音自动中文化工具

本程序实现了将视频中的语音内容自动转换为中文的功能，可生成带中文配音的新视频文件，助力跨语言内容无障碍传播。

## 主要功能
- 🎙️ 语音识别：自动提取视频音频并转写为原文文本
- 🌍 智能翻译：支持多语种翻译（英/日/韩等→中文）
- 🔊 语音合成：生成自然流畅的中文配音音频
- 🎬 视频合成：自动对齐时间轴，保留原视频画面与背景音
- ⚡ 批量处理：支持同时处理多个视频文件

## 快速开始
### 安装依赖
```bash
pip install -r requirements.txt
```
### 需提前安装FFmpeg并加入系统路径

## 基本使用
```yaml
复制
translation:
  source_lang: auto    # 自动检测源语言
  target_lang: zh-CN   # 输出中文
tts:
  voice: "zh-CN-XiaoxiaoNeural"  # 微软Azure语音合成
  speed: 1.1                     # 语速调节
支持格式
输入格式	输出格式	备注
MP4	MP4	推荐H.264编码
MOV	AVI	保留1080p分辨率
MKV	MP4	自动处理字幕流
依赖组件
语音识别：OpenAI Whisper

机器翻译：Google Translate API

语音合成：Microsoft Azure TTS

视频处理：FFmpeg + MoviePy

许可协议
MIT License - 免费用于个人及商业用途，需保留版权声明
