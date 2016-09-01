import logging

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from . import parsers

logger = logging.getLogger(__name__)


class ArrisModem(object):
    def __init__(self, address, port=80):
        self.address = address
        self.port = port
        self._contents = {}

    def clear_cache(self):
        self._contents = {}
        return self

    def _get_url(self, uri):
        return "http://{host}:{port}{uri}".format(
            host=self.address,
            port=self.port,
            uri=uri)

    def _get_parsed(self, content):
        logger.debug("Getting contents for '{}'".format(content))
        if content not in self._contents:
            # Need to fetch it
            parser = getattr(parsers, content)
            content_url = self._get_url(parser.uri)
            raw_data = urlopen(content_url).read()
            self._contents[content] = parser.parse(raw_data)

        return self._contents[content]

    @property
    def events(self):
        return self._get_parsed('Events')

    @property
    def hardware(self):
        return self._get_parsed('Hardware')

    @property
    def state(self):
        return self._get_parsed('State')

    @property
    def status(self):
        return self._get_parsed('Status')

    def __getattr__(self, name):
        logger.debug("Fetching {}".format(name))

