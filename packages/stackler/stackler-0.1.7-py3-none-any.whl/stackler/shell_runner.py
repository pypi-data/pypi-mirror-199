
"""
A subprocess wrapper for Stackler.
This is necessary mostly because git writes everything to stderr.
"""

import subprocess
import sys

from typing import Union

from stackler import display_utils


def run(args: list[str],
        shell: bool = False,
        hide_output: bool = True,
        show_output_upon_error: bool = True,
        should_raise_instead_of_exit: bool = False):
    """_summary_

    Args:
        args (list[str]): _description_
        shell (Boolean, optional): When set to True, args can be a string. Defaults to True.
        hide_output (Boolean, optional):
            Hides and caches the output when set to True. Defaults to True.
        show_output_upon_error (Boolean, optional):
            Shows the cached output when an error occures. Defaults to True.
        should_raise_instead_of_exit (bool, optional): When set to True, the runner will raise
            CalledProcessError instead of printing out error messages and exiting. 
            Defaults to False.

    Raises:
        subprocess.CalledProcessError: The original error raise by the run command.
    """
    process = None
    display_args = args if shell else ' '.join(args)
    try:
        if hide_output:
            process = subprocess.run(args=args,
                                     shell=shell,
                                     check=False,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True)
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, display_args)
        else:
            process = subprocess.run(args=args,
                                     shell=shell,
                                     check=True)
    except subprocess.CalledProcessError as err:
        if should_raise_instead_of_exit:
            raise err
        if hide_output and show_output_upon_error and process:
            display_utils.print_error("An error occured.")
            display_utils.print_cont_msg(f"The command ran: {display_args}")

            if process.stdout:
                display_utils.print_msg("stdout:")
                display_utils.print_cont_msg(_output_to_string(process.stdout))
            else:
                display_utils.print_msg("No stdout")

            if process.stderr:
                display_utils.print_msg("stderr:")
                display_utils.print_cont_msg(_output_to_string(process.stderr))
            else:
                display_utils.print_msg("No stderr")
        sys.exit(1)


def _output_to_string(source: Union[str, bytes]) -> str:
    """
    Convert a byte string to regular string
    """
    if isinstance(source, str):
        return source
    if isinstance(source, bytes):
        return source.decode('utf-8')
    return str(source)
