# Contributing to OPDS-ABS

Thank you for your interest in contributing! This project is maintained as an open-source effort, and we appreciate help with bug fixes, documentation, and new features.

## ✅ How to contribute

1. **Fork the repository** and create a feature branch.
2. Make your changes.
3. Run the checks locally (see below).
4. Open a pull request against the `master` branch.

## 🧪 Local checks (required before opening a PR)

### 1) Install dependencies

```bash
python -m pip install -r requirements-dev.txt
```

### 2) Run pre-commit hooks

This ensures formatting and docstring checks are enforced.

```bash
pre-commit install
pre-commit run --all-files
```

### 3) Run docstring checks

The repository includes a helper script for docstring validation.

```bash
python docstring-check.py --summary
```

### 4) (Optional) Run the server locally

```bash
python run.py
```

By default, the server binds to `0.0.0.0:8000` and will automatically try the next available port if it is occupied.

## 📚 Documentation standards

Refer to [DOCS_STANDARDS.md](DOCS_STANDARDS.md) for the docstring style guide and required patterns.

## 🐳 Docker image publishing

This project publishes Docker images to GitHub Container Registry automatically via GitHub Actions:

- `master` pushes produce `ghcr.io/<org>/opds-abs:latest`
- `dev` pushes produce `ghcr.io/<org>/opds-abs:dev-<sha>`

## 🔍 Need help?

If you run into any issues or want to propose a change, open an issue on GitHub and provide as much detail as possible.
