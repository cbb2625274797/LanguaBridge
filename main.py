import audio_process
import asr_whisper as asr
from LLM import ollama
import translator
import GPT_SoVits as sovits

if __name__ == "__main__":
    # 使用示例
    input_video = "./temp/test2.mp4"  # 替换为你的视频路径
    output_audio = "./temp/extracted_audio.mp3"  # 输出音频路径

    # 翻译大模型初始化
    translator_LLM = ollama.translator()

    audio_process.extract_audio_from_video(input_video, output_audio)  # 分离视频音频
    audio_process.extract_vocals(output_audio, "./temp")  # 分离人声与背景音

    text_results = asr.transcribe_audio("./temp/htdemucs/extracted_audio/vocals.wav", translate=True)  # 音频识别
    text_results = asr.merge_with_stop(text_results)  # 按句逗分割
    text_results = asr.merge_by_time(text_results)  # 按时间分割

    audio_process.extract_audio_segment("./temp/htdemucs/extracted_audio/vocals.wav", text_results,
                                        "./temp/origin_segment")  # 分割音频
    translator_results = translator.translate_text(translator_LLM, text_results)  # 大模型翻译
    sovits.get_audio_file(text_results, translator_results)  # 语音生成
    audio_process.insert_audios("./temp/translation.wav", "./temp/translated_segment/")
