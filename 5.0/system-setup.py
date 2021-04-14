#!/usr/bin/env python3

import sys
import os
import argparse

HERE=os.path.dirname(__file__)
READIES = os.path.join(HERE, "deps/readies")
if not os.path.exists(READIES):
    # not in docker
    READIES = os.path.join(HERE, "../deps/readies")
sys.path.insert(0, READIES)
import paella

#----------------------------------------------------------------------------------------------

class RedisSetup(paella.Setup):
    def __init__(self, nop=False):
        paella.Setup.__init__(self, nop)

    def common_first(self):
        self.install_downloaders()

    def debian_compat(self):
        self.install("build-essential")

    def redhat_compat(self):
        self.group_install("'Development Tools'")
        self.install("libatomic")
        self.run("[[ ! -e /usr/lib64/libatomic.so ]] && ln -s /usr/lib64/libatomic.so.1 /usr/lib64/libatomic.so")

    def fedora(self):
        self.group_install("'Development Tools'")
        self.install("libatomic")

    def macos(self):
        self.install("openssl")

    def archlinux(self):
        self.install("gcc gcc-libs make openssl")

    def alpine(self):
        self.install("gcc make openssl openssl-dev libatomic dev86 musl-dev linux-headers")

    def common_last(self):
        if self.dist == 'arch':
            self.install("patch pkg-config")
        elif self.dist == 'alpine':
            self.install('patch pkgconfig gnupg')
        else:
            self.install("dirmngr gnupg patch")

#----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Set up system for RedisGears build.')
parser.add_argument('-n', '--nop', action="store_true", help='no operation')
args = parser.parse_args()

RedisSetup(nop = args.nop).setup()
