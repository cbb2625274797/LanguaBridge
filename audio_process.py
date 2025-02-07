import shutil
import struct
import subprocess
import wave

from moviepy import VideoFileClip, AudioFileClip


def extract_audio_from_video(video_path, output_audio_path):
    """
    从视频文件中提取音频并保存为独立文件
    :param video_path: 输入视频文件路径
    :param output_audio_path: 输出音频文件路径
    """
    # 加载视频文件
    video = VideoFileClip(video_path)

    print("从视频分离音频中...")
    # 提取音频轨道
    audio = video.audio

    # 保存音频文件
    audio.write_audiofile(output_audio_path)

    # 关闭资源
    audio.close()
    video.close()

    print(f"音频已成功分离到 {os.path.abspath(output_audio_path)}")


def extract_vocals(audio_file, output_dir):
    # 使用-o参数指定输出目录
    command = ["demucs", "--two-stems=vocals", "-o", output_dir, audio_file]
    print("提取人声中...")
    subprocess.run(command)


def create_silent_wav(output_path, duration=5, sample_rate=44100, channels=2):
    """
    生成指定时长的空白 WAV 音频
    :param output_path: 输出文件路径 (.wav)
    :param duration: 音频时长 (秒)
    :param sample_rate: 采样率 (默认 44100 Hz)
    :param channels: 声道数 (1=单声道, 2=立体声)
    """
    num_frames = int(duration * sample_rate)

    # 创建全零数据 (静音)
    silent_data = struct.pack("<" + "h" * num_frames * channels, *(0 for _ in range(num_frames * channels)))

    with wave.open(output_path, "wb") as f:
        f.setnchannels(channels)  # 声道数
        f.setsampwidth(2)  # 采样位宽 (2 bytes = 16-bit)
        f.setframerate(sample_rate)  # 采样率
        f.writeframes(silent_data)  # 写入静音数据


def extract_audio_segment(audio_path, text_results, output_path, ):
    """
    根据给定的起始时间和持续时间从音频文件中提取一段切片。

    :param audio_path: 原始音频文件路径
    :param text_results: 识别字符串
    :param output_path: 输出切片音频文件路径
    """
    # 确保输出目录存在
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)
    # 加载音频文件
    audio = AudioSegment.from_file(audio_path)

    print("音频分割中...")
    for segment in text_results["segments"]:
        # 根据给定的起始时间和持续时间提取音频片段
        audio_segment = audio[segment['start'] * 1000:segment['end'] * 1000]
        audio_segment.export(os.path.join(output_path, f"{segment['start']:.2f}.mp3"), format="mp3")
    print("音频片段已导出到指定目录。")


from pydub import AudioSegment
import os


def load_audio(file_path):
    """根据文件扩展名加载音频文件"""
    if file_path.endswith('.mp3'):
        return AudioSegment.from_mp3(file_path)
    elif file_path.endswith('.wav'):
        return AudioSegment.from_wav(file_path)
    else:
        raise ValueError(f"Unsupported audio format: {file_path}")


def split_filename(filename):
    # 去掉文件扩展名
    name_without_extension = os.path.splitext(filename)[0]

    # 使用下划线分割字符串
    parts = name_without_extension.split('_')

    if len(parts) != 2:
        raise ValueError("文件名格式不正确，应包含两个用下划线分隔的数字")

    try:
        start_time = float(parts[0]) * 1000
        end_time = float(parts[1]) * 1000
    except ValueError as e:
        raise ValueError(f"文件名中的时间戳格式不正确: {e}")

    return start_time, end_time


def adjust_audio_speed(audio_path, target_duration_ms):
    """
    调整音频速度以匹配目标时长
    :param audio_path: 输入音频文件路径
    :param target_duration_ms: 目标时长（毫秒）
    """
    # 加载音频文件
    audio = AudioSegment.from_file(audio_path)
    # 获取当前音频时长（毫秒）
    current_duration_ms = len(audio)
    # 计算需要的播放速度
    speed_factor = current_duration_ms / target_duration_ms

    # 如果当前音频时长小于或等于目标时长，则无需调整
    if current_duration_ms <= target_duration_ms:
        return audio
    else:
        print("调整音频速度为" + str(speed_factor))
        pass

    # 调整音频速度
    adjusted_audio = audio.speedup(playback_speed=speed_factor)

    return adjusted_audio


def insert_audios(main_audio_path, insert_dir):
    # 根据文件扩展名加载主音频文件
    main_audio = load_audio(main_audio_path)

    for file_name in os.listdir(insert_dir):
        if file_name.endswith((".mp3", ".wav")):  # 支持mp3和wav格式
            try:
                start_time, end_time = split_filename(file_name)
                insert_audio = adjust_audio_speed(insert_dir + file_name, end_time - start_time)  # 调整插入音频的速度以匹配目标时长

                # 确保插入位置不超过主音频长度
                if start_time > len(main_audio):
                    print(f"警告：插入时间 {start_time} 超过主音频长度 {len(main_audio)}")
                    continue

                # 计算需要替换的长度，并进行替换
                main_audio = main_audio[:start_time] + insert_audio + main_audio[start_time + len(insert_audio):]
            except ValueError as e:
                print(f"处理文件 '{file_name}' 时出错: {e}")

    # 导出处理后的音频
    output_format = os.path.splitext(main_audio_path)[1][1:]  # 获取输入文件的格式
    main_audio.export("./temp/translation." + output_format, format=output_format)


def merge_audio_video(video_path, audio_path, output_path):
    # 加载视频和音频文件
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # 如果音频长度与视频不匹配，调整音频长度以匹配视频
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)
    elif audio.duration < video.duration:
        # 若音频较短，可以选择循环播放或静音延长。这里选择静音延长作为示例。
        audio = audio.set_duration(video.duration)

    # 将音频设置到视频中
    final_clip = video.set_audio(audio)

    # 导出最终的视频文件
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')


if __name__ == "__main__":
    # create_silent_wav(output_path="./temp/translation.wav",
    #                   duration=600, )
    # 使用示例
    main_audio_path = "./temp/translation.wav"
    insert_dir = "./temp/translated_segment/"
    insert_audios(main_audio_path, insert_dir)
