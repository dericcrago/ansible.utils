"""
PEP440 parser and comparison
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    author: Bradley Thornton (@cidrblock)
    name: version_pep440
    short_description: The PEP440 version parser
    description:
     - Parse PEP440 version identifiers from a string
     - Works with ansible.utils.version_test
     - Works with ansible.utils.version_parse
    version_added: 2.4.0
"""

RETURN = r"""
base_version:
  description: The base version identifier.
  returned: always
  type: str
dev:
  description: The dev version identifier.
  type:
  - str
  - int
epoch:
  description: The epoch version identifier.
  returned: always
  type: int
local:
  description: The local version identifier.
  type: str
original:
  description: The original version string.
  returned: always
  type: str
major:
  description: The major version identifier.
  type: int
micro:
  description: The micro version identifier.
  type: int
minor:
  description: The minor version identifer.
  type: int
post:
  description: the post version identifer.
  type:
  - str
  - int
pre:
  description: The pre version idenifier.
  type:
  - str
  - int
public:
  description: The public version identifier.
  type: str
  returned: always
release:
  description: The release identifier.
  type: list
  elements: int
version_format:
  description: The format of this version
  returned: always
  type: str
"""


import json
import operator as lib_operator

from ansible_collections.ansible.utils.plugins.plugin_utils.base.version_parser import (
    VersionParserBase,
)
from ansible.module_utils._text import to_native
from ansible.module_utils.six import string_types


try:
    from setuptools.extern.packaging.version import parse
    from setuptools.extern.packaging.version import LegacyVersion
    from setuptools.extern.packaging.version import Version


    HAS_PEP440 = True
except ImportError:
    HAS_PEP440 = False


KEYS = (
    "base_version",
    "dev",
    "epoch",
    "local",
    "major",
    "micro",
    "minor",
    "post",
    "pre",
    "public",
    "release",
)


class VersionParser(VersionParserBase):
    """The pep 440 parser class
    """

    def compare(self, left, right, operator):
        """ compare 2 versions
        
        :param left: the left side
        :type left: str
        :param right: the right side
        :type right: str
        :param operator: the operator (see doc)
        :type operator: str
        :return: result of comparison
        :rtype: bool
        """
        if HAS_PEP440:
            try:
                left_obj = parse(left)
                if not isinstance(left_obj, Version):
                    raise Exception("Not a valid PEP440 version identifier")
            except Exception as exc:
                return self._parser_error(string=left, error=to_native(exc))

            try:
                right_obj = parse(right)
                if not isinstance(left_obj, Version):
                    raise Exception("Not a valid PEP440 version identifier")
            except Exception as exc:
                return self._parser_error(string=right, error=to_native(exc))
        else:
            return self._library_error("setuptools")

        return self._response(
            result=getattr(lib_operator, operator)(left_obj, right_obj)
        )

    def parse(self, string):
        """Std entry point for a version parser

        :param string: the string to parse the version from
        :type string: str
        :return: a response (errors and result)
        :rtype: namedtuple
        """
        if HAS_PEP440:
            try:
                parsed = parse(string)
                if isinstance(parsed, Version):
                    result = {
                        k: getattr(parsed, k, None)
                        for k in KEYS
                        if getattr(parsed, k, None) is not None
                    }
                    result['version_format'] = 'pep440'
                    result['original'] = string
                    return self._response(result=result)
                else:
                    raise Exception("Not a valid PEP440 version")
            except Exception as exc:
                return self._parser_error(string=string, error=to_native(exc))
        else:
            return self._library_error("setuptools")
