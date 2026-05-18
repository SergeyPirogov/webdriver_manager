# Releasing webdriver-manager

This document is the maintainer runbook for publishing `webdriver-manager` releases.

## Release model

- Use `patch` for bugfixes, metadata/docs cleanup, and non-breaking maintenance changes.
- Use `minor` for new backward-compatible features.
- Use `major` for breaking changes.

## Prerequisites

- Maintainer access to:
  - repository push/tag permissions;
  - GitHub Releases;
  - PyPI token (`__token__` user) when publishing manually.
- Local environment:
  - Python 3.12+ is recommended for release tooling;
  - `.venv` with `build`, `twine`, and `bump2version`.

Install tooling:

```bash
./.venv/bin/pip install -U build twine bump2version
```

## Version sources

Release version must stay aligned in:

- `pyproject.toml` (`[project].version`);
- `webdriver_manager/__init__.py` (`__version__`);
- `setup.cfg` (`[bumpversion].current_version`).

`setup.py` is a compatibility shim. Packaging metadata is sourced from `pyproject.toml`.

## Standard release flow (preferred)

1. Ensure branch is up to date and tests are green.
2. Update `CHANGELOG.md` for the target version.
3. Bump version:

```bash
./.venv/bin/bump2version patch
# or: minor / major
```

4. Build and validate artifacts:

```bash
find . -maxdepth 1 -name '*.egg-info' -exec rm -rf {} +
rm -rf dist build
./.venv/bin/python -m build
./.venv/bin/twine check dist/*
```

5. Push commit and tag:

```bash
git push
git push --tags
```

6. Create and publish a GitHub Release for the new tag.
7. Verify deploy workflow completed successfully:
   - `.github/workflows/deploy.yml` runs on `release.published`;
   - artifacts are uploaded to PyPI.

## Fallback when GitHub Release UI/API is unavailable

Use this only when GitHub release creation is blocked.

1. Run steps 1-5 from the standard flow.
2. Publish directly to PyPI from local artifacts:

```bash
./.venv/bin/twine upload dist/*
```

3. When GitHub recovers, create the GitHub Release for the same tag and include notes.

Important:

- The deploy workflow may fail later on re-upload because the same version already exists on PyPI.
- That failure is expected in this fallback path; do not republish with the same version.

## Post-release checks

- PyPI page shows correct:
  - version;
  - summary;
  - `Requires-Python`;
  - supported Python classifiers.
- README badges resolve to `webdriver-manager` package.
- Install smoke test:

```bash
python -m venv /tmp/wdm-smoke
source /tmp/wdm-smoke/bin/activate
pip install webdriver-manager==X.Y.Z
python -c "import webdriver_manager; print(webdriver_manager.__version__)"
```

## Notes

- Keep `4.x` maintenance releases small and focused.
- Do not yank a release unless it is functionally unsafe (install/runtime/security/API breakage).
