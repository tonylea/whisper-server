from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from faster_whisper import WhisperModel
import tempfile, os, subprocess, json
from pathlib import Path
from typing import Dict

app = FastAPI(
    title="Whisper Transcription API",
    description="OpenAI Whisper-compatible transcription API using faster-whisper",
    version="1.0.0"
)

# Configuration from environment variables
DEFAULT_MODEL = os.environ.get("WHISPER_MODEL", "medium.en")
DEVICE = os.environ.get("DEVICE", "cpu")
COMPUTE_TYPE = os.environ.get("COMPUTE_TYPE", "int8")
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "/transcription/output"))

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Model cache to avoid reloading models
model_cache: Dict[str, WhisperModel] = {}

def get_whisper_model(model_name: str) -> WhisperModel:
    """Get or load a Whisper model from cache."""
    if model_name not in model_cache:
        print(f"Loading model: {model_name}")
        model_cache[model_name] = WhisperModel(model_name, device=DEVICE, compute_type=COMPUTE_TYPE)
    return model_cache[model_name]

# Pre-load default model
whisper = get_whisper_model(DEFAULT_MODEL)

def get_duration(path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True
    )
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])

def transcribe_background(tmp_path: str, filename: str, model_name: str):
    try:
        stem = Path(filename).stem
        output_path = OUTPUT_DIR / f"{stem}.txt"
        model = get_whisper_model(model_name)
        segments, _ = model.transcribe(tmp_path)
        with output_path.open("w") as f:
            for segment in segments:
                f.write(segment.text + " ")
                f.flush()
    finally:
        os.unlink(tmp_path)

@app.post("/v1/audio/transcriptions")
async def transcribe(background_tasks: BackgroundTasks, file: UploadFile = File(...), model: str = Form(default=None)):
    # Use provided model or fall back to default
    model_name = model or DEFAULT_MODEL

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    duration = get_duration(tmp_path)
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    background_tasks.add_task(transcribe_background, tmp_path, file.filename, model_name)

    return {
        "status": "processing",
        "message": f"Transcription started for {file.filename}",
        "model": model_name,
        "audio_duration": f"{minutes}m {seconds}s",
        "output_file": str(OUTPUT_DIR / f"{Path(file.filename).stem}.txt")
    }
