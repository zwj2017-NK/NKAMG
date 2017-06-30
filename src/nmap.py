#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''nmap_scanner

'''

import subprocess
import getopt, sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class Scanner(object):
    def __init__(self, dest_file = None):
        if dest_file:
            self._dest_file = dest_file
        else:
            self._dest_file = 'default.xml'

    def scan(self, host):
        cmd = 'nmap -oX %s %s' %(self.dest_file, host)

    def nmap(host):
        # nmap opts: 
        # -T<0-5>: Set timing template (higher is faster)
        # -v: Increase verbosity level (use -vv or more for greater effect)
        # -A: Enable OS detection, version detection, script scanning, and traceroute
        # -Pn: Treat all hosts as online -- skip host discovery
        cmd = 'sudo nmap -T4 -A -v -Pn %s' %host
        output = subprocess.check_output(cmd, shell = True)
        print(output)

        # match = [total, os_info]
        os_patterns = [
                r'Aggressive OS guesses:\s*(.+)',
                r'OS details:\s*(.*)',
                ]
        for pattern in os_patterns:
            if re.search(pattern, output):
                print(re.search(pattern, output).group(0))
            else:
                print('None')

        # match = [total, port_num/port_type, open|filtered, else_info]
        port_pattern = r'(\d+\/\w+)\s+(open|filtered)\s+(.+)'
        if re.finditer(port_pattern, output):
            # finditer return iterator of match objs while findall return string list
            for item in re.finditer(port_pattern, output):
                # do not use 'print(item[0])', it is the feature for py3.6
                print(item.group(0))
        else:
            print('None')
                
    def xml_parse(self):
        tree = ET.ElementTree(file = self.dest_file)
        return tree

    @property
    def dest_file(self):
        return self._dest_file

def main(host):
    '''
    try:
        import docopt
    except ImportError:
        exit('Please install python lib: docopt')

    args = docopt()
    '''
    s = Scanner()
    tree = s.xml_parse()
    for ele in tree.iter(tag = 'port'):
        print(ele.tag, ele.attrib)
    return
    
if __name__ == '__main__':
    host = '45.33.32.156'     # scanme.nmap.org
    main(host)
