import json
import shutil
import threading
import time
from io import BytesIO
import os
import requests
from pydub import AudioSegment

url = "http://192.168.31.3:9880"


def post(refer_wav_path, refer_wav_text, text):
    # 设置URL和要发送的数据
    data = {
        "refer_wav_path": refer_wav_path,
        "prompt_text": refer_wav_text,
        "prompt_language": "zh",
        "text": text,
        "text_language": "zh"
    }
    json_data = json.dumps(data)
    # print(json_data)

    # 设置请求头，指定内容类型为JSON
    headers = {
        'Content-Type': 'application/json',
    }
    # 发送POST请求
    response = requests.post(url, data=json_data, headers=headers, timeout=10)

    # 检查响应状态码
    if response.status_code == 200:
        # 将响应内容读取为字节流
        audio_stream = BytesIO(response.content)

        # 假设音频流是WAV格式
        audio = AudioSegment.from_wav(audio_stream)
        return audio
    else:
        print("请求失败，状态码:", response.status_code)
        # 处理错误情况
        print(response.text)


def post_v2(
        refer_wav_path,
        refer_wav_text,
        text, top_k: int = 5,
        top_p: float = 1,
        temperature: float = 1,
        speed_factor: float = 1.0
):
    url_v2_tts = 'http://192.168.31.3:9880/tts'
    # 设置URL和要发送的数据
    data = {
        "text": text,  # str.(required) text to be synthesized
        "text_lang": "zh",  # str.(required) language of the text to be synthesized
        "ref_audio_path": refer_wav_path,  # str.(required) reference audio path.
        "prompt_text": refer_wav_text,  # str.(optional) prompt text for the reference audio
        "prompt_lang": "zh",  # str.(required) language of the prompt text for the reference audio
        "top_k": top_k,  # int.(optional) top k sampling
        "top_p": top_p,  # float.(optional) top p sampling
        "temperature": temperature,  # float.(optional) temperature for sampling
        "text_split_method": "cut5",  # str.(optional) text split method, see text_segmentation_method.py for details.
        "batch_size": 6,  # int.(optional) batch size for inference
        "batch_threshold": 0.75,  # float.(optional) threshold for batch splitting.
        "split_bucket": True,  # bool.(optional) whether to split the batch into multiple buckets.
        "speed_factor": speed_factor,  # float.(optional) control the speed of the synthesized audio.
        "fragment_interval": 0.3,  # float.(optional) to control the interval of the audio fragment.
        "seed": -1,  # int.(optional) random seed for reproducibility.
        "media_type": "wav",  # str.(optional) media type of the output audio, support "wav", "raw", "ogg", "aac".
        "streaming_mode": False,  # bool.(optional) whether to return a streaming response.
    }
    json_data = json.dumps(data)
    # print(json_data)

    # 设置请求头，指定内容类型为JSON
    headers = {
        'Content-Type': 'application/json',
    }
    # 发送POST请求
    response = requests.post(url_v2_tts, data=json_data, headers=headers, timeout=99)

    # 检查响应状态码
    if response.status_code == 200:
        # 将响应内容读取为字节流
        audio_stream = BytesIO(response.content)

        # 假设音频流是WAV格式
        audio = AudioSegment.from_wav(audio_stream)
        return audio
    else:
        print("请求失败，状态码:", response.status_code)
        # 处理错误情况
        print(response.text)


def commanmd(command: str):
    if command == "exit":
        url_command = url + "/control?command=exit"
    elif command == "restart":
        url_command = url + "/control?command=restart"
        print("等待重启...")
    else:
        url_command = url + "/control?command=??"
        print("未知命令")
    try:
        # 发送GET请求
        response = requests.get(url_command)
    except Exception:
        pass
    time.sleep(12)
    if command == "restart":
        print("重启成功")
    elif command == "exit":
        print("无法运行时退出！")


def get_audio_file(text_results, translated_results):
    # 确保输出目录存在
    output_path = os.path.abspath(f"./temp/translated_segment")
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    for i in range(len(text_results['segments'])):
        audio = post_v2(
            refer_wav_path=os.path.abspath(f"./temp/origin_segment/{text_results['segments'][i]['start']:.2f}.mp3"),
            refer_wav_text=text_results['segments'][i]['text'],
            text=translated_results['segments'][i]['text']
        )

        print(os.path.abspath(f"./temp/translated_segment/{text_results['segments'][i]['start']:.2f}.wav"))
        audio.export(f"./temp/translated_segment/{text_results['segments'][i]['start']:.2f}_{text_results['segments'][i]['end']:.2f}.wav", format="wav")


if __name__ == '__main__':
    audio1 = post_v2("G:/translate/temp/origin_segment/7.12.mp3",
                     "So for the last few days,",
                     "你好，请问你是谁？")
    # audio1 = post("EmotionEngine/EmotionList/paimon/开心.wav",
    #               "要不，我们两个也去看看吧，如果能帮上忙，就可以更早吃上万民堂的料理了",
    #               "请确保你的POST请求返回的是有效的音频流数据，并且你正确处理了任何潜在的错误或异常。")
    # 将WAV转换为MP3并保存
    audio1.export("./temp/post.mp3", format="mp3")
    print("音频流已保存为 post.mp3")

    exit(0)

    set_character(4)

    exit(0)
    my_dict = {
        "开心": "嗯，能有一个让我暂时安身的地方，我很开心。",
        "害怕": "恐怕那时候的他就已经受了碎神之力的影响。",
        "生气": "要是天目幽野正在无差别，行凶不赶快阻止他，还有更多人会遭遇同样的不幸。",
        "失落": "说的也是，感谢各位的关心。幸好这些事对我而言都是过去了。",
        "好奇": "此事的讨论先告一段落，你们两位为什么会找到这里来？",
        "戏谑": "大姐头，对这种事情恐怕是毫无兴趣，我便想着不如请你来体会一番。"
    }
    # 将字典保存到JSON文件中
    with open('../EmotionEngine/EmotionList/wanye/情绪参考文本.json', 'w') as f:
        json.dump(my_dict, f)
    exit(0)
