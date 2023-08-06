# Contributing

Setting up different Python environments, we need to install all supported
Python version using [pyenv](https://github.com/pyenv/pyenv):

```bash
pyenv install 3.7.16
pyenv install 3.8.16
pyenv install 3.9.16
pyenv install 3.10.10
pyenv install 3.11.2
```

Setting up development environment and install dependencies:

```bash
python -m pip install --upgrade pip poetry
poetry install
poetry check
```

Create a virtualenv for the current running Python version:

```bash
$ poetry env list
txt2ebook-HLRzIsQs-py3.7 (Activated)
```

Show all available tox tasks:

```bash
$ tox -av
...
default environments:
py37    -> testing against python3.7
py38    -> testing against python3.8
py39    -> testing against python3.9
py310   -> testing against python3.10
py311   -> testing against python3.11

additional environments:
cover   -> generate code coverage report in html
doc     -> generate sphinx documentation in html
gettext -> update pot/po/mo files
```

To run specific test:

```bash
tox -e py37,py38,py39,py310,py311 -- tests/test_tokenizer.py
```

For code lint, we're using `pre-commit`:

```bash
pre-commit install # run once
pre-commit clean
pre-commit run --all-files
```

Or specific hook:

```bash
pre-commit run pylint -a
```

We're using zero-based versioning.

For patches or bug fixes:

```bash
poetry version patch
```

For feature release:

```bash
poetry version minor
```

# Create a Pull Request

Fork it at GitHub, http://github.com/kianmeng/txt2ebook/fork

Create your feature branch:

```bash
git checkout -b my-new-feature
```

Commit your changes:

```bash
git commit -am 'Add some feature'
```

Push to the branch:

```bash
git push origin my-new-feature
```

Create new Pull Request in GitHub.
