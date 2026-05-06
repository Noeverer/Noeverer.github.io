---
title: hugging-face使用
date: 2026-01-01 12:00:00
tags: ["platform"]
categories: work
description: hugging-face使用
published: true
---

# 如何使用
```
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    curl ca-certificates sudo build-essential git wget nano vim unzip zip htop tmux tree \
    python3 python3-pip python3-venv python-is-python3 \
    nodejs npm \
    openjdk-17-jdk \
    golang-go \
    rustc cargo \
    ruby-full \
    php-cli composer \
    perl \
    lua5.4 \
    r-base \
    scala \
    ghc cabal-install \
    docker.io docker-compose \
    nmap net-tools \
    openssh-client \
    cmake make clang gdb netcat-openbsd \
    libgtk-3-dev libgtk-3-0 \
    qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools libqt5widgets5 \
    libsdl2-dev \
    libgl1-mesa-dev libglu1-mesa-dev freeglut3-dev \
    xorg-dev xvfb x11-apps \
    && rm -rf /var/lib/apt/lists/*
# Install Tailscale
RUN export PASSWORD="Liu@06027"
RUN curl -fsSL https://tailscale.com/install.sh | sh
RUN useradd -m -s /bin/bash app && echo "app ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/app && chmod 440 /etc/sudoers.d/app
ENV HOME=/home/app
ENV XDG_CONFIG_HOME=/home/app/.config
ENV PASSWORD="Liu@06027"
RUN mkdir -p /home/app/.config/code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh
RUN echo "bind-addr: 0.0.0.0:7860" > /home/app/.config/code-server/config.yaml
RUN echo "auth: password" >> /home/app/.config/code-server/config.yaml
RUN echo "password: $PASSWORD" >> /home/app/.config/code-server/config.yaml
RUN echo "cert: false" >> /home/app/.config/code-server/config.yaml
RUN pip3 install --no-cache-dir -U pip setuptools wheel && pip3 install --no-cache-dir \
    numpy pandas scipy scikit-learn matplotlib seaborn \
    torch torchvision torchaudio \
    tensorflow keras \
    transformers datasets sentencepiece huggingface-hub \
    diffusers accelerate \
    opencv-python pillow \
    fastapi uvicorn \
    langchain gradio streamlit \
    pyaudioop audioop
RUN curl -fsSL https://ollama.com/download/OllamaLinux -o /usr/local/bin/ollama && chmod +x /usr/local/bin/ollama || true
RUN chown -R app:app /home/app
USER app
CMD ["sh", "-c", "code-server --bind-addr 0.0.0.0:7860"]

```

