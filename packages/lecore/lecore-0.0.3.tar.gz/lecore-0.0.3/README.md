# LE core package

This is package of core python utils for LE.

# Build

In command line (not venv) run:

Update PIP, build, twine
```
python -m pip install --upgrade build
python -m pip install --upgrade pip
python -m pip install --upgrade twine
```

Run Build
````
py -m build
````

# Upload to test

Upload package to test.pypi.org server

```
py -m twine upload --repository testpypi dist/*
```

# Download from test pypi

