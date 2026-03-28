#!/usr/bin/env python3
"""启动 vLLM OpenAI 兼容推理服务"""
import os
import sys
from pathlib import Path

from config import CONFIG


def build_args() -> list[str]:
    # 优先用本地路径，不存在则直接用 HuggingFace model ID
    model_path = CONFIG.model_local_dir if Path(CONFIG.model_local_dir).exists() else CONFIG.model_id

    args = [
        "--model", model_path,
        "--served-model-name", CONFIG.model_name,
        "--host", CONFIG.host,
        "--port", str(CONFIG.port),
        "--dtype", CONFIG.dtype,
        "--tensor-parallel-size", str(CONFIG.tensor_parallel_size),
        "--gpu-memory-utilization", str(CONFIG.gpu_memory_utilization),
        "--max-model-len", str(CONFIG.max_model_len),
        "--enable-prefix-caching",
    ]

    if CONFIG.quantization == "bitsandbytes":
        args += ["--quantization", "bitsandbytes", "--load-format", "bitsandbytes"]
    elif CONFIG.quantization:
        args += ["--quantization", CONFIG.quantization]

    return args, model_path


def main() -> None:
    # 绑定指定 GPU，设置后 vLLM 只能看到这一张卡
    os.environ["CUDA_VISIBLE_DEVICES"] = str(CONFIG.gpu_id)

    if CONFIG.hf_endpoint:
        os.environ["HF_ENDPOINT"] = CONFIG.hf_endpoint

    args, model_path = build_args()

    print("==> 启动 vLLM")
    print(f"    GPU:    #{CONFIG.gpu_id}")
    print(f"    模型:   {model_path}")
    print(f"    地址:   http://{CONFIG.host}:{CONFIG.port}")
    print(f"    量化:   {CONFIG.quantization or '无'}")
    print(f"    上下文: {CONFIG.max_model_len} tokens")
    print()

    # 直接调用 vLLM 的 entrypoint，等同于 python -m vllm.entrypoints.openai.api_server
    from vllm.entrypoints.openai.cli_args import make_arg_parser
    from vllm.entrypoints.openai.api_server import run_server
    from vllm.utils import FlexibleArgumentParser

    parser = make_arg_parser(FlexibleArgumentParser())
    parsed_args = parser.parse_args(args)
    run_server(parsed_args)


if __name__ == "__main__":
    main()
