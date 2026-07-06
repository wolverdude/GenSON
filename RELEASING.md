# Releasing GenSON

Releases are published automatically by the `Publish` GitHub Actions workflow
via [PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/) —
no local credentials or `twine upload` needed. Pushing a tag is the release.

**The published version comes from `__version__` in `genson/__init__.py`,
not from the tag.** The tag only triggers the workflow. The workflow fails
fast if the two disagree, so an rc tag can't silently publish a final-looking
version (this happened with `v1.3.1rc1`, which published as `1.3.1`).

Version strings follow [PEP 440](https://peps.python.org/pep-0440/): release
candidates are `1.4.0rc1`, `1.4.0rc2`, … Don't use a fourth dotted number
(e.g. `1.4.0.1`) for test releases — it sorts *after* the final release, so
resolvers treat it as newer, whereas `rc` versions sort before the final and
pip ignores them unless explicitly pinned.

## Checklist

1. **Python version matrix check** (do this every release — it goes stale with
   time, not with code): are there new stable CPython releases to add, or
   EOL versions to drop? Update all three together:
   - `tox.ini` (`envlist`)
   - `.github/workflows/test.yml` (matrix)
   - `setup.cfg` (classifiers)

   Note any support changes in `HISTORY.rst`.

2. Add a `HISTORY.rst` entry for the new version.

3. Make sure CI is green on `master`.

4. **Dry run against TestPyPI**: set `__version__` in `genson/__init__.py` to
   the rc version, commit, and push a matching tag:

   ```sh
   # in genson/__init__.py: __version__ = '1.4.0rc1'
   git commit -am "Bump version to 1.4.0rc1" && git push
   git tag v1.4.0rc1 && git push origin v1.4.0rc1
   ```

   The workflow publishes rc tags to TestPyPI and then **verifies the release
   automatically** (`verify-testpypi` job): installs it from TestPyPI in a
   clean environment, checks the version, imports the package (this catches
   packaging bugs like v1.3.0's missing `genson.schema` subpackage), and runs
   the CLI. If that job is green, the mechanics are good.

   Then open [the TestPyPI page](https://test.pypi.org/project/genson/) and
   inspect the docs to ensure nothing broke the RST parsing.

   If something needs fixing, fix it and repeat with `rc2` — (Test)PyPI never
   accepts the same version twice, so each attempt needs a new rc number.

5. **Release**: set `__version__` to the final version, commit, tag, push.

   ```sh
   # in genson/__init__.py: __version__ = '1.4.0'
   git commit -am "Release 1.4.0" && git push
   git tag v1.4.0 && git push origin v1.4.0
   ```

   The workflow publishes final tags to PyPI and verifies the same way
   (`verify-pypi` job). Check [the PyPI page](https://pypi.org/project/genson/)
   docs rendering once more.

6. Create a GitHub release from the tag with the `HISTORY.rst` entry as notes
   (optional but nice for watchers).

## Manual verification (fallback)

Normally the workflow's verify job covers this. To check by hand, run from the
repo with the tag you're verifying checked out:

```sh
VERSION="$(git describe --tags --exact-match | sed 's/^v//')"
VENV_DIR="$(mktemp -d)"
python3 -m venv "$VENV_DIR/venv"
"$VENV_DIR/venv/bin/pip" install \
  --index-url https://test.pypi.org/simple/ "genson==$VERSION"
"$VENV_DIR/venv/bin/python" -c "import genson; print(genson.__version__)"
"$VENV_DIR/venv/bin/python" -m genson --version
echo '{"hi": 5}' | "$VENV_DIR/venv/bin/genson"
rm -rf "$VENV_DIR"  # clean up so a stale venv can't shadow the next rc
```

(Drop the `--index-url` line to verify a final release from PyPI instead.)

## Trusted publisher configuration (one-time, already done)

- pypi.org → project `genson` → Settings → Publishing → GitHub:
  owner `wolverdude`, repo `GenSON`, workflow `publish.yml`, environment `pypi`.
- test.pypi.org: same, with environment `testpypi`.
