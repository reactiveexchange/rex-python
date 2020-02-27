# REX Python

## Getting Started

Start by creating a virtual environment and installing required packages:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the tests:

```bash
$ python setup.py test
```

Deactivate the virtual environment when you are done:

```bash
$ deactivate
```

## Upgrade Dependencies

Dependencies can be upgraded as follows:

```bash
$ pip install pip-tools
$ pip-compile requirements.in >requirements.txt
$ pip install -r requirements.txt
```

## Testing

Run the tests:

```bash
$ python setup.py test
```

Run nosestests:

```bash
$ pip install coverage flake8 nose pylint
$ python setup.py nosetests
```

Generate coverage report:

```bash
$ python setup.py nosetests --cover-html --cover-html-dir=DIR
```

Run tox:

```bash
$ pip install tox
$ tox
```

## Installation

Install locally:

```bash
$ pip install .
```

## Build Python Package

Build Python package:

```bash
$ python setup.py sdist
```

Build wheel:

```bash
$ python setup.py bdist_wheel
```
