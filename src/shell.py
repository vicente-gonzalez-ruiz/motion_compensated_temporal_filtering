#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

from subprocess  import check_call
from subprocess  import CalledProcessError
from sys         import exit

import logging

logging.basicConfig()
log = logging.getLogger("shell")
log.setLevel('INFO')

class Shell:

    @staticmethod
    def run(command):
        
        log.info("Running \"" + command + "\"")

        try:
            check_call(command, shell=True)
        except CalledProcessError:
            exit(-1)
