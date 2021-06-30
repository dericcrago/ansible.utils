# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Test plugin file for netaddr tests: in_any_network
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: version_test
    author: Bradley Thornton (@cidrblock)
    version_added: "2.4.0"
    short_description: Test if a string is a valid version identifier or compare 2 version strings
    description:
        - Test if a string is a valid identifier or compare 2 version strings
    options:
        left:
            description:
            - The primary string to work with
            type: str
            required: True
        format:
            description:
            - Specify the version format of the strings
            type: str
            required: True
        operator:
            description:
            - Specifcy how 2 version strings should be compared
            type: str
            choices:
            - '='
            - '=='
            - '>='
            - '>'
            - '<='
            - '<'
            - '!='
            - 'eq'
            - 'ge'
            - 'gt'
            - 'le'
            - 'lt'
            - 'ne'
        right:
            description:
            - The version string to compare against
            type: str
        

    notes:
    - 
"""

EXAMPLES = r"""

- name: Check if various strings are valid PEP440 identifiers
  assert:
    that: "{{ string is ansible.utils.version_test('ansible.utils.version_pep440') }}"
    success_msg: "{{ message }}"
    fail_msg: "{{ message.replace('is', 'is not') }}"
  loop:
  - 1.0
  - 1.0b2.post345.dev456
  - 1.2.3-pre.2+build.4
  - ABCDEF
  loop_control:
    loop_var: string
  ignore_errors: True
  vars:
    message: "'{{ string }}' is a valid PEP440 identifier"

# TASK [Check if various strings are valid PEP440 identifiers] ***************
# ok: [localhost] => (item=1.0) => {
#     "ansible_loop_var": "string",
#     "changed": false,
#     "msg": "'1.0' is a valid PEP440 identifier",
#     "string": 1.0
# }
# ok: [localhost] => (item=1.0b2.post345.dev456) => {
#     "ansible_loop_var": "string",
#     "changed": false,
#     "msg": "'1.0b2.post345.dev456' is a valid PEP440 identifier",
#     "string": "1.0b2.post345.dev456"
# }
# ok: [localhost] => (item=1.2.3-pre.2+build.4) => {
#     "ansible_loop_var": "string",
#     "changed": false,
#     "msg": "'1.2.3-pre.2+build.4' is a valid PEP440 identifier",
#     "string": "1.2.3-pre.2+build.4"
# }
# failed: [localhost] (item=ABCDEF) => {
#     "ansible_loop_var": "string",
#     "assertion": false,
#     "changed": false,
#     "evaluated_to": false,
#     "msg": "'ABCDEF' is not a valid PEP440 identifier",
#     "string": "ABCDEF"
# }

- name: Check if various strings are valid semver identifiers
  assert:
    that: "{{ string is ansible.utils.version_test('ansible.utils.version_semver') }}"
    success_msg: "{{ message }}"
    fail_msg: "{{ message.replace('is', 'is not') }}"
  loop:
  - 1.0.0
  - 1.2.3-pre.2+build.4
  - ABCDEF
  loop_control:
    loop_var: string
  ignore_errors: True
  vars:
    message: "'{{ string }}' is a valid semver identifier"

# TASK [Check if various strings are valid semver identifiers] ***************
# ok: [localhost] => (item=1.0.0) => {
#     "ansible_loop_var": "string",
#     "changed": false,
#     "msg": "'1.0.0' is a valid semver identifier",
#     "string": "1.0.0"
# }
# ok: [localhost] => (item=1.2.3-pre.2+build.4) => {
#     "ansible_loop_var": "string",
#     "changed": false,
#     "msg": "'1.2.3-pre.2+build.4' is a valid semver identifier",
#     "string": "1.2.3-pre.2+build.4"
# }
# failed: [localhost] (item=ABCDEF) => {
#     "ansible_loop_var": "string",
#     "assertion": false,
#     "changed": false,
#     "evaluated_to": false,
#     "msg": "'ABCDEF' is not a valid semver identifier",
#     "string": "ABCDEF"
# }


- name: Compare several pep440 strings
  assert:
    that: "{{ left is ansible.utils.version_test(format, operator, right) }}"
    success_msg: "{{ message }}"
    fail_msg: "{{ message.replace('is', 'is not') }}"
  loop:
  - ['1.0.0', '>', '0.0.1']
  - ['1.0.0', '<', '0.0.1']
  - ['1.0b2.post345.dev456', 'lt', '1.0b2.post345.dev457']
  vars:
    format: ansible.utils.version_pep440
    left: "{{ item.0 }}"
    message: "'{{ left }}' is {{ operator }} than '{{ right }}'"
    operator: "{{ item.1 }}"
    right: "{{ item.2 }}"
  ignore_errors: True

