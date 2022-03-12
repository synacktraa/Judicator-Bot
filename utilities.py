def replace_ic(data, pattern_to_be_replaced, new_pattern):
    """
        Replaces words while ignoring letters case.
    """
    idx = data.lower().find(pattern_to_be_replaced.lower())
    mod_data = data.replace(
        data[idx:idx+len(pattern_to_be_replaced)], new_pattern)
    return mod_data
