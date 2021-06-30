from collections import namedtuple
from importlib import import_module

from ansible.module_utils._text import to_native


Response = namedtuple("Response", ["failed", "msg", "subplugin"])


def load(name, directory, type, cls, **kwargs):
    """load a subplugin or return a failure"""

    if len(name.split(".")) != 3:
        msg = "{type} name should be provided as a full name including collection".format(
            type=type
        )
        return Response(failed=True, msg=msg, subplugin=None)

    cref = dict(zip(["corg", "cname", "plugin"], name.split(".")))
    subplugin_lib = "ansible_collections.{corg}.{cname}.plugins.sub_plugins.{directory}.{plugin}".format(
        **cref, directory=directory
    )

    try:
        subplugin_cls = getattr(import_module(subplugin_lib), cls)
        subplugin_instance = subplugin_cls(**kwargs)
        return Response(failed=False, msg="", subplugin=subplugin_instance)
    except Exception as exc:
        msg = "error loading the corresponding {type} plugin: {err}".format(
            type=type, err=to_native(exc)
        )
        return Response(failed=True, msg=msg, subplugin=None)
