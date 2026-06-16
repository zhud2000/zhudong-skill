#!/usr/bin/env python3
# [2026-06-16] SenseVoice转写辅助脚本——meeting-minutes SKILL 的语音转文字部分
# [2026-06-16 V1.3] 从 Whisper 迁移至 SenseVoice（国产优先原则）
# 关联影响：SKILL.md 调用此脚本获取转写文本后，自动生成结构化纪要

import sys
from pathlib import Path

WORKSPACE = "C:/Users/zhud2000/Desktop/工作文件/研究院工作区"
MINUTES_DIR = Path(WORKSPACE) / "会议纪要"

def transcribe(audio_path: str) -> str:
    """用 SenseVoice-Small（阿里达摩院）转写中文音频。国产、CPU可用、比Whisper快15倍。"""
    from funasr import AutoModel
    print("   加载 SenseVoice-Small 模型（国产·CPU可用）...")
    model = AutoModel(
        model="iic/SenseVoiceSmall",
        vad_model="fsmn-vad",
        device="cpu"
    )
    print(f"   转写中: {audio_path}")
    result = model.generate(input=audio_path, language="auto", use_itn=True)
    if result and len(result) > 0:
        return result[0].get("text", "")
    return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python transcribe.py <音频文件路径>")
        sys.exit(1)

    audio = sys.argv[1]
    MINUTES_DIR.mkdir(parents=True, exist_ok=True)

    text = transcribe(audio)
    print(f"===TRANSCRIPT_START===")
    print(text)
    print(f"===TRANSCRIPT_END===")
    print(f"字数: {len(text)}")
