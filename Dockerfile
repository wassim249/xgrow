ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001

# Install dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER root

COPY . .


# Run the application.
CMD python main.py
