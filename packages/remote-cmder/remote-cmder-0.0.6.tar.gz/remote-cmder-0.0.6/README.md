# remote-cmder

## Prerequisites

### Deps:

```shell
poetry install
```

### pre-commit

```shell
pre-commit install --install-hooks
pre-commit install --hook-type pre-push
# update
pre-commit autoupdate
```

## Quick Start

### Start

```shell
$ python main.py
```

### MD5

```shell
$ curl -F 'file=@test.txt' -F 'file=@test.txt' http://127.0.0.1:8888/md5
================= test.txt =================
test.txt: ba1f2511fc30423bdbb183fe33f3dd0f
================= test.txt =================
test.txt: ba1f2511fc30423bdbb183fe33f3dd0f
```

## Run test

```shell
pytest .
# or
pytest --cov-config=.coveragerc --cov=. .
```

## Run Pylint

```shell
pylint *.py remote_cmder
```

## Docker

### Start

```shell
make build
make run
```

### Stop

```shell
make clean
```

## Podman

### Start

```shell
make -f Makefile.podman build
make -f Makefile.podman run
```

### Stop

```shell
make -f Makefile.podman clean
```
