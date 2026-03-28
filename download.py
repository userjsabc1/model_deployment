#!/usr/bin/env python3
"""从 HuggingFace 下载模型到本地"""
import os
from pathlib import Path

from config import CONFIG


def main() -> None:
    # 设置镜像
    if CONFIG.hf_endpoint:
        os.environ["HF_ENDPOINT"] = CONFIG.hf_endpoint
        print(f"==> HF 镜像: {CONFIG.hf_endpoint}")
    if CONFIG.hf_token:
        os.environ["HUGGING_FACE_HUB_TOKEN"] = CONFIG.hf_token

    from huggingface_hub import snapshot_download

    local_dir = Path(CONFIG.model_local_dir)
    local_dir.mkdir(parents=True, exist_ok=True)

    print(f"==> 下载模型: {CONFIG.model_id}")
    print(f"==> 保存到:   {local_dir}")
    print("    （模型约 54GB，请耐心等待）\n")

    snapshot_download(
        repo_id=CONFIG.model_id,
        local_dir=str(local_dir),
        ignore_patterns=["*.gguf", "*.bin"],   # 只要 safetensors
    )

    print(f"\n==> 下载完成: {local_dir}")


if __name__ == "__main__":
    main()
