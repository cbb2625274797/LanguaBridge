import whisper
import FunASR


def transcribe_audio(file_path, language=None, translate=False):
    # 加载模型
    model = whisper.load_model(
        name="large",  # 模型名称（如 base/small/medium/large）
        download_root="./Whisper-large-v3"  # 自定义模型存放路径
    )

    # 执行转录
    result = model.transcribe(
        file_path,
        verbose=True,
        language=language,
        task="translate" if translate else "transcribe",
        fp16=False,  # GPU 加速（CPU 需设为 False）
        no_speech_threshold=0.5  # 跳过静音部分
    )

    # 输出结果
    # print("Text:", result["text"])
    # print("\nSegments:")
    # for segment in result["segments"]:
    #     print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")

    print(result)
    return result


def repeat_fix(text_results):
    """
    :param text_results: 去重前
    :return: text_results: 去重后
    """
    i = 1
    while i < len(text_results["segments"]):
        segments = text_results["segments"]
        if segments[i]["text"] == segments[i - 1]["text"]:
            segments[i - 1]["end"] = segments[i]["end"]
            del text_results["segments"][i]
        else:
            i = i + 1

    print("\n去重后:")
    for segment in text_results["segments"]:
        print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")
    # print(text_results)
    return text_results


def merge_with_stop(text_results):
    merged_text = ""
    start_time = float(text_results["segments"][0]["start"])
    i = 0
    while i < len(text_results["segments"]):
        segment = text_results["segments"]
        merged_text = merged_text + segment[i]["text"]
        # 确保文本以标点符号结尾
        if segment[i]["text"].endswith(".") or segment[i]["text"].endswith("?") or segment[i]["text"].endswith("!") or \
                segment[i]["text"].endswith(","):
            segment[i]['text'] = merged_text
            segment[i]["start"] = start_time

            merged_text = ""
            if i < len(text_results["segments"]) - 1:
                start_time = segment[i + 1]["start"]
            else:
                pass
            i = i + 1
        else:
            # 删除当前 segment
            del text_results["segments"][i]

    print("\n按句逗分割后:")
    for segment in text_results["segments"]:
        print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")
    print(text_results)

    return text_results


def merge_by_time(text_results):
    i = 0
    start = float(text_results["segments"][0]["start"])
    text = ''
    print("\n按时间分割后:")
    while i < len(text_results["segments"]):
        segment = text_results["segments"]
        # 合格
        if float(segment[i]['end']) - start > 3.1:
            segment[i]['text'] = text + segment[i]['text']
            segment[i]['start'] = start
            # 重置文本
            text = ''
            # 起始时间更新
            if i < len(text_results["segments"]) - 1:
                start = float(segment[i + 1]['start'])
            else:
                pass
        elif float(segment[i]['end']) - start < 3.1:
            # 添加文本
            text = text + segment[i]['text']
            if i == len(text_results["segments"]) - 1:
                print("末尾句时长不足，已补全")
                segment[i]['end'] = float(segment[i]['start']) + 3.1
            else:
                # 删除该段落
                del text_results["segments"][i]
                i = i - 1

        if float(segment[i]['end']) - float(segment[i]['start']) > 9.9:
            segment[i]['end'] = float(segment[i]['start']) + 9.9
        i = i + 1

    for segment in text_results["segments"]:
        print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")
    print(text_results)

    return text_results


# 使用示例
if __name__ == "__main__":
    transcribe_audio("/temp/htdemucs/extracted_audio/vocals.mp3", translate=True)
