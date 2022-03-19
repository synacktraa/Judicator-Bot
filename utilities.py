import constants


def replace_ic(data, pattern_to_be_replaced, new_pattern):
    """
        Replaces words while ignoring letters case.
    """
    idx = data.lower().find(pattern_to_be_replaced.lower())
    mod_data = data.replace(
        data[idx:idx+len(pattern_to_be_replaced)], new_pattern)
    return mod_data


def censor_message(msg):
    """
        Censors the message according to given patterns.
    """
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    for pattern in constants.CENSORED:
        if pattern in msg.lower():
            idx = msg.lower().find(pattern)
            rev_data = msg[idx:idx+len(pattern)]
            for char in rev_data:
                for v in vowels:
                    if char == v:
                        rev_data = rev_data.replace(char, '\*')
            msg = replace_ic(msg, pattern, rev_data)
    return msg