# Contributing to Whisper Server

Thank you for considering contributing to Whisper Server! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, Docker version, etc.)
- Relevant logs or error messages

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:

- A clear description of the feature
- Use cases and benefits
- Any potential implementation ideas

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

### Development Setup

1. Clone your fork:

   ```bash
   git clone https://github.com/tonylea/whisper-server.git
   cd whisper-server
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the server locally:

   ```bash
   uvicorn server:app --reload
   ```

### Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and concise

### Testing

Before submitting a PR:

- Test with different audio formats
- Test with different Whisper models
- Ensure the Docker build works: `docker build -t whisper-server .`
- Test the docker-compose setup

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Reference issues when applicable (e.g., "Fix #123")

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
