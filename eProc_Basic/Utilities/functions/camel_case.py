from re import sub


def convert_to_camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", " ")
    return s[:1].lower() + s[1:] if s else s

