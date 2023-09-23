FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MPLCONFIGDIR /tmp/matplotlib
# Install dependencies
RUN --mount=type=cache,target=/var/cache/apt,id=apt \
    apt-get update && \
    apt-get install --no-install-recommends -y git vim build-essential python3.11-dev python3-pip procps net-tools tini && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3.11 -m pip install --upgrade pip

# Create appuser
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Create app directory and change ownership to appuser
RUN mkdir /app && \
    mkdir -p /home/appuser/.cache && \
    chown -R appuser:appuser /app /home/appuser
COPY ./requirements/requirements.txt /app/requirements.txt
COPY ./requirements/requirements-server.txt /app/requirements-server.txt
RUN --mount=type=cache,target=~/.cache/pip \
    python3.11 -m pip install -r /app/requirements.txt && \
    python3.11 -m pip install -r /app/requirements-server.txt
# # Set working directory to /app
WORKDIR /app

COPY --chown=appuser:appuser  . /app/ai_driver
USER appuser
WORKDIR /app/ai_driver
RUN python3.11 -m pip install .
RUN chmod +x ./ai_driver/server/scripts/run.sh
ENTRYPOINT ["tini", "--", "./ai_driver/server/scripts/run.sh"]
# CMD ["tail", "-f", "/dev/null"]
