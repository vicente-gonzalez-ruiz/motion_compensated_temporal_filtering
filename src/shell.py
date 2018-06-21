#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

from subprocess import check_call
from subprocess import CalledProcessError
from sys import exit
from colorlog import ColorLog
import logging
import traceback

logger = None

class Shell:

    def setLogger(_logger_):
        global logger
        logger = _logger_
        
    @staticmethod
    def run(command):
        
        logger.info("Running \"" + command + "\"")

        try:
            check_call(command, shell=True)
        except CalledProcessError:
            logger.warning("Exception {}".format(traceback.format_exc()))
            raise
            #exit(-1)
