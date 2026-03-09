import sys
import queue
import sherpa_onnx
import sounddevice as sd
import numpy as np
import re

sys.path.append("/home/zpr/glove_ai")

from nlp.command_parser import parse_command
from tts.speech_play import speak

def remove_repetition(text):

    # 1️⃣ 去除连续字符重复，例如：哈哈哈 -> 哈
    text = re.sub(r'(.)\1{1,}', r'\1', text)

    # 2️⃣ 去除连续词重复，例如：电视电视 -> 电视
    text = re.sub(r'(.{2,})\1+', r'\1', text)

    return text


def main():
    # === 麦克风配置 ===
    MIC_SAMPLE_RATE = 48000
    MIC_DEVICE_ID = 11

    # === 模型路径 ===
    base_path = "./model_zipformer"

    tokens = f"{base_path}/tokens.txt"
    encoder = f"{base_path}/encoder-epoch-99-avg-1.int8.onnx"
    decoder = f"{base_path}/decoder-epoch-99-avg-1.int8.onnx"
    joiner = f"{base_path}/joiner-epoch-99-avg-1.int8.onnx"

    print("正在初始化模型 (CPU 4核全开模式)...")

    try:
        recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
            tokens=tokens,
            encoder=encoder,
            decoder=decoder,
            joiner=joiner,

            hotwords_file="hotwords.txt",
            hotwords_score=1.5,

            num_threads=4,
            provider="cpu",

            sample_rate=16000,
            feature_dim=80,

            decoding_method="modified_beam_search",
            max_active_paths=2,

            # 语音结束规则
            rule2_min_trailing_silence=0.4,
            rule3_min_utterance_length=8.0
        )

    except Exception as e:
        print(f"\n❌ 模型加载失败: {e}")
        return

    # 队列
    audio_queue = queue.Queue(maxsize=50)

    def callback(indata, frames, time, status):
        if status:
            pass

        try:
            audio_queue.put_nowait(bytes(indata))
        except queue.Full:
            pass

    print("\n========================================")
    print("🎤 语音识别启动 (缓冲模式，录制率: 48000Hz -> 模型: 16000Hz)")
    print("   请对着麦克风说话... (按 Ctrl+C 退出)")
    print("========================================\n")

    stream = recognizer.create_stream()

    last_text = ""
    same_result_count = 0  # 记录相同识别结果的次数
    consecutive_frames = 0  # 记录连续帧数

    try:

        NOISE_THRESHOLD = 0.02

        with sd.InputStream(
            channels=1,
            dtype="float32",
            samplerate=MIC_SAMPLE_RATE,
            callback=callback,
            device=MIC_DEVICE_ID,
        ):

            while True:

                audio_data_bytes = audio_queue.get()

                samples = np.frombuffer(audio_data_bytes, dtype=np.float32)

                volume = np.max(np.abs(samples))

                # 静音过滤
                if volume < NOISE_THRESHOLD:
                    continue

                stream.accept_waveform(MIC_SAMPLE_RATE, samples)

                while recognizer.is_ready(stream):

                    recognizer.decode_stream(stream)

                    result = recognizer.get_result(stream)
                    is_endpoint = recognizer.is_endpoint(stream)

                    # 检查是否有结果
                    if result:
                        text = result.strip()

                        if len(text) < 2:
                            consecutive_frames = 0
                            continue

                        text = remove_repetition(text)

                        # 检查识别结果是否更新
                        if text != last_text:
                            # 新的识别结果，显示它
                            display_text = text[-25:]
                            sys.stdout.write(f"\r\033[2K👂: {display_text}")
                            sys.stdout.flush()
                            last_text = text
                            same_result_count = 0
                            consecutive_frames = 0
                        else:
                            # 识别结果没有变化，计数增加
                            same_result_count += 1
                            consecutive_frames += 1

                        # 当连续3次获得相同结果或 is_endpoint 为真时，认为识别完成
                        if (same_result_count >= 3 or is_endpoint) and last_text:
                            sys.stdout.write(f"\r\033[2K✅: {last_text}\n")
                            sys.stdout.flush()

                            print(f"[DEBUG] 触发条件: same_result_count={same_result_count}, is_endpoint={is_endpoint}")

                            # === 调用 glove 语义解析 ===
                            action, device, value = parse_command(last_text)
                            
                            print(f"[DEBUG] 解析结果: action={action}, device={device}, value={value}")

                            if action == "open" and device == "air_conditioner":
                                if value:
                                    message = f"空调已经打开到{value}度"
                                else:
                                    message = "空调已经打开"

                                print("🤖:", message)
                                speak(message)

                            # 重置流和状态，准备下一句
                            recognizer.reset(stream)
                            last_text = ""
                            same_result_count = 0
                            consecutive_frames = 0
                    else:
                        consecutive_frames = 0

    except Exception as e:
        print(f"\n❌ 麦克风错误: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 停止识别")
