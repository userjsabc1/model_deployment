# Model Deployment

部署 [Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled](https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled) 到 L20 GPU 机器。

## 文件说明

| 文件 | 说明 |
|------|------|
| `config.py` | 所有配置（先改这里） |
| `install.py` | 安装依赖 |
| `download.py` | 下载模型到本地 |
| `serve.py` | 启动 vLLM 推理服务 |
| `health_check.py` | 健康检查 + 测试请求 |
| `docker/` | Docker 部署方式 |

## 快速开始

### 1. 修改配置

```python
# config.py
model_local_dir: str = "/data/models/qwen3.5-27b"   # 模型存放路径
hf_endpoint: str = "https://hf-mirror.com"           # 国内加速，境外置空
port: int = 8000
```

### 2. 安装依赖

```bash
python install.py
```

### 3. 下载模型（约 54GB）

```bash
python download.py
```

### 4. 启动服务

```bash
# 前台（调试）
python serve.py

# 后台
nohup python serve.py > serve.log 2>&1 &
```

### 5. 验证

```bash
python health_check.py
```

## 显存说明（L20 48GB）

| 量化 | 显存 | 说明 |
|------|------|------|
| BF16 | ~54GB | L20 装不下 |
| INT8 | ~27GB | 默认，推荐 |
| INT4 | ~14GB | 显存宽裕时可扩大上下文 |

## 常见问题

**OOM** → 降低 `max_model_len`（如 8192）或调低 `gpu_memory_utilization`

**下载慢** → 设置 `hf_endpoint = "https://hf-mirror.com"`

**服务无响应** → 模型加载需 1~3 分钟，等待后再运行 `health_check.py`
