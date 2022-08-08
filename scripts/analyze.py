#!/usr/bin/env python3
from genericpath import isfile
import os
import sys
import argparse
import subprocess

# bash colors
RED="\033[31m"
YELLOW="\033[33m"
CYAN="\033[96m"
GREEN="\033[32m"
RESET="\033[0m"

# provided inputs
SRC = ""
LANGUAGE = ""
OVERRIDE = False
OUTPUT = ""
DB = ""
LANG = ""
FORMAT = ""
QS = ""
QUERIES = []

# pre-defined query suite
QPACKS_SUITE = []
QUERIES_SUITE = []

def get_qs():
  global QPACKS_SUITE, QUERIES_SUITE
  print(f"[+]{GREEN} Get List of Query Suites & Query Packs {RESET}")
  # getting all query packs
  cmd = f"codeql resolve qlpacks --format=json | jq -r 'keys[]'"
  packs = subprocess.Popen([cmd], shell=True, stdin=None, stdout=subprocess.PIPE, stderr=None, close_fds=True).stdout.readlines()
  for line in packs:
    pack = line.decode('utf-8').strip()
    QPACKS_SUITE.append(pack)

  # geting all queries suites
  if os.path.isfile("/tmp/list-querysuites"):
    # reading all the queries suites from file
    with open("/tmp/list-querysuites", "r") as f:
      rawQuery = f.readlines()
    for queryPath in rawQuery:
      query = os.path.basename(queryPath).strip()
      QUERIES_SUITE.append(query)


def picking_qpack(lang):
  global QUERIES
  query = f"codeql/{lang}-queries"
  for qs in QPACKS_SUITE:
    if query == qs:
      QUERIES.append(query)
  # picking default query based on language
  QUERIES.append(f"{lang}-security-and-quality.qls")
  return QUERIES

def picking_query(query):
  queries = []
  for qs in QUERIES_SUITE:
    if query in qs:
      queries.append(qs)
  if len(queries) == 0:
    print(f"[-]{RED} No Query Suite matchs: {CYAN}{query} {RESET}")
  return queries

def build_db():
  buildCmd = f"codeql database create --language={LANGUAGE} {DB} -s {SRC}"
  print(f"[+]{CYAN} ==> Creating Database: {GREEN} {buildCmd} {RESET}")
  if not os.path.exists(DB):
    os.system(buildCmd)
  else:
    if OVERRIDE == True:
      buildCmd = f"codeql database create --overwrite --language={LANGUAGE} {DB} -s {SRC}"
      os.system(buildCmd)
      return
    print(f"[-]{GREEN} ==> Database already exist at {RESET}{DB}")
    print(f"[+]{GREEN} ==> Set ENV {RESET}'OVERRIDE=True'{GREEN} if you want to override it {RESET}")

def start_analyze(query):
  if query not in QUERIES_SUITE and query not in QPACKS_SUITE:
    print(f"[-] {RED} Query Suite not found: {CYAN}{query} {RESET}")
    return -1
  output = f"issues-{query}.{FORMAT}".replace(" ", "-").replace("/", "-")
  analyzeCmd = f"codeql database analyze --format={FORMAT} --output={OUTPUT}/{output} {DB} {query}"
  print(f"[+]{CYAN} ==> Start analyze with query {GREEN}{query}{RESET}: {analyzeCmd}")
  os.system(analyzeCmd)

def parse_input(args):
  global SRC, OUTPUT, LANGUAGE, FORMAT, QUERIES, QS, DB, OVERRIDE
  SRC = args.src
  if not os.path.exists(SRC):
    print(f"[+]{RED} Source folder {RESET}{SRC}{RED} not found")
    os.exit(-1)

  LANGUAGE = args.language
  FORMAT = args.format
  DB = args.database
  if args.query is not None:
    QUERIES.append(args.query)
  OVERRIDE = args.override

  OUTPUT = os.path.abspath(args.output)
  if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)

  # check if we have anything from ENV
  if 'FORMAT' in os.environ:
    FORMAT = os.environ.get('FORMAT')
  if 'OVERRIDE' in os.environ:
    OVERRIDE = True
  if 'LANGUAGE' in os.environ:
    LANGUAGE = os.environ.get('LANGUAGE')
  if 'QS' in os.environ:
    QS = os.environ.get('QS')
    QUERIES.append(QS)

  banner()
  if len(QUERIES) > 0:
    runningQueries = []
    for query in QUERIES:
      runningQueries += picking_query(query)
    QUERIES = runningQueries
  
  # pick the query pack from the provided language
  QUERIES += picking_qpack(LANGUAGE)
  QUERIES = sorted(set(QUERIES))
  if QUERIES == "" or QUERIES == []:
    print(f"[-]{RED} Query Suite not found for language: {CYAN}{LANGUAGE} {RESET}")
    sys.exit(-1)
  else:
    print(f"[+]{GREEN} Picking Query Suite from language {LANGUAGE}: {CYAN}{QUERIES} {RESET}")
  

def banner():
  print(f"{GREEN}------------------{RESET}")
  print(f"{GREEN}>>> Provided Inputs{RESET}")
  print(f"{GREEN}[+] Language: {RESET}{LANGUAGE}")
  print(f"{GREEN}[+] Query-suites: {RESET}{QS}")
  print(f"{GREEN}[+] Database: {RESET}{DB}")
  print(f"{GREEN}[+] Source: {RESET}{SRC}")
  print(f"{GREEN}[+] Output: {RESET}{OUTPUT}")
  print(f"{GREEN}[+] Format: {RESET}{FORMAT}")
  print(f"{GREEN}------------------{RESET}")

def main():
  parser = argparse.ArgumentParser(description="Script to start CodeQL Analyze")
  parser.add_argument('--format', nargs='?', type=str, default="sarif-latest", help='Format of output')
  parser.add_argument('-o', '--output', nargs='?', type=str, default="/opt/results", help='Output folder to store result')
  parser.add_argument('-d', '--database', nargs='?', type=str, default="/opt/src/codeql-db", help='CodeQL database for a source tree')
  parser.add_argument('-s', '--src', nargs='?', type=str, default="/opt/src", help='Folder of source code to analyze')
  parser.add_argument('-l', '--language', nargs='?', type=str, help='Language to run analyze')
  parser.add_argument('-q', '--query', nargs='?', type=str, help='Query Suite to run analyze')
  parser.add_argument('-r', '--override', nargs='?', type=bool, help='Override existing database')

  args = parser.parse_args()
  if len(sys.argv) == 1 and 'LANGUAGE' not in os.environ:
    print('''
    Usage:
      python analyze.py -s <source-core> -l <language> -q <query-suite> -d <database> -o <output> -f <format>
    ''')
    sys.exit(0)

  get_qs()
  parse_input(args)
  build_db()
  # really start to run the query
  for query in QUERIES:
    start_analyze(query)

  for file in os.listdir(OUTPUT):
      if file.startswith("issues-"):
        result = os.path.join(OUTPUT, file)
        print(f"[+]{GREEN} Detail Issue Store at: {CYAN}{result} {RESET}")

if __name__ == '__main__':
  main()
