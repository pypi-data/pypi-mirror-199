import logging
from tsabin.meta import __version__


def get_version():
	return __version__


logging.getLogger(__name__).addHandler(logging.NullHandler())
