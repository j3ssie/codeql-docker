# CodeQL docker build

Based on [microsoft/codeql-container](https://github.com/microsoft/codeql-container) with java, golang installed and .NET removed.

## Build & Run

```shell
docker build -t j3ssie/codeql-docker:latest .
```

or pull the latest from docker hub

```shell
docker pull j3ssie/codeql-docker:latest

# then run the container
docker run -it j3ssie/codeql-docker:latest
```


## Usage

### Access container with bash shell

```shell
docker run -it --entrypoint=/bin/bash -t j3ssie/codeql-docker:latest /bin/bash
```

### Run with helper scripts

With `/tmp/src` is your source code and `/tmp/results` is where result store.

> NOTE: make sure /tmp/results folder is exist otherwise no result will be created

```shell
# simple usage
docker run --rm --name codeql-docker -v "/tmp/src:/opt/src" -v "/tmp/results:/opt/results" -e "LANGUAGE=go" j3ssie/codeql-docker:latest

# more options
docker run --rm --name codeql-docker -v "/tmp/src:/opt/src" -v "/tmp/results:/opt/results" -e "LANGUAGE=go" -e "FORMAT=csv" -e "QS=golang-security-and-quality.qls" j3ssie/codeql-docker:latest
```

### Manual analyze

```shell
# Copy your code to container
docker cp <your-source-cde> <docker-ID>:/opt/src

# create DB in this folder /opt/src/db
# This might take a while depend on your code
codeql database create --language=<language> /opt/src/db -s /opt/src

# run analyze
# normally query-suites will will be: <language>-security-and-quality.qls
codeql database analyze --format=sarif-latest --output=/opt/issues.sarif /opt/src/db <query-suites>

# copy the result back to host machine
docker cp <docker-ID>:/opt/issues.sarif .
```

### Other commands

```shell
# List all query suites
codeql resolve queries

# Upgrade DB
codeql database upgrade <database>

```
