#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
# customized lib
from host_info import Host, Port

class NmapScanner(object):
    # cmd is a string of a nmap command
    def __init__(self, command):
        self._cmd = command
        self._tmp_file = '~tmp~.xml'
        self._tree = None

    def get_info(self):
        self._scan_with_xml_output()
        self._tree = ET.ElementTree(file = self._tmp_file)
        info = self._get_info_by_host()
        return info

    def _scan_with_xml_output(self):
        if '-oX' not in self._cmd:
            self._cmd += ' -oX ' + self._tmp_file
        else:
            # TODO: may be send message to server
            exit('command error')
        subprocess.call(self._cmd, shell = True)
        return

    # -----------------------------------------------------------------------
    # pattern in xml file is like:
    # <host>
    #   <address addr="127.0.0.1" addrtype="ipv4"/>
    #   <ports>
    #       <port protocol="tcp" portid="22">
    #           <state state="open" reason="syn-ack" reason_ttl="0"/>
    #           <service name="ssh" method="table" conf="3"/>
    #       </port>
    #   </ports>
    #   <os>
    #       <osmatch name="FreeBSD 6.2-RELEASE">
    #       </osmatch>
    #   <os>
    # </host>
    # <host>
    # ...
    def _get_info_by_host(self):
        hosts = []
        for host_layer in self._tree.iter(tag = 'host'):
            host = Host()
            ip = host_layer.find('address').get('addr')
            host['ip'] = ip

            # extracting ports from xml file
            ports = []
            for port_layer in self._tree.iter(tag = 'port'):
                port = Port()
                port['portid'] = port_layer.get('portid')
                port['protocol'] = port_layer.get('protocol')
                for port_detail_layer in port_layer:
                    if port_detail_layer.tag == 'state':
                        port['state'] = port_detail_layer.get('state')
                    elif port_detail_layer.tag == 'service':
                        port['name'] = port_detail_layer.get('name')
                ports.append(port)
            host['port'] = ports

            # extracting os info
            os = host_layer.find('os').find('osmatch').get('name')
            host['os'] = os

            hosts.append(host)
        return hosts


def main(host):
    cmd = 'nmap -A -Pn 127.0.0.1 scanme.nmap.org'
    s = NmapScanner(cmd)
    hosts = s.get_info()
    for host in hosts:
        print(host)
    return
    
if __name__ == '__main__':
    host = '45.33.32.156'     # scanme.nmap.org
    main(host)
