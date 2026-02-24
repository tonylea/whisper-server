# Changelog

All notable changes to this project will be documented in this file. See [commit-and-tag-version](https://github.com/absolute-version/commit-and-tag-version) for commit guidelines.

## 2.0.0 (2026-02-24)


### Features

* **ci:** add automated versioning and release workflow ([d1b24bb](https://github.com/tonylea/whisper-server/commit/d1b24bb9ec8b1154f6d298890041ca5135fa31dc))
* **ci:** integrate Docker tagging with automated releases ([f7cafb3](https://github.com/tonylea/whisper-server/commit/f7cafb399c16960802231f5bd35e2bc7090823f6))


### Maintenance

* update gitignore for Node.js and Claude CLI ([a3ff6bc](https://github.com/tonylea/whisper-server/commit/a3ff6bca67aab4fdf223e5920ec6feb44912f23d))


### Documentation

* add conventional commits guide and update README ([1659196](https://github.com/tonylea/whisper-server/commit/1659196883f441277616f2b6f5e86eb23c680913))

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
