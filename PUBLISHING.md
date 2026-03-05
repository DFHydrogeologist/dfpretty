# Publishing Guide — dfpretty

Step-by-step instructions to go from local code → GitHub → PyPI → conda-forge.

---

## 1 · Prepare GitHub

```bash
cd dfpretty
git init
git add .
git commit -m "feat: initial release v0.1.0"

# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/dfpretty.git
git branch -M main
git push -u origin main
```

Tag the release (conda-forge needs a git tag):
```bash
git tag v0.1.0
git push origin v0.1.0
```

---

## 2 · Publish to PyPI

PyPI is the required step before conda-forge — conda-forge builds *from* PyPI.

### 2a · Create accounts
- https://pypi.org/account/register/
- Enable 2FA (required for new packages)

### 2b · Build the package

```bash
pip install build twine
python -m build          # creates dist/dfpretty-0.1.0.tar.gz + .whl
```

### 2c · Upload

```bash
# Test first on test.pypi.org
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ dfpretty

# When happy, upload to real PyPI
twine upload dist/*
```

You'll be prompted for your PyPI username and password (or API token).
It's easier to use an API token — create one at https://pypi.org/manage/account/token/
and store it in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-XXXXXXXXXXXXXXXX
```

After upload, anyone can install with:
```bash
pip install dfpretty
```

---

## 3 · Publish to conda-forge

conda-forge is a community channel. Publishing there requires a PR to their
feedstock repository. It takes ~1–2 days but then users can install via:

```bash
conda install -c conda-forge dfpretty
```

### 3a · Fork conda-forge/staged-recipes

Go to https://github.com/conda-forge/staged-recipes and fork it.

### 3b · Create the recipe

```bash
git clone https://github.com/YOUR_USERNAME/staged-recipes
cd staged-recipes
mkdir recipes/dfpretty
```

Create `recipes/dfpretty/meta.yaml`:

```yaml
{% set name = "dfpretty" %}
{% set version = "0.1.0" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.io/packages/source/{{ name[0] }}/{{ name }}/dfpretty-{{ version }}.tar.gz
  sha256: <PASTE SHA256 FROM PyPI HERE>   # see step 3c

build:
  noarch: python
  number: 0
  script: {{ PYTHON }} -m pip install . -vv --no-deps --no-build-isolation

requirements:
  host:
    - python >=3.9
    - pip
    - setuptools >=68
  run:
    - python >=3.9
    - pandas >=1.5

test:
  imports:
    - dfpretty
  commands:
    - pip check
  requires:
    - pip

about:
  home: https://github.com/YOUR_USERNAME/dfpretty
  summary: "Pretty-print pandas DataFrames as styled interactive HTML tables"
  license: MIT
  license_file: LICENSE

extra:
  recipe-maintainers:
    - YOUR_GITHUB_USERNAME
```

### 3c · Get the SHA256 hash

```bash
pip download dfpretty==0.1.0 --no-deps -d /tmp/pkg
sha256sum /tmp/pkg/dfpretty-0.1.0.tar.gz
```

Paste that hash in `meta.yaml`.

### 3d · Open the PR

```bash
git add recipes/dfpretty/
git commit -m "Add dfpretty recipe"
git push
```

Go to https://github.com/conda-forge/staged-recipes and open a Pull Request.
The CI will run automatically. A conda-forge bot will review and merge it
(usually within 1–2 days). After merge, a `dfpretty-feedstock` repo is
auto-created and the package appears on conda-forge within minutes.

---

## 4 · Releasing new versions

```bash
# 1. Bump version in pyproject.toml and __init__.py
# 2. Commit + tag
git tag v0.2.0
git push origin v0.2.0

# 3. Build & upload to PyPI
python -m build
twine upload dist/*

# 4. Update conda-forge feedstock
#    Go to https://github.com/conda-forge/dfpretty-feedstock
#    Open a PR bumping version + sha256 in recipe/meta.yaml
#    (or wait — the regro-cf-autotick-bot does this automatically within ~24h)
```

---

## Quick reference

| Step | Command |
|---|---|
| Build | `python -m build` |
| Test upload | `twine upload --repository testpypi dist/*` |
| Production upload | `twine upload dist/*` |
| Run tests | `pytest` |
| Check package | `twine check dist/*` |
