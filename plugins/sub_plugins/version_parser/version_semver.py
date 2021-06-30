"""
json parser

This is the json parser for use with the cli_parse module and action plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    author: Bradley Thornton (@cidrblock)
    name: version_semver
    short_description: The semver version parser
    description:
     - Parse semver version identifiers from a string
     - Works with ansible.utils.version_test
     - Works with ansible.utils.version_parse
    version_added: 2.4.0
"""

RETURN = r"""
"""

EXAMPLES = r"""
"""

import json

from ansible.module_utils._text import to_native
from ansible.module_utils.six import string_types
from ansible_collections.ansible.utils.plugins.plugin_utils.base.version_parser import (
    VersionParserBase,
)
from ansible_collections.ansible.utils.plugins.plugin_utils.utils import (
    generate_missing_lib_message,
)


try:
    import semver

    HAS_SEMVER = True
except ImportError:
    HAS_SEMVER = False


class VersionParser(VersionParserBase):
    """The semver parser class
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
        if HAS_SEMVER:
            try:
                left_obj = semver.VersionInfo.parse(left)
            except Exception as exc:
                return self._parser_error(string=left, error=to_native(exc))

            try:
                right_obj = semver.VersionInfo.parse(right)
            except Exception as exc:
                return self._parser_error(string=right, error=to_native(exc))
        else:
            return self._library_error("semver")

        comparison = semver.compare(left, right)

        comp_map = {
            "lt": (-1,),
            "le": (0, -1),
            "eq": (0,),
            "ne": (1, -1),
            "ge": (0, 1),
            "gt": (1,),
        }

        return self._response(result=comparison in comp_map[operator])

    def parse(self, string):
        """Std entry point for a version parser

        :param string: the string to parse the version from
        :type string: str
        :return: a response (errors and result)
        :rtype: namedtuple
        """
        if HAS_SEMVER:
            try:
                parsed = semver.VersionInfo.parse(string)
                result=dict(parsed.to_dict())
                result['version_format'] = 'semver'
                result['original'] = string
                return self._response(result=result)
            except Exception as exc:
                return self._parser_error(string=string, error=to_native(exc))
        else:
            return self._library_error("semver")
