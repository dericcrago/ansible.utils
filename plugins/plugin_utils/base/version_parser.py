"""
The base class for version parsers
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from collections import namedtuple

from ansible_collections.ansible.utils.plugins.plugin_utils.utils import (
    generate_missing_lib_message,
)


class VersionParserBase:
    """ The base class for version parsers
    Provides a  standard response and error
    """

    def __init__(self, caller_type):
        self._caller_type = caller_type
        self._response = namedtuple("Response", ["errors", "result"])
        self._response.__new__.__defaults__ = (None, None)

    def _library_error(self, library):
        error = generate_missing_lib_message(
            library="setuptools", type=self._caller_type
        )
        return self._response(errors=[error])

    def _parser_error(self, string, error):
        error = "No version could be extracted from the string '{string}', the error was '{error}'".format(
            string=string, error=error
        )
        return self._response(errors=[error])
