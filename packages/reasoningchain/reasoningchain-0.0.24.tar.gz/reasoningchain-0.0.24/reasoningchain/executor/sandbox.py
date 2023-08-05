#!/usr/bin/env python3

import os
import sys
import subprocess

def execute_python(codes:str) -> str:
    codes = codes.strip()
    if codes.startswith('```'):
        parts = codes.split('\n', 1)
        if len(parts) == 1:
            codes = codes.strip('`')
        else:
            codes = parts[1].rstrip('`')
    codes = codes.strip().strip('`')
    #print("execute_python:{\n%s\n}" % codes)

    cp = subprocess.Popen(["python3", "-c", codes], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = cp.communicate()[0].decode().strip()
    if cp.returncode != 0:
        out += f'\n\nProcess exited abnormally with exit code {cp.returncode}'
    return out

if __name__ == '__main__':
    codes = ''
    for line in sys.stdin:
        codes += line
    execute(codes)

