try:
    from termcolor import colored
except ImportError:
    colored = None

from pyfiglet import figlet_format

import six


def styled_ascii_text(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


def field_name_format(field_name: str):
    return field_name.replace("_", " ").capitalize()