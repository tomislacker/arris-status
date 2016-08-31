#!/usr/bin/env python
"""
Arris Cable Modem Scraper

Usage:
    arris_status [options] <host/ip>

Options:
    -j, --json      Output JSON instead of table
    --status        Get status overview
    --hw            Get hardware/firmware
    --events        Get event list
    --state         Get state information
"""
import logging
from docopt import docopt
from .status import ArrisModem

__version__ = 'dev'

logging.basicConfig(**{
    'level': logging.DEBUG,
})

args = docopt(__doc__, version=__version__)
logging.debug(args)

modem = ArrisModem(args['<host/ip>'])
logging.debug(modem)
