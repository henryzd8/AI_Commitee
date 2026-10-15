# Pinned GPU runtime: official vLLM 0.31.0 image (digest pinned), plus this package.
# Build from the repo root:  docker build -f docker/Dockerfile -t policy-updates .
# Run (GPU box):             docker run --gpus all -v /data:/data -e HF_TOKEN policy-updates run ...
FROM vllm/vllm-openai:v0.31.0@sha256:c1c9f6fd5c109ba7f0546a59f5b2f15fb87f64c77782e90a27b648b42a8e67c3

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY configs ./configs

# vllm and torch come from the base image; pin the rest to match uv.lock.
RUN pip install --no-cache-dir "transformers==5.17.0" "pyyaml==6.0.3" \
 && pip install --no-cache-dir --no-deps -e . \
 && python -c "import vllm, transformers; assert vllm.__version__ == '0.31.0', vllm.__version__; assert transformers.__version__ == '5.17.0'"

ENV PU_CONFIG_DIR=/app/configs \
    HF_HOME=/data/hf-cache
ENTRYPOINT ["pu"]
