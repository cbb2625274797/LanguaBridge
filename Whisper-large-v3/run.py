import whisper


def transcribe_audio(file_path, language=None, translate=False):
    # 加载模型
    model = whisper.load_model(
        name="large",  # 模型名称（如 base/small/medium/large）
        download_root="../Whisper-large-v3"  # 自定义模型存放路径
    )

    # 执行转录
    result = model.transcribe(
        file_path,
        verbose=True,
        language=language,
        task="translate" if translate else "transcribe",
        fp16=True,                  # GPU 加速（CPU 需设为 False）
        no_speech_threshold=0.5  # 跳过静音部分
    )

    # 输出结果
    print("Text:", result["text"])
    print("\nSegments:")
    for segment in result["segments"]:
        print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")

    return result


# 使用示例
if __name__ == "__main__":
    transcribe_audio("/temp/htdemucs/extracted_audio/vocals.mp3", translate=True)
