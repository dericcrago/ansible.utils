#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The version parser filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: version_parser
    author: Bradley Thornton (@cidrblock)
    version_added: "2.4.0"
    short_description: Convert a version string to a dictionary
    description:
        - 
    options:
      string:
        description:
        - The string from which version information will be extracted
        type: str
        required: True
      parser:
        description:
        - The parser for the version string
        type: str
        default: ansible.utils.parser_semver
"""

EXAMPLES = r"""

- name: Parse a semver formatted version identifier
  debug:
    msg: "{{ '1.2.3-pre.2+build.4' | ansible.utils.version_parser('ansible.utils.parser_semver') }}"

# TASK [debug] ************************************************************
# ok: [localhost] => {
#     "msg": {
#         "build": "build.4",
#         "major": 1,
#         "minor": 2,
#         "patch": 3,
#         "prerelease": "pre.2"
#     }
# }

- name: Parse a PEP440 formatted version identifier
  debug:
    msg: "{{ '1.0b2.post345.dev456' | ansible.utils.version_parser('ansible.utils.parser_pep440') }}"

# TASK [debug] ************************************************************
# ok: [localhost] => {
#     "msg": {
#         "base_version": "1.0",
#         "dev": 456,
#         "epoch": 0,
#         "local": null,
#         "major": 1,
#         "micro": 0,
#         "minor": 0,
#         "post": 345,
#         "pre": [
#             "b",
#             2
#         ],
#         "public": "1.0b2.post345.dev456",
#         "release": [
#             1,
#             0
#         ]
#     }
# }
"""

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)
from ansible_collections.ansible.utils.plugins.plugin_utils.subplugin_loader import (
    load,
)


def _version_parser(*args, **kwargs):
    """Convert a version string to structured data."""

    keys = ["string", "parser"]
    data = dict(zip(keys, args))
    data.update(kwargs)

    aav = AnsibleArgSpecValidator(
        data=data, schema=DOCUMENTATION, name="version_parser"
    )

    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)

    response = load(
        name=updated_data["parser"],
        directory="version_parser",
        type="version parser",
        cls="VersionParser",
        caller_type="filter plugin",
    )
    if response.failed:
        raise AnsibleFilterError(message=response.msg)

    result = response.subplugin.parse(string=updated_data["string"])
    if result.errors:
        raise AnsibleFilterError(message=" ".join(result.errors))
    return result.result


class FilterModule(object):
    """ from_xml  """

    def filters(self):

        """a mapping of filter names to functions"""
        return {"version_parser": _version_parser}
