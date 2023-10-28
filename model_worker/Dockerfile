FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MPLCONFIGDIR /tmp/matplotlib
ENV TRANSFORMERS_CACHE=/models

# Install dependencies
RUN --mount=type=cache,target=/var/cache/apt,id=apt \
    apt-get update && \
    apt-get install --no-install-recommends -y git vim build-essential python3.11-dev python3-pip procps net-tools tini && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3.11 -m pip install --upgrade pip

# Create app_user
RUN groupadd -r app_user && useradd --no-log-init -r -g app_user app_user

# Create model_workerdirectory and change ownership to appuser
RUN mkdir /model_worker && \
    mkdir -p /home/app_user/.cache && \
    chown -R app_user:app_user /model_worker /home/app_user

COPY ./model_worker/requirements.txt /model_worker/requirements.txt

RUN --mount=type=cache,target=~/.cache/pip \
    python3.11 -m pip install -r /model_worker/requirements.txt
# # Set working directory to /app

COPY ./model_worker /model_worker
WORKDIR /model_worker
# RUN ls 
RUN chmod +x /model_worker/run.sh
ENTRYPOINT ["tini", "--", "./run.sh"]
# CMD ["tail", "-f", "/dev/null"]
