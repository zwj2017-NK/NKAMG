#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''nmap_scanner

APIs:
    class NmapScanner:
        function scan()

'''

import subprocess
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
# customized lib
from port import Port       # Port is a dict class for storing port info such ad id and protocol

class NmapScanner(object):
    def __init__(self, dest_file = None):
        if dest_file:
            self._dest_file = dest_file
        else:
            # TODO: I am not sure if I need to get abs path
            pwd = os.path.dirname(__file__)
            sep = os.path.sep
            self._dest_file = pwd + sep + '..' + sep + 'data' + sep + 'default.csv'

    def get_port_by_ip(self, ip):
        tmp_file = '~tmp~.xml'
        cmd = 'nmap %s -oX %s' % ip, tmp_file
        subprocess.call(cmd, shell = True)
        ports = self._read_xml(tmp_file)

    def _read_xml(self, xml):
        tree = ET.ElementTree(file = xml)
        ports = []
        for item in tree.iter(tag = 'port'):
            port = Port()
            port['portid'] = item.get('portid')
            port['protocol'] = item.get('protocol')
            for child in item:
                if child.tag == 'state':
                    port['state'] = child.get('state')
                elif child.tag == 'service':
                    port['name'] = child.get('name')
            ports.append(port)
        return ports

    def nmap(host):
        # nmap opts: 
        # -T<0-5>: Set timing template (higher is faster)
        # -v: Increase verbosity level (use -vv or more for greater effect)
        # -A: Enable OS detection, version detection, script scanning, and traceroute
        # -Pn: Treat all hosts as online -- skip host discovery
        cmd = 'sudo nmap -T4 -A -v -Pn %s' %host
        output = subprocess.check_output(cmd, shell = True)
        print(output)

    @property
    def dest_file(self):
        return self._dest_file

def main(host):
    s = NmapScanner()
    ports = s._read_xml('default.xml')
    for port in ports:
        print(port)
    print(s.dest_file)
    return
    
if __name__ == '__main__':
    host = '45.33.32.156'     # scanme.nmap.org
    main(host)
