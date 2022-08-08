# Docker for CodeQL

Based on [microsoft/codeql-container](https://github.com/microsoft/codeql-container) with Java, Golang installed and .NET removed.

## Build & Run

```shell
docker build -t j3ssie/codeql-docker:latest .
```

or pull the latest from [Docker hub](https://hub.docker.com/r/j3ssie/codeql-docker)

```shell
docker pull j3ssie/codeql-docker:latest

```

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
# simple usage which will run the QL Packs of that language
docker run --rm --name codeql-docker -v "/tmp/src:/opt/src" -v "/tmp/results:/opt/results" -e "LANGUAGE=go" j3ssie/codeql-docker:latest

# Run with specific Queries Suite and different output format
docker run --rm --name codeql-docker -v "/tmp/src:/opt/src" -v "/tmp/results:/opt/results" -e "LANGUAGE=javascript" -e "FORMAT=csv" -e "QS=javascript-security-and-quality.qls" j3ssie/codeql-docker:latest

# Override the source code DB tree
docker run --rm --name codeql-docker -v "/tmp/src:/opt/src" -v "/tmp/results:/opt/results" -e "LANGUAGE=javascript" -e "FORMAT=csv" -e "QS=javascript-security-and-quality.qls" -e "OVERRIDE=True" j3ssie/codeql-docker:latest

```

### Manual analyze

```shell
# Directly access container with bash shell
docker run -it --entrypoint=/bin/bash -t j3ssie/codeql-docker:latest

# Copy your code to container
docker cp <your-source-cde> <docker-ID>:/opt/src

# You use the helper scripts to run CodeQL
python3 analyze.py -d /opt/src/db -s /opt/src/ -l javascript --override=True

# Or using raw command from codeQL
## create DB in this folder /opt/src/db
## This might take a while depend on your code
codeql database create --language=<language> /opt/src/db -s /opt/src

## run analyze
## normally query-suites will will be: <language>-security-and-quality.qls
codeql database analyze --format=sarif-latest --output=/opt/issues.sarif /opt/src/db <query-suites>

# copy the result back to host machine
docker cp <docker-ID>:/opt/issues.sarif .
```

### Other commands

```shell
# List all query packs
codeql resolve qlpacks --format=json | jq -r 'keys[]'

# List all query suites
codeql resolve queries

# Upgrade DB
codeql database upgrade <database>

# Building the base image
docker build -f base-image-Dockerfile -t j3ssie/codeql-base:latest .
```

## Donation

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/j3ssiejjj)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/j3ssie)
