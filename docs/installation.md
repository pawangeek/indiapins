Installation
============

Install from PyPI
-----------------

The recommended way is installing the latest stable package from PyPI:

```
$ pip install indiapins
```

This installs the package and the `indiapins` CLI entry point.

Python requirement:

- Python 3.11 or newer

If `pip` is not available, install/update it first:

```
$ python -m pip install --upgrade pip
```

From Source (Local Development)
-------------------------------

Clone the repository and install locally:

```
$ git clone https://github.com/pawangeek/indiapins.git
$ cd indiapins
$ pip install .
```

For editable installs during development:

```
$ pip install -e .
```

Verify Installation
-------------------

Quick import check:

```
$ python -c "import indiapins; print(indiapins.__version__)"
```

Quick function check:

```
$ python -c "import indiapins; print(indiapins.isvalid('110001'))"
```

Expected output is `True` for the second command.

Useful Links
------------

- Project homepage: https://github.com/pawangeek/indiapins
- Package on PyPI: https://pypi.org/project/indiapins/
- Documentation: https://pawangeek.github.io/indiapins/
