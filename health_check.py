#!/usr/bin/env python3
"""健康检查：验证服务是否正常，并发一条测试请求"""
import sys

from openai import OpenAI
import httpx

from config import CONFIG


def main() -> None:
    base_url = f"http://{CONFIG.host}:{CONFIG.port}"

    # 1. 检查 /health
    print(f"==> 检查服务: {base_url}/health")
    try:
        resp = httpx.get(f"{base_url}/health", timeout=5)
        if resp.status_code == 200:
            print("    [OK] 服务正常")
        else:
            print(f"    [FAIL] HTTP {resp.status_code}")
            sys.exit(1)
    except httpx.ConnectError:
        print("    [FAIL] 无法连接，服务可能还未启动")
        sys.exit(1)

    # 2. 列出已加载模型
    print("\n==> 已加载模型:")
    models_resp = httpx.get(f"{base_url}/v1/models", timeout=5)
    for m in models_resp.json()["data"]:
        print(f"    - {m['id']}")

    # 3. 发送测试请求
    print("\n==> 发送测试请求...")
    client = OpenAI(base_url=f"{base_url}/v1", api_key="dummy")
    completion = client.chat.completions.create(
        model=CONFIG.model_name,
        messages=[{"role": "user", "content": "1+1等于几？简短回答。"}],
        max_tokens=64,
    )
    answer = completion.choices[0].message.content
    print(f"    [响应] {answer}")
    print(f"\n    tokens: prompt={completion.usage.prompt_tokens} "
          f"completion={completion.usage.completion_tokens}")


if __name__ == "__main__":
    main()
