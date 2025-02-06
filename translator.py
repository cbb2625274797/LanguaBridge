import copy


def translate_text(translator_LLM,text_results):
    """
    :param translator_LLM: 大模型实例
    :param text_results: 识别英文字符串
    :return: 翻译后中文字符串
    """
    translator_results = copy.deepcopy(text_results)
    for segment in translator_results["segments"]:
        segment['text'] = translator_LLM.translate_text(segment['text'])  # 调用翻译方法并保存

    print("\n翻译后:")
    for segment in translator_results["segments"]:
        print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")
    print("————————————————————————————————————————————————————————————————————————————")

    return translator_results
