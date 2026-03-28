FROM vllm/vllm-openai:latest

WORKDIR /app

COPY configs/config.env /app/configs/config.env
COPY scripts/ /app/scripts/

RUN chmod +x /app/scripts/*.sh

# 默认启动命令（实际参数通过 docker-compose 环境变量传入）
CMD ["python3", "-m", "vllm.entrypoints.openai.api_server"]