## cs-models

This package provides a reusable library to connect to the cs database.

### Setup

1. Install `pyenv`
    ```bash
    brew install pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
    ```
2. Install Python
    ```bash
    pyenv install
    ```
3. Setup project
    ```bash
    chmod a+x bin/*
    . ./bin/bootstrap.sh
    ```

### Commands

**List commands**

`inv -l`

### Usage

**Configure the database in your app**

```
from silver_surfer_models.database import get_db_session

db_uri = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4' % (
    'root',
    'password',
    'host',
    'db',
)
engine, db_session, Base = database.get_db_session(db_uri)

```

### How to release a new version?

**Update the `version` in `setup.py`**

```
setuptools.setup(
    ...
    version='0.0.9',
    ...
)
```

**Publish to PyPI repository**

```inv deploy```
