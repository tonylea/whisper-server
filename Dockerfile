FROM python:3.12-slim

# Install ffmpeg (required for audio processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    faster-whisper \
    fastapi \
    uvicorn \
    python-multipart

# Copy application code
COPY server.py .

# Create output directory
RUN mkdir -p /transcription/output

# Environment variables with defaults
ENV WHISPER_MODEL=medium.en \
    DEVICE=cpu \
    COMPUTE_TYPE=int8 \
    OUTPUT_DIR=/transcription/output \
    PORT=8000 \
    HOST=0.0.0.0

EXPOSE ${PORT}

CMD uvicorn server:app --host ${HOST} --port ${PORT}
