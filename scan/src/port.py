#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Port(dict):
    __slots__ = ('protocol', 
            'portid',       # e.g. 80/tcp
            'state',        # open / filtered
            'name',         # service name
            )
