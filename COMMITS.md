# Conventional Commits Guide

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, whitespace, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Changes to build system or dependencies
- **ci**: Changes to CI/CD configuration
- **chore**: Other changes that don't modify src or test files

## Examples

### Feature
```bash
git commit -m "feat: add per-request model selection"
git commit -m "feat(api): add model caching for better performance"
```

### Bug Fix
```bash
git commit -m "fix: resolve memory leak in transcription background task"
git commit -m "fix(docker): correct environment variable handling"
```

### Documentation
```bash
git commit -m "docs: add conventional commits guide"
git commit -m "docs(readme): update API usage examples"
```

### Breaking Changes
```bash
git commit -m "feat!: change API response format

BREAKING CHANGE: The response now includes a 'model' field"
```

### Chore
```bash
git commit -m "chore: update dependencies"
git commit -m "chore(ci): add automated release workflow"
```

## Scope (Optional)

Scopes help identify what part of the codebase was changed:
- `api` - API endpoints
- `docker` - Docker configuration
- `ci` - CI/CD workflows
- `docs` - Documentation
- `deps` - Dependencies

## Benefits

1. **Automated Changelog**: Automatically generates CHANGELOG.md
2. **Semantic Versioning**: Automatically determines version bumps
   - `fix`: patch version (1.0.0 → 1.0.1)
   - `feat`: minor version (1.0.0 → 1.1.0)
   - `BREAKING CHANGE`: major version (1.0.0 → 2.0.0)
3. **Better Git History**: Easier to understand project evolution
4. **Automated Releases**: Triggers versioning and releases automatically

## Creating Releases

### Using GitHub Actions (Recommended)

1. Go to Actions → Automated Release
2. Click "Run workflow"
3. Select release type (patch/minor/major)
4. The workflow will:
   - Generate/update CHANGELOG.md
   - Bump version in package.json
   - Create a git tag
   - Push changes and tag
   - Trigger Docker image build

### Local Release

```bash
# Install dependencies
npm install

# Create a patch release (1.0.0 → 1.0.1)
npm run release:patch

# Create a minor release (1.0.0 → 1.1.0)
npm run release:minor

# Create a major release (1.0.0 → 2.0.0)
npm run release:major

# Push changes and tags
git push --follow-tags origin main
```

## Complete Workflow Example

### Development and Release Cycle

```bash
# 1. Create feature branch
git checkout -b feat/new-feature

# 2. Make changes and commit using conventional commits
git add .
git commit -m "feat: add new transcription format"

# 3. Push branch and create PR
git push origin feat/new-feature

# 4. After PR is merged to main, create release (maintainers only)
# Option A: Via GitHub Actions
# - Go to Actions → "Automated Release" → Run workflow → Select patch/minor/major

# Option B: Via local npm
npm install
npm run release:minor  # Creates v1.1.0 tag
git push --follow-tags origin main

# 5. Automated Docker Build is triggered
# When the git tag (e.g., v1.1.0) is pushed, the Docker workflow automatically:
# - Builds the Docker image
# - Tags it as: 1.1.0, 1.1, 1, latest
# - Pushes to Docker Hub
```

### What Happens During a Release

1. **Changelog Generation**: CHANGELOG.md is updated with all commits since last release
2. **Version Bump**: package.json version is bumped (1.0.0 → 1.1.0)
3. **Git Tag Created**: A tag like `v1.1.0` is created
4. **Commit & Push**: Changes are committed and pushed with the tag
5. **Docker Build Triggered**: The tag push triggers the Docker workflow
6. **Multi-Tag Docker Images**: Image is tagged with `1.1.0`, `1.1`, `1`, and `latest`
7. **Published**: Docker images are available on Docker Hub

Users can then pull the new version:

```bash
docker pull deadrobot/whisper-server:1.1.0  # Specific version
docker pull deadrobot/whisper-server:latest # Always latest
```

## Version Bumping Logic

- Commits with `fix:` → **PATCH** version bump (1.0.0 → 1.0.1)
- Commits with `feat:` → **MINOR** version bump (1.0.0 → 1.1.0)
- Commits with `BREAKING CHANGE:` → **MAJOR** version bump (1.0.0 → 2.0.0)
- Commits with `chore:`, `docs:`, etc. → No version bump (unless manually triggered)

## Tips

- Keep commits focused and atomic
- Use descriptive but concise commit messages
- Reference issues when applicable: `fix: resolve #123`
- Use breaking changes sparingly and document them well
- The first line should be ≤ 72 characters
