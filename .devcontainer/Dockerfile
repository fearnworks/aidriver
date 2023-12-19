FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

RUN --mount=type=cache,target=/var/cache/apt,id=apt \
    apt-get update && \
    apt-get install --no-install-recommends -y vim build-essential procps net-tools tini cuda-toolkit && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

