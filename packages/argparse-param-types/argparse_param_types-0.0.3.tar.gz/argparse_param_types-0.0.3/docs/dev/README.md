# Dev guide for argparse_param_types
## Development requirements on project
When contributing to the project, there are several requirements that applies to ensure code consistency and code quality. The requirements are ase follow:
- Code style follows PEP8
  - Using `black` and `isort`
- Documentation is done with docstrings restructuredtext
- Type hinting is provided
- Only supports Python3

## How to package the project
### Dependencies
```
pip install build twine black flake8 flake8-import-order isort
```

### Style checks
```
black --check --line-length 79 --target-version py310 .
flake8
```

### Auto format
```
black --line-length 79 --target-version py310 .
isort --profile black -l 79 .
```

### Run unit tests
```
pip install -e .
pytest
```

### Build & upload
#### Production environment
```
python -m build
python -m twine upload --repository-url https://upload.pypi.org/legacy/ --repository argparse-param-types dist/*
```

#### Test environment
```
python -m build
python -m twine upload --repository-url https://test.pypi.org/legacy/ --repository argparse-param-types dist/*
```



http://www.sefidian.com/2021/08/03/how-to-use-black-flake8-and-isort-to-format-python-codes/
https://medium.com/mlearning-ai/python-auto-formatter-autopep8-vs-black-and-some-practical-tips-e71adb24aee1


tox
https://github.com/pyca/pyopenssl/blob/main/tox.ini

pip install -e .
