FROM python:3.10-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -r requirements.txt


FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

COPY main.py .
COPY core/ ./core/
COPY handlers/ ./handlers/
COPY utils/ ./utils/

VOLUME /app/audio
VOLUME /app/data
VOLUME /app/logs

CMD ["python", "main.py"]