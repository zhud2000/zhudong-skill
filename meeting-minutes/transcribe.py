#!/usr/bin/env python3
# [2026-06-16] Whisper转写辅助脚本——meeting-minutes SKILL 的语音转文字部分
# 关联影响：SKILL.md 调用此脚本获取转写文本后，自动生成结构化纪要

import sys
from pathlib import Path

WORKSPACE = "C:/Users/zhud2000/Desktop/工作文件/研究院工作区"
MINUTES_DIR = Path(WORKSPACE) / "会议纪要"

def transcribe(audio_path: str) -> str:
    """用 Whisper small 模型转写中文音频"""
    import whisper
    print(f"   加载 Whisper small 模型...")
    model = whisper.load_model("small")
    print(f"   转写中: {audio_path}")
    result = model.transcribe(audio_path, language="zh")
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python transcribe.py <音频文件路径>")
        sys.exit(1)

    audio = sys.argv[1]
    MINUTES_DIR.mkdir(parents=True, exist_ok=True)

    text = transcribe(audio)
    # 输出到标准输出，SKILL 会读取
    print(f"===TRANSCRIPT_START===")
    print(text)
    print(f"===TRANSCRIPT_END===")
    print(f"字数: {len(text)}")
