FROM python:3.11
ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MPLCONFIGDIR /tmp/matplotlib

RUN --mount=type=cache,target=/var/cache/apt,id=apt \
    apt-get update && apt-get -y upgrade
RUN apt-get update && apt-get -y install procps net-tools tini

RUN python3 -m pip install --upgrade pip

# Create appuser
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Create app directory and change ownership to appuser
RUN mkdir /app && \
    mkdir -p /home/appuser/.cache && \
    chown -R appuser:appuser /app /home/appuser

COPY ./requirements/requirements-ui.in /app/requirements.txt
# Set environment variables
RUN --mount=type=cache,target=~/.cache/pip \
    pip install -r /app/requirements.txt
# Download public link share
RUN curl -o frpc_linux_amd64_v0.2 https://cdn-media.huggingface.co/frpc-gradio-0.2/frpc_linux_amd64 && \
    mv frpc_linux_amd64_v0.2 /usr/local/lib/python3.11/site-packages/gradio
# Set working directory to /app
COPY .  /aidriver/
RUN --mount=type=cache,target=~/.cache/pip \
    pip install -e /aidriver
WORKDIR /app

COPY --chown=appuser:appuser  . /app/webui
USER appuser
WORKDIR /app/webui

ENTRYPOINT ["tini", "--", "python3", "webui/server.py"]
# CMD ["tail", "-f", "/dev/null"]