# TASK [Compare several pep440 strings] **************************************
# ok: [localhost] => (item=['1.0.0', '>', '0.0.1']) => {
#     "ansible_loop_var": "item",
#     "changed": false,
#     "item": [
#         "1.0.0",
#         ">",
#         "0.0.1"
#     ],
#     "msg": "'1.0.0' is > than '0.0.1'"
# }
# failed: [localhost] (item=['1.0.0', '<', '0.0.1']) => {
#     "ansible_loop_var": "item",
#     "assertion": false,
#     "changed": false,
#     "evaluated_to": false,
#     "item": [
#         "1.0.0",
#         "<",
#         "0.0.1"
#     ],
#     "msg": "'1.0.0' is not < than '0.0.1'"
# }
# ok: [localhost] => (item=['1.0b2.post345.dev456', 'lt', '1.0b2.post345.dev457']) => {
#     "ansible_loop_var": "item",
#     "changed": false,
#     "item": [
#         "1.0b2.post345.dev456",
#         "lt",
#         "1.0b2.post345.dev457"
#     ],
#     "msg": "'1.0b2.post345.dev456' is lt than '1.0b2.post345.dev457'"
# }

- name: Compare several semver strings
  assert:
    that: "{{ left is ansible.utils.version_test(format=format, operator=operator, right=right) }}"
    success_msg: "{{ message }}"
    fail_msg: "{{ message.replace('is', 'is not') }}"
  loop:
  - ['1.0.0', '>', '0.0.1']
  - ['1.0.0', '<', '0.0.1']
  - ['1.2.3-pre.3', 'lt', '1.2.3-pre.4']
  vars:
    format: ansible.utils.version_semver
    left: "{{ item.0 }}"
    message: "'{{ left }}' is {{ operator }} than '{{ right }}'"
    operator: "{{ item.1 }}"
    right: "{{ item.2 }}"

# TASK [Compare several semver strings] **************************************
# ok: [localhost] => (item=['1.0.0', '>', '0.0.1']) => {
#     "ansible_loop_var": "item",
#     "changed": false,
#     "item": [
#         "1.0.0",
#         ">",
#         "0.0.1"
#     ],
#     "msg": "'1.0.0' is > than '0.0.1'"
# }
# failed: [localhost] (item=['1.0.0', '<', '0.0.1']) => {
#     "ansible_loop_var": "item",
#     "assertion": false,
#     "changed": false,
#     "evaluated_to": false,
#     "item": [
#         "1.0.0",
#         "<",
#         "0.0.1"
#     ],
#     "msg": "'1.0.0' is not < than '0.0.1'"
# }
# ok: [localhost] => (item=['1.2.3-pre.3', 'lt', '1.2.3-pre.4']) => {
#     "ansible_loop_var": "item",
#     "changed": false,
#     "item": [
#         "1.2.3-pre.3",
#         "lt",
#         "1.2.3-pre.4"
#     ],
#     "msg": "'1.2.3-pre.3' is lt than '1.2.3-pre.4'"
# }


"""

RETURN = """

Note: See the documentation of each version format plugin to review the return value

"""

from ansible.errors import AnsibleError

from ansible_collections.ansible.utils.plugins.plugin_utils.subplugin_loader import (
    load,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

ARGSPEC_CONDITIONALS = {
    "required_by": {"operator": "right"}
}

OPERATOR_MAP = {
    "=": "eq",
    "==": "eq",
    ">=": "ge",
    ">": "gt",
    "<": "lt",
    "<=": "le",
    "!=": "ne",
}


def _version_test(*args, **kwargs):
    keys = ["left", "format", "operator", "right"]
    data = dict(zip(keys, args))
    data.update(kwargs)

    aav = AnsibleArgSpecValidator(
        data=data, schema=DOCUMENTATION, schema_conditionals=ARGSPEC_CONDITIONALS, name="version_parser"
    )

    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleError(errors)

    response = load(
        name=data["format"],
        directory="version_parser",
        type="version parser",
        cls="VersionParser",
        caller_type="test plugin",
    )
    if response.failed:
        raise AnsibleError(message=response.msg)

    if updated_data['operator'] is None:
        result = response.subplugin.parse(string=updated_data['left'])
        return not result.errors
    else:
        operator = OPERATOR_MAP.get(
            updated_data["operator"], updated_data["operator"]
        )
        result = response.subplugin.compare(
            left=updated_data["left"],
            right=updated_data["right"],
            operator=operator,
        )
        if result.errors:
            raise AnsibleError(message=" ".join(result.errors))
        return result.result


class TestModule(object):
    """ network jinja test"""

    test_map = {"version_test": _version_test}

    def tests(self):
        return self.test_map
