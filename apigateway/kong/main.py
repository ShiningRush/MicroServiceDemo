#!/usr/bin/python3

from initor import init

import sys

def main():
    if len(sys.argv) < 2:
        print("please input enviroment")
        return
    
    if len(sys.argv) < 3:
        print("please input module")
        return

    init.init(sys.argv[1], sys.argv[2])

main()