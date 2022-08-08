#!/usr/bin/env python3

import os
import sys
import argparse

# bash colors
RED="\033[31m"
YELLOW="\033[33m"
CYAN="\033[96m"
GREEN="\033[32m"
RESET="\033[0m"

IMAGE_NAME = "j3ssie/codeql-docker:latest"

SRC = ""
OUTPUT = ""
UPDATE = False
DOCKER_CMD = ""
LANG = ""
FORMAT = ""
QS = ""
ANALYZE_OUTPUT = "beautify-issues.txt"

def update_docker():
  if not UPDATE:
    return
  PULL_CMD = "docker pull j3ssie/codeql-docker:latest"
  print(f"[+]{GREEN} Update the latest docker: {RESET}{PULL_CMD}")
  os.system(PULL_CMD)

def start_analyze():
  print(f"[+]{GREEN} Start Analyze: {RESET}{DOCKER_CMD}")
  os.system(DOCKER_CMD)
  # proc = subprocess.Popen([DOCKER_CMD], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
  # print(f"[+]{GREEN} Start docker with process ID: {0}".format(proc.pid))
  # return proc.pid

def parse_input(args):
  global SRC, OUTPUT, DOCKER_CMD, LANG, FORMAT, QS, ANALYZE_OUTPUT, UPDATE
  SRC = args.src
  UPDATE = False if args.no_update is None else True
  if not os.path.isdir(SRC):
    print(f"[-]{RED} Source code folder not exist: {SRC}")
    os.exit(-1)

  LANG = args.lang
  FORMAT = args.format
  OUTPUT = os.path.abspath(args.output)
  if not os.path.isdir(OUTPUT):
    os.makedirs(OUTPUT)

  DOCKER_CMD = f'''docker run --rm --name codeql-docker -v "{SRC}:/opt/src" -v "{OUTPUT}:/opt/results" -e "LANGUAGE={LANG}" -e "FORMAT={FORMAT}"'''
  if args.query:
    QS = args.query
    DOCKER_CMD = f'''docker run --rm --name codeql-docker -v "{SRC}:/opt/src" -v "{OUTPUT}:/opt/results" -e "LANGUAGE={LANG}" -e "FORMAT={FORMAT}" -e "QS={QS}"'''
  if args.override:
    DOCKER_CMD += ' -e "OVERRIDE=true"'
  DOCKER_CMD += f'  {IMAGE_NAME}'

def main():
  parser = argparse.ArgumentParser(description="Script to start CodeQL Analyze")
  parser.add_argument('--format', nargs='?', type=str, default="sarif-latest", help='Format of output')
  parser.add_argument('-o', '--output', nargs='?', type=str, default="results", help='Output folder to store result')
  parser.add_argument('-s', '--src', nargs='?', type=str, required=True, help='Folder of source code to analyze')
  parser.add_argument('-l', '--lang', nargs='?', type=str, required=True, help='Language to run analyze')
  parser.add_argument('-q', '--query', nargs='?', type=str, help='Query Suite to run analyze')
  parser.add_argument('-n', '--no-update', nargs='?', type=bool, help='Disable auto update docker')
  parser.add_argument('-r', '--override', nargs='?', type=bool, help='Override existing database')

  args = parser.parse_args()
  if len(sys.argv) == 1:
    print('''
    Usage:
      python run.py -s <source_code_folder> -l <language> -o <output_folder> -f <format> -q <query_suite>
    ''')
    sys.exit(0)

  parse_input(args)
  update_docker()
  start_analyze()
  for file in os.listdir(OUTPUT):
      if file.startswith("issues-"):
        result = os.path.join(OUTPUT, file)
        print(f"[+]{GREEN} Detail Issue in host machine: {CYAN}{result} {RESET}")

if __name__ == '__main__':
  main()
