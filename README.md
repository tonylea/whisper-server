# Whisper Transcription Server

A lightweight, OpenAI-compatible audio transcription API server powered by [faster-whisper](https://github.com/SYSTRAN/faster-whisper). This Docker-based service provides fast and efficient audio transcription using OpenAI's Whisper models.

## Features

- OpenAI API-compatible endpoint (`/v1/audio/transcriptions`)
- Background processing for efficient transcription
- Configurable Whisper models (tiny to large)
- Docker-based deployment for easy setup
- Persistent output directory for transcriptions
- FFmpeg integration for audio metadata extraction
- Fully configurable via environment variables

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/tonylea/whisper-server.git
   cd whisper-server
   ```

1. (Optional) Copy and customize the environment file:

   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

1. Start the server:

   ```bash
   docker-compose up -d
   ```

The server will be available at `http://localhost:8000`.

### Using Docker

Build and run the container:

```bash
docker build -t whisper-server .
docker run -d -p 8000:8000 -v $(pwd)/output:/transcription/output whisper-server
```

### Using Docker Hub

Pull and run the pre-built image:

```bash
docker pull deadrobot/whisper-server:latest
docker run -d -p 8000:8000 -v $(pwd)/output:/transcription/output deadrobot/whisper-server:latest
```

## Configuration

Configure the server using environment variables:

| Variable        | Default                 | Description                         |
| --------------- | ----------------------- | ----------------------------------- |
| `WHISPER_MODEL` | `medium.en`             | Whisper model to use (see below)    |
| `DEVICE`        | `cpu`                   | Device to run on (`cpu` or `cuda`)  |
| `COMPUTE_TYPE`  | `int8`                  | Computation precision (see below)   |
| `OUTPUT_DIR`    | `/transcription/output` | Directory for transcription outputs |
| `PORT`          | `8000`                  | Server port                         |
| `HOST`          | `0.0.0.0`               | Server host                         |

### Available Whisper Models

- `tiny`, `tiny.en`
- `base`, `base.en`
- `small`, `small.en`
- `medium`, `medium.en`
- `large-v1`, `large-v2`, `large-v3`

English-only models (`.en`) are faster and more accurate for English audio.

### Compute Types

- `int8` - Best for CPU (recommended)
- `int8_float16` - Mixed precision
- `int16` - Higher precision
- `float16` - GPU optimized
- `float32` - Highest precision

## API Usage

### Transcribe Audio

**Endpoint:** `POST /v1/audio/transcriptions`

**Request:**

```bash
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=medium.en"
```

**Response:**

```json
{
  "status": "processing",
  "message": "Transcription started for audio.mp3",
  "model": "medium.en",
  "audio_duration": "3m 45s",
  "output_file": "/transcription/output/audio.txt"
}
```

The transcription is processed in the background. Results are saved to the `output_file` location.

**Note:** You can specify different Whisper models per request using the `model` parameter. If not specified, it defaults to the `WHISPER_MODEL` environment variable. Models are cached in memory after first use for better performance.

**Using different models:**

```bash
# Use tiny model for faster transcription
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=tiny.en"

# Use large model for better accuracy
curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -F "file=@audio.mp3" \
  -F "model=large-v3"
```

### Supported Audio Formats

Any format supported by FFmpeg:

- MP3
- WAV
- M4A
- FLAC
- OGG
- And many more...

## API Documentation

Once the server is running, visit:

- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Development

### Local Setup with Virtual Environment

1. Clone the repository and create a virtual environment:

   ```bash
   git clone https://github.com/tonylea/whisper-server.git
   cd whisper-server

   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure FFmpeg is installed:

   ```bash
   # macOS
   brew install ffmpeg

   # Ubuntu/Debian
   sudo apt-get install ffmpeg

   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

4. Run the server:

   ```bash
   uvicorn server:app --reload
   ```

5. When done, deactivate the virtual environment:

   ```bash
   deactivate
   ```

### Setup GitHub Actions

1. Go to your GitHub repository Settings → Secrets and variables → Actions
2. Add the following secrets:

   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token (create at [Docker Hub Security](https://hub.docker.com/settings/security))

3. Create releases using the Automated Release workflow:

   **Via GitHub Actions (Recommended):**

   - Go to Actions → "Automated Release"
   - Click "Run workflow"
   - Select release type (patch/minor/major)
   - The workflow will:
     - Generate/update CHANGELOG.md based on conventional commits
     - Bump version in package.json
     - Create a git tag (e.g., `v1.2.3`)
     - Push changes and tag to repository
     - Automatically trigger the Docker build workflow

   **Via Local Development:**

   ```bash
   # Install Node.js dependencies
   npm install

   # Create a release (updates version, changelog, and creates tag)
   npm run release:patch  # 1.0.0 → 1.0.1
   npm run release:minor  # 1.0.0 → 1.1.0
   npm run release:major  # 1.0.0 → 2.0.0

   # Push changes and tags
   git push --follow-tags origin main
   ```

### Docker Image Tagging

When a git tag is created (e.g., `v1.2.3`), the Docker workflow automatically builds and pushes images with multiple tags:

- `deadrobot/whisper-server:1.2.3` - Full version
- `deadrobot/whisper-server:1.2` - Minor version
- `deadrobot/whisper-server:1` - Major version
- `deadrobot/whisper-server:latest` - Latest stable release

This allows users to pin to specific versions or always use the latest:

```bash
# Use specific version (recommended for production)
docker pull deadrobot/whisper-server:1.2.3

# Use minor version (gets patch updates)
docker pull deadrobot/whisper-server:1.2

# Use major version (gets minor and patch updates)
docker pull deadrobot/whisper-server:1

# Always use latest (gets all updates)
docker pull deadrobot/whisper-server:latest
```

## Performance Tips

- Use English-only models (`.en`) for English audio - they're faster and more accurate
- For CPU: Use `int8` compute type
- For GPU: Use `float16` or `int8_float16` compute type with `DEVICE=cuda`
- Larger models are more accurate but slower
- Consider using `tiny` or `base` models for real-time applications

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Conventional Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for commit messages and automated versioning. Please follow the commit message format:

```bash
feat: add new feature
fix: resolve bug
docs: update documentation
chore: maintenance tasks
```

See [COMMITS.md](COMMITS.md) for detailed guidelines and examples.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make changes using conventional commits
4. Push and create a Pull Request
5. Once merged, maintainers will create releases using the automated release workflow

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Original Whisper model
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - Optimized Whisper implementation
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/tonylea/whisper-server/issues) on GitHub.
