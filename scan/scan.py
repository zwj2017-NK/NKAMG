#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''active scanner

In this version, (I'm sorry but) you have to run the program by using 'python scan.py [options]'

Usage:
    scan -i <ip> [-o]
    scan -h|--help
    scan --version

Options:
    -h --help               show help page
    --version               show version info
    -i --ip=<ip>            scan by given ip
'''

import sys, getopt

from src.nmap import NmapScanner

__version__ = '0.1'

def main():
    args = docopt.docopt(__doc__, version = __version__)
    print(args)
    ip = args['--ip']

    info = NmapScanner()
    return

if __name__ == '__main__':
    main()
