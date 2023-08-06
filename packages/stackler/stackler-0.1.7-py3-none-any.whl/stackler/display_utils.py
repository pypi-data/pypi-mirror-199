"""
Display utils for better UX for Stackler
"""

from datetime import datetime
import sys
import os
from textwrap import TextWrapper

from humanize import naturaltime
from git import Commit
from termcolor import colored
from wcwidth import wcswidth

from stackler.git_utils import get_short_hash
from stackler.phab_utils import has_diff_attached, get_diff_id, get_matadata_from_commit

DIFF_ID_LENGTH = 7  # Dxxxxxx
PRINT_PREFIX = " Stackler "


def darken(in_s: str) -> str:
    """Returns a darkened string"""
    return colored(in_s, attrs=['dark'])


def underline(in_s: str) -> str:
    """Returns an underlined string"""
    return colored(in_s, attrs=['underline'])


def bold(in_s: str) -> str:
    """Returns a bold string"""
    return colored(in_s, attrs=['bold'])


def green(in_s: str) -> str:
    """Returns a green string"""
    return colored(in_s, 'green')


def red(in_s: str) -> str:
    """Returns a red string"""
    return colored(in_s, 'red')


def cyan(in_s: str) -> str:
    """Returns a cyan string"""
    return colored(in_s, 'cyan')


def yellow(in_s: str) -> str:
    """Returns a yellow string"""
    return colored(in_s, 'yellow')


def blue(in_s: str) -> str:
    """Returns a blue string"""
    return colored(in_s, 'blue')


def _truncate_and_flatten_string(str_input: str, max_length: int) -> str:
    """Truncates and flatten (normalize whitespace) the string to a specified displayed length"""
    str_input = ' '.join(str_input.split())
    displayed_length = wcswidth(str_input)
    if displayed_length < max_length:
        return str_input
    else:
        # this assumes the worst possible situation known to me,
        # which is when a unicode char takes 2 spaces. If it takes more, this will not work.
        last_idx = max_length // 2 - 1

        str_end = '...'
        while wcswidth(str_input[:last_idx]) < max_length - len(str_end):
            last_idx += 1
        return str_input[:last_idx-1] + str_end


def _get_term_width() -> int:
    """Gets the term width (amount of characters per line)"""
    return os.get_terminal_size().columns


_status_name_display_map: dict[str: str] = {
    'na': '--',
    'needs review': 'NR',
    'accepted': green(bold('AC')),
    'needs revision': red(bold('RJ')),
    'changes planned': red(bold('CP')),
    'abandoned': darken('AB'),
    'closed': darken('CO'),
}


def commit_summary(cmt: Commit, short=True) -> str:
    """Returns an inline summary of a given commit"""
    hsh = get_short_hash(cmt)
    author = cmt.author.name
    time = naturaltime(datetime.now() - cmt.committed_datetime.replace(tzinfo=None))
    diff_id = get_diff_id(cmt) if has_diff_attached(cmt) else "N/A".center(DIFF_ID_LENGTH)

    matadata = get_matadata_from_commit(cmt) if has_diff_attached(cmt) else {}
    status_name = matadata['statusName'].lower() if has_diff_attached(cmt) else 'na'
    displayed_status_name = ''
    if status_name in _status_name_display_map:
        displayed_status_name = _status_name_display_map[status_name]
    else:
        displayed_status_name = '??'
        print_warning(f"looks like your diff is in an unrecgonized status: {status_name}")
    status_name = f"{darken('[')}{displayed_status_name}{darken(']')}"

    term_width = _get_term_width()
    msg = _truncate_and_flatten_string(cmt.message, term_width - DIFF_ID_LENGTH -
                                       wcswidth(hsh + author + time + diff_id) - 14)

    hsh = red(hsh)
    author = cyan(author)
    time = green(time)
    diff_id = yellow(diff_id)

    if short:
        return f"<{hsh} {_truncate_and_flatten_string(msg, 20)}>"
    else:
        return f"{status_name} {diff_id} - {hsh} - {msg} ({time}) <{author}>"


def print_base(base: str, cmt: Commit):
    """Prints the base tag and the base commit"""
    line_char = '-'
    base_header = "Base -> "
    base_text = f'└-{base_header}{base} (shown below) '
    # using ^ as it's illegal in tag names
    base_placeholder = '^' * len(base_text)
    width = _get_term_width() - 6
    print(base_placeholder
          .ljust(width, line_char)
          .replace(' ', line_char)
          .replace(base_placeholder, darken(yellow(base_text))))
    print(commit_summary(cmt, short=False))


def print_update_msg(
        current_commit: Commit, current_diff_id: str, update_message: str, ongoing: bool):
    """Prints msg for updating an diff"""
    print_cont_msg(
        f"{blue('Updating' if ongoing else 'Update')} {yellow(current_diff_id)} with" +
        f" {commit_summary(current_commit)}" +
        (f", message: {_truncate_and_flatten_string(update_message, 30) }."
         if update_message else "."))


def print_submit_msg(current_commit: Commit, prev_commit: Commit, ongoing: bool):
    """Prints msg for submitting an diff"""
    print_cont_msg(
        f"{green('Submiting' if ongoing else 'Submit')} {commit_summary(current_commit)}"
        + f" based on {commit_summary(prev_commit)}.")


def add_msg_prefix(msg: str):
    """Returns a message with the regular prefix"""
    return colored(PRINT_PREFIX, attrs=['reverse', 'underline']) + ' ' + str(msg)


def print_msg(msg: str):
    """Prints a regular message"""
    print(add_msg_prefix(msg))


def _get_prefix_textwrapper() -> TextWrapper:
    """Returns a textwrap.TextWrapper that wraps text to the width of the screen plus the initial
    indention"""
    indent = ' ' * (len(PRINT_PREFIX)+1)
    return TextWrapper(initial_indent=indent, subsequent_indent=indent, width=_get_term_width())


def print_cont_msg(msg: str, *args, attrs=None):
    """
    Prints a regular message, but leaving the space in the beginning to match the indentation.
    You may also pass in the parameters for termcolor#colored.

    >>> print_msg('abc')
     Stackler abc
    >>> print_cont_msg('bcd')
              bcd
    >>> print_cont_msg('bcd\nbcd') # essentially a really long line should break with indentition
              bcd
              bcd
    """
    print(colored(_get_prefix_textwrapper().fill(msg), *args, attrs=(attrs if attrs else [])))


def add_prefix_padding(string: str):
    """Pads the string with spaces of the length of PRINT_PREFIX"""
    return _get_prefix_textwrapper().fill(string)


def add_success_prefix(success_msg: str):
    """Returns a message with the green prefix"""
    return colored(PRINT_PREFIX, 'green', attrs=['reverse', 'underline']) + ' ' + success_msg


def print_success(success_msg: str):
    """Prints a success message"""
    print(add_success_prefix(success_msg))


def add_error_prefix(err_msg: str):
    """Returns a msg with the red prefix"""
    return colored(PRINT_PREFIX, 'red', attrs=['reverse', 'underline']) + ' ' + err_msg


def print_error(err_msg: str):
    """Prints error msg to stderr"""
    print(add_error_prefix(err_msg), file=sys.stderr)


def add_warning_prefix(warning_msg: str):
    """Returns a msg with the red prefix"""
    return colored(PRINT_PREFIX, 'yellow', attrs=['reverse', 'underline']) + ' ' + warning_msg


def print_warning(warning_msg: str):
    """Prints yellow msg to stdout"""
    print(add_warning_prefix(warning_msg))
