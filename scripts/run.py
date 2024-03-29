#!/usr/bin/env python3

import os
import sys
import argparse

SRC = ""
OUTPUT = ""
DOCKER_CMD = ""
LANG = ""
FORMAT = ""
QS = ""
THREADS = ""
ANALYZE_OUTPUT = "beautify-issues.txt"

def update_docker():
  PULL_CMD = "docker pull j3ssie/codeql-docker:latest"
  print(f"Update the latest docker: {PULL_CMD}")
  os.system(PULL_CMD)

def start_analyze():
  print(f"==> Start Analyze:: \033[1;32m{DOCKER_CMD}\033[0m")

  os.system(DOCKER_CMD)
  # proc = subprocess.Popen([DOCKER_CMD], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
  # print("Start docker with process ID: {0}".format(proc.pid))
  # return proc.pid

def parse_input(args):
  global SRC, OUTPUT, DOCKER_CMD, LANG, FORMAT, QS, ANALYZE_OUTPUT, THREADS
  SRC = args.src
  if not os.path.isdir(SRC):
    print(f"[-] Source code folder not exist: {SRC}")
    os.exit(-1)

  LANG = args.lang
  FORMAT = args.format
  THREADS = args.threads

  OUTPUT = os.path.abspath(args.output)
  if not os.path.isdir(OUTPUT):
    print(f"[-] Output folder not exist, create new one: {OUTPUT}")
    os.makedirs(OUTPUT)

  if not args.query:
    QS = f"{LANG}-security-and-quality.qls"

  DOCKER_CMD = f'''docker run --rm --name codeql-docker -v "{SRC}:/opt/src" -v "{OUTPUT}:/opt/results" -e "LANGUAGE={LANG}" -e "FORMAT={FORMAT}" -e "QS={QS}" -e "THREADS={THREADS}" j3ssie/codeql-docker:latest'''


def main():
  parser = argparse.ArgumentParser(description="Script to start CodeQL Analyze")
  parser.add_argument('--format', nargs='?', type=str, default="sarif-latest", help='Format of output')
  parser.add_argument('-o', '--output', nargs='?', type=str, default="results", help='Output folder to store result')
  parser.add_argument('-s', '--src', nargs='?', type=str, required=True, help='Folder of source code to analyze')
  parser.add_argument('-l', '--lang', nargs='?', type=str, required=True, help='Language to run analyze')
  parser.add_argument('-q', '--query', nargs='?', type=str, help='Query Suite to run analyze')
  parser.add_argument('-j', '--threads', nargs='?', default=20, type=int, help='Number of threads to evaluate queries.')

  args = parser.parse_args()
  if len(sys.argv) == 1:
    sys.exit(0)

  parse_input(args)
  update_docker()
  start_analyze()
  print(f"[+] Detail Issue Store at: \033[1;32m{OUTPUT}/issues.{FORMAT}\033[0m")

if __name__ == '__main__':
  main()