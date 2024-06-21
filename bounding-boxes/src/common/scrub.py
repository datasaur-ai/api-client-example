import copy


def scrub(x):
    """
    Adapted from https://stackoverflow.com/a/11410935
    """
    ret = copy.deepcopy(x)
    if isinstance(x, dict):
        for key, value in x.items():
            if isinstance(value, dict):
                ret[key] = scrub(value)
                continue

            if value is None:
                del ret[key]
                continue

            ret[key] = scrub(value)
    elif isinstance(x, list):
        for index, item in enumerate(x):
            ret[index] = scrub(item)

    return ret
