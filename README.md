# pytest-ansible-units

![VScode Overview](images/vscode_overview.png)
![VScode Debug](images/vscode_debug.png)


An experimental `pytest` plugin to run an ansible collection's unit tests with `pytest`.

## Description

`pytest-ansible-units` is a `pytest` plugin that allows an ansible collection's unit tests to be run with only `pytest`.  `pytest` can be used from the command line or from the IDE.

## Getting Started

### Dependencies

Installing `pytest-ansible-units` will install the following:

* `ansible-core`
* `pytest`
* `pyyaml`

`pytest-ansible-units` requires python 3.8 or greater.

### Installing


```
python -m pip install pytest-ansible-units
```

2 directory structures are supported, with either approach collection dependencies need to be installed. Either in the default user location or in the collection tree structure in option 1.


#### Collection tree

The preferred approach is to clone the collections being developed into it's proper collection tree path. This eliminates the need for any symlinks and other collections being developed can be cloned into the same tree structure.

```
git clone <repo> collections/ansible_collections/<namepspace>/<name>
```

Note:

* `pytest` needs to be run in the root of the collection directory, adjacent to the collection's galaxy.yml file

#### Shallow tree

The alternative approach allow for a shallow directory structure.

```
git clone <repo> 
```

Notes:

* `pytest` needs to be run in the root of the collection directory, adjacent to the collection's galaxy.yml file
* A collections directory will be created in the repository directory and the collections content linked into it.
* Add `/collections/` to the .gitignore, since there is no need for this to be checked in.
* `ansible-test sanity` will fail due to the symlinks, with this approach.


### Executing program

From the command line, from the collection's root directory:

```
pytest tests
```

## Help

The following may be added to the collections' `pyproject.toml` file to limit warnings and set the default path for the collection's tests

```
[tool.pytest.ini_options]
testpaths = [
    "tests",
]
filterwarnings = [
    'ignore:AnsibleCollectionFinder has already been configured',
]
```

Information from the `galaxy.yml` file is used to build the `collections` directory structure and link the contents. The `galaxy.yml` file should reflect the correct collection namespace and name.

One way to detect issues without running the tests is to run:

```
pytest --collect-only
```

The follow errors may be seen:

```
E   ModuleNotFoundError: No module named 'ansible_collections'
```

* Check the `galaxy.yml` file for an accurate namespace and name
* Ensure `pytest` is being run from the collection's root directory, adjacent to the `galaxy.yml`

```
HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules
```

* Ensure each test directory has an `__init__.py`


## Authors

* cidrblock

## License

This project is licensed under the GPL-v3 License - see the LICENSE file for details
