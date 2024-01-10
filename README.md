# Docker for CodeQL

Based on [microsoft/codeql-container](https://github.com/microsoft/codeql-container) with Java, Golang installed and .NET removed.

## Build & Run

```shell
docker build -t j3ssie/codeql-docker:latest .
```

or pull the latest from Docker hub

```shell
docker pull j3ssie/codeql-docker:latest

```
***

## Usage

### Run with helper scripts

```shell
# usage
./scripts/run.py -l <language-of-source-code> -s <source-code-folder> [--format=csv] [-o ouput]

# simple usage
./scripts/run.py -l go -s /tmp/insecure-project
# default output is JSON format so read them with this command
cat results/issues.sarif-latest| jq '.runs[].results'

# with custom format and output
./scripts/run.py -l javascript -s /tmp/cc/code-scanning-javascript-demo --format=csv -o sample
# your output will be store at sample/issues.csv

```

### Run with docker command

With `/tmp/src` is your source code and `/tmp/results` is where result store.

> NOTE: make sure /tmp/results folder exist otherwise it won't work

```shell
# run in the current folder
mkdir -p ${PWD}/codeql-result
docker run --rm --name codeql-docker -v ${PWD}:/opt/src -v ${PWD}/codeql-result:/opt/results -e "LANGUAGE=javascript" -e "THREADS=5" j3ssie/codeql-docker:latest

# simple usage
docker run --rm --name codeql-docker -v "/tmp/src:/opt/src" -v "/tmp/local-results:/opt/results" -e "LANGUAGE=go" j3ssie/codeql-docker:latest

# more options
docker run --rm --name codeql-docker -v "/tmp/src:/opt/src" -v "/tmp/local-results:/opt/results" -e "LANGUAGE=javascript" -e "FORMAT=csv" -e "QS=javascript-security-and-quality.qls" j3ssie/codeql-docker:latest

```

### Manual analyze

```shell
# Directly access container with bash shell
docker run -it --entrypoint=/bin/bash -t j3ssie/codeql-docker:latest

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
