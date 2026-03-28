#!/usr/bin/env python3
"""安装部署所需依赖"""
import subprocess
import sys


PACKAGES = [
    "vllm",
    "huggingface-hub",
    "transformers>=5.2.0",
    "accelerate",
    "openai",
    "httpx",
]


def pip_install(package: str) -> None:
    print(f"  installing {package} ...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", package, "-U", "-q"],
        check=True,
    )


def main() -> None:
    print("==> 安装依赖")
    for pkg in PACKAGES:
        pip_install(pkg)

    import vllm
    print(f"\n==> 完成")
    print(f"    vLLM {vllm.__version__} | Python {sys.version.split()[0]}")


if __name__ == "__main__":
    main()
