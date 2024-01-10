#!/bin/bash

RED="\033[31m"
YELLOW="\033[33m"
GREEN="\033[32m"
RESET="\033[0m"

print_green() {
  echo -e "${GREEN}${1}${RESET}"
}

print_green "[+] Start Compiling query suites"

# get all query suites except Java
ls /root/codeql-home/codeql-repo/*/ql/src/codeql-suites/*.qls | grep -v 'csharp' >> /tmp/list-querysuites

while IFS="" read -r qs || [ -n "$qs" ]
do
  print_green "[+] Compiling query suites: $qs"
  codeql query compile --threads=50 --ram=4096 $qs
done < /tmp/list-querysuites

print_green "[+] Done Compiling query suites ..."