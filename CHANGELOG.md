# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-24

### Features

- Initial release of Whisper Transcription Server
- OpenAI-compatible `/v1/audio/transcriptions` endpoint
- Background processing for efficient transcription
- Configurable Whisper models (tiny to large)
- Docker-based deployment
- Per-request model selection with caching
- Environment variable configuration
- FFmpeg integration for audio metadata
- FastAPI with automatic API documentation
