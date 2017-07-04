#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Specifying the host (host can be ip, a range of ip, the whole subnet, and domain), and some options to start scanning by using nmap.

Typical Usage:
    scan <host>             This command is equivalent to nmap command 'sudo nmap -O <host>'

Usage:
    scan <host> [options]
    scan -h|--help
    scan -V|--version

Options:
    -Pn                     equal to nmap command -Pn
    --version, -V           show version info
    --help, -h

The host can be composed with the following formats:
    192.168.0.1             scanning single ip
    192.168.0.1-20          scanning a range of ips from 1 to 20
    192.168.0.0/24          scanning the subnet
    scanme.nmap.org         scanning by domain

'''

import sys, getopt
import argparse

__version__ = '0.1'

def get_parser():
    parser = argparse.ArgumentParser()

    # specify hosts
    parser.add_argument('host', help = 'specify the host here', nargs = '+')

    # -Pn
    parser.add_argument('-Pn', help = 'equal to nmap option -Pn', action = 'store_true')

    parser.add_argument('--version', '-V', action = 'version', version = __version__)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    nmap_cmd = 'sudo '
    nmap_cmd += 'nmap -O '
    if args.Pn:
        nmap_cmd += '-Pn '
    nmap_cmd += ' '.join(args.host)
    print(nmap_cmd)

if __name__ == '__main__':
    main()
