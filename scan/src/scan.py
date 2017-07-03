#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Specifying the host (host can be ip, a range of ip, the whole subnet, and domain), and some options to start scanning by using nmap.

Usage:
    scan <host> [options]
    scan -h|--help
    scan -V|--version

Options:
    --sudo
    --version, -V
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

    # require sudo
    parser.add_argument('--sudo', help = 'execute nmap command with sudo', action = 'store_true')

    parser.add_argument('--version', '-V', action = 'version', version = __version__)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    nmap_cmd = ''
    if args.sudo:
        nmap_cmd += 'sudo '
    nmap_cmd += 'nmap -A -Pn ' + ' '.join(args.host)
    print(nmap_cmd)

if __name__ == '__main__':
    main()
