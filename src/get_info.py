#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import subprocess
import re

def location(ip):
    cmd = 'curl -s ip.chinaz.com/%s' %ip
    html = subprocess.check_output(cmd, shell = True)
    #print(html)
    domtree = etree.HTML(html)
    location = domtree.xpath(u'//*[@id="leftinfo"]/div[3]/div[2]/p[2]/span[4]/text()')
    return location[0].encode('utf-8')

def nmap(ip):
    # nmap opts: 
    # -T<0-5>: Set timing template (higher is faster)
    # -v: Increase verbosity level (use -vv or more for greater effect)
    # -A: Enable OS detection, version detection, script scanning, and traceroute
    # -Pn: Treat all hosts as online -- skip host discovery
    cmd = 'sudo nmap -T4 -A -v -Pn %s' %ip
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
    
def main(ip):
    print(location(ip))
    nmap(ip)
    
if __name__ == '__main__':
    ip = '45.33.32.156'     # scanme.nmap.org
    main(ip)
