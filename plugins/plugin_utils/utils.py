from ansible.module_utils.basic import missing_required_lib


def generate_missing_lib_message(library, type=None):
    msg = missing_required_lib(library=library)
    if type:
        msg = msg.replace("module", type)
    return msg
