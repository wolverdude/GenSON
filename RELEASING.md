# Releasing GenSON

Releases are published automatically by the `Publish` GitHub Actions workflow
via [PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/) —
no local credentials or `twine upload` needed. Pushing a tag is the release.

## Checklist

1. **Python version matrix check** (do this every release — it goes stale with
   time, not with code): are there new stable CPython releases to add, or
   EOL versions to drop? Update all three together:
   - `tox.ini` (`envlist`)
   - `.github/workflows/test.yml` (matrix)
   - `setup.cfg` (classifiers)

   Note any support changes in `HISTORY.rst`.

2. Add a `HISTORY.rst` entry for the new version.

3. Bump `__version__` in `genson/__init__.py` (it is the single source of
   truth; `setup.cfg` reads it).

4. Make sure CI is green on `master`.

5. **Dry run against TestPyPI**: push an rc tag, e.g.

   ```sh
   git tag v1.3.1rc1 && git push origin v1.3.1rc1
   ```

   The workflow publishes rc tags to TestPyPI. Then verify in a fresh venv:

   ```sh
   python3 -m venv /tmp/genson-rc && /tmp/genson-rc/bin/pip install \
     --index-url https://test.pypi.org/simple/ genson==<version>rc1
   /tmp/genson-rc/bin/python -c "import genson; print(genson.__version__)"
   /tmp/genson-rc/bin/python -m genson --version
   echo '{"hi": 5}' | /tmp/genson-rc/bin/genson
   ```

   The import check matters: it catches packaging bugs like v1.3.0's missing
   `genson.schema` subpackage.

   Finally, open the web page and inspect the docs to ensure nothing broke the RST parsing.

6. **Release**: push the final tag.

   ```sh
   git tag v1.3.1 && git push origin v1.3.1
   ```

   The workflow publishes final tags to PyPI. Verify with
   `pip install genson==<version>` in a fresh venv.

7. Create a GitHub release from the tag with the `HISTORY.rst` entry as notes
   (optional but nice for watchers).

## Trusted publisher configuration (one-time, already done)

- pypi.org → project `genson` → Settings → Publishing → GitHub:
  owner `wolverdude`, repo `GenSON`, workflow `publish.yml`, environment `pypi`.
- test.pypi.org: same, with environment `testpypi`.
