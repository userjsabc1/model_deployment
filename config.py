"""部署配置，按需修改"""
from dataclasses import dataclass


@dataclass
class Config:
    # 模型（FP8 量化版，~27GB，H20 原生硬件加速支持，精度损失极小）
    model_id: str = "mconcat/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-FP8-Dynamic"
    model_name: str = "qwen3.5-27b"
    model_local_dir: str = "/mnt/data/models/qwen3.5-27b-fp8"  # NFS 大盘，空间充足

    # 服务
    host: str = "0.0.0.0"
    port: int = 8000

    # GPU（指定用哪张卡，0/1/2/3，不影响其他人）
    gpu_id: int = 3                 # 用最后一张，通常最空闲
    tensor_parallel_size: int = 1
    gpu_memory_utilization: float = 0.80
    dtype: str = "bfloat16"

    # FP8 量化（H20 Hopper 架构原生支持，vLLM 自动识别）
    quantization: str = "fp8"

    # 上下文长度（先用最小，跑通后再调大）
    max_model_len: int = 4096

    # HuggingFace（huggingface.co 不通，走镜像）
    hf_endpoint: str = "https://hf-mirror.com"
    hf_token: str = ""


CONFIG = Config()