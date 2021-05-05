#!/bin/bash

RED="\033[31m"
YELLOW="\033[33m"
GREEN="\033[32m"
RESET="\033[0m"

print_green() {
    echo -e "${GREEN}${1}${RESET}"
}

SRC=/opt/src
if [ -z $FORMAT ]
then
    FORMAT="sarif-latest"
fi

if [ -z $QS ]
then
    QS="$LANGUAGE-security-and-quality.qls"
fi

if [ -z $OUTPUT ]
then
    OUTPUT="/opt/results"
fi
DB=$SRC/codeql-db

echo "----------------"
print_green " [+] Language: $LANGUAGE"
print_green " [+] Query-suites: $QS"
print_green " [+] Database: $DB"
print_green " [+] Source: $SRC"
print_green " [+] Output: $OUTPUT"
print_green " [+] Format: $FORMAT"
echo "----------------"

echo -e "Creating DB: codeql database create --language=$LANGUAGE $DB -s $SRC"
codeql database create --language=$LANGUAGE $DB -s $SRC

echo -e "Start Scanning: codeql database analyze --format=$FORMAT --output=$OUTPUT/issues.$FORMAT $DB $QS"
codeql database analyze --format=$FORMAT --output=$OUTPUT/issues.$FORMAT $DB $QS
