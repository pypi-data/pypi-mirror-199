"""
Main Stackler Script
"""

import subprocess
import sys
from typing import Optional

import click
from git import Repo
import typer

from stackler import display_utils
from stackler import phab_utils
from stackler import git_utils
from stackler import shell_runner
from stackler.git_utils import REPO_PATH, BASE_TAG
from stackler.display_utils import \
    print_cont_msg, print_error, print_msg, print_success, print_warning

app = typer.Typer()


arg_sha = typer.Argument(None, help="The SHA to the commit")

option_base = typer.Option(
    BASE_TAG,
    "--base", "-b",
    help='The base commit of the stack')
option_update_message = typer.Option(
    '',
    "--update-message", "-m",
    help='The message for updating a diff')
option_dry_run = typer.Option(
    False,
    "--dry-run", "-n",
    help='Print which commits are going to be submitted, but doesn\'t submit anything')
option_finish = typer.Option(
    False,
    "--finish", "-f",
    help='Use this flag if you finish editing the mid-stack commit')
option_create = typer.Option(
    False, "--create", "-c",
    help='When submitting, use this flag if you wish to create new diffs instead ' +
    'of updating the attached ones')
option_no_link = typer.Option(
    False,
    "--no-link", "-nl",
    help='When turned on, no link will be displayed with the commit summary, ' +
    'leaving you a more succinct overview of the stack. You could also configure ' +
    r'your terminal (smart selection in iTerm2) to detect diff ID ({D\d+} for example) ' +
    'and convert it into a clickable link.')


@app.command()
def submit(
        base: str = option_base,
        update_message: str = option_update_message,
        is_creating: bool = option_create,
        dry_run: bool = option_dry_run):
    """
    Submit a stack of commits separately.
    Use -b to specify a base if you aren't working on <develop>.
    """
    _precheck(base)
    _submit(base,
            update_message,
            is_creating,
            dry_run,
            prompt_dry_run=False)


def _submit(base: str,
            update_message: str,
            is_creating: bool,
            dry_run: bool,
            prompt_dry_run=False):

    # do an internal dry run to show the prompt
    if not dry_run and not prompt_dry_run:
        print_msg("By continuing, this script will:")
        _submit(base,
                update_message,
                is_creating,
                dry_run,
                prompt_dry_run=True)
        prompt = display_utils.add_msg_prefix("Do you want to continue?")
        if not click.confirm(prompt, default=True):
            print_error('Aborted')
            return

    # To submit a stack, a few things need to happen:
    # 1. find the base commit, which will remain unchanged for the entirety of
    # the operation.
    # 2. go through the stack of commits one by one via checkout:
    #     a. diff it out, get a modified commit
    #     b. connect diff with the previous one
    #     c. checkout the tip of the stack, rebase it onto the lastly modified
    #     commit
    # 3. move HEAD to the new tip

    repo = Repo(REPO_PATH)
    current_branch = repo.active_branch
    base_commit = repo.commit(base)
    prev_commits = [repo.head.commit]
    for prev_commit in repo.head.commit.traverse():
        if prev_commit == base_commit:
            break
        prev_commits.append(prev_commit)

    # 1. find the base commit
    current_commit = prev_commits[-1]
    if base_commit == current_commit:
        print_msg("No commits to submit")
        return

    # 2. go through the stack of commits
    prev_commit = base_commit
    prev_diff_id = ''
    current_diff_id = ''
    for i in range(len(prev_commits)):
        # sanity check:
        # Base - A - B - C - D
        # len(prev_commits) = 4
        # i goes from 0 to 3
        # to go to A, we need HEAD^3 (4 - 1)
        # hence `len(prev_commits) - i - 1`
        # HEAD^x now has x going from 3 to 0; current_commit from A to D
        path = f'HEAD~{len(prev_commits) - i - 1}'
        current_commit = repo.commit(path)

        repo.git.checkout(current_commit)
        is_updating = not is_creating and phab_utils.has_diff_attached()
        if is_updating:
            current_diff_id = phab_utils.get_diff_id()

        # show msgs
        if is_updating:
            display_utils.print_update_msg(
                current_commit, current_diff_id, update_message, not prompt_dry_run)
        else:
            display_utils.print_submit_msg(current_commit, prev_commit, not prompt_dry_run)

        # 2a. diff it out
        if not prompt_dry_run and not dry_run:
            arc_args = ["arc", "diff", prev_commit.hexsha]

            if is_updating:
                arc_args.append('-m')
                arc_args.append(update_message)
            else:
                if is_creating:
                    arc_args.append("--create")
                arc_args.append("--verbatim")

            try:
                shell_runner.run(arc_args, should_raise_instead_of_exit=True)
            except subprocess.CalledProcessError:
                print_warning(
                    "arc sumbit failed. Please start over."
                )
                print_cont_msg(
                    f"The command ran: {' '.join(arc_args)}"
                )
                repo.git.checkout(current_branch)
                sys.exit(1)

            # 2b. connect the diff with previous one
            current_diff_id = phab_utils.get_diff_id()
            if not is_updating and prev_diff_id:
                phab_utils.add_parent_to_diff(current_diff_id, prev_diff_id)
            prev_diff_id = current_diff_id

        # 2c. restack
        prev_commit = repo.head.commit
        repo.git.checkout(current_branch)
        repo.git.rebase(prev_commit.hexsha)

    # 3. move HEAD to new tip
    # already performed

    if not prompt_dry_run:
        display_utils.print_success("Success")


@ app.command()
def edit(sha: Optional[str] = arg_sha,
         base: str = option_base,
         finish: bool = option_finish):
    """
    Allows you to edit a commit within a stack easily.
    This is basically just a wrapper for `git rebase sha^`)
    Use -b to specify a base if you aren't working on <develop>.
    """
    if not finish:
        _precheck(base)
        if not sha:
            print_error("You must specify a SHA to edit.")
            sys.exit(1)
        if not git_utils.is_commit_in_stack(sha, tip='HEAD', base=base):
            print_error(
                f"The commit <{sha[:8]}> isn't in the stack.")
            print_cont_msg("Stackler only supports editing a commit in the working stack:")
            show(base)
            sys.exit(1)

        editor_cmd = "sed -i -re '1s/pick/e/'"
        git_cmd = f"git rebase -i {sha}^"
        shell_runner.run(
            f"GIT_SEQUENCE_EDITOR=\"{editor_cmd}\" {git_cmd}", shell=True)

        print_msg("Editing the commit:")
        git_cmd = "git show --stat"
        shell_runner.run(git_cmd, shell=True, hide_output=False)
        print_success(
            "Make your changes and amend them into the commit, " +
            "then use `stackler edit --finish` to restore the stack.")

    else:
        print_msg("Restoring the stack")
        git_cmd = "git rebase --continue"
        shell_runner.run(git_cmd, shell=True, hide_output=False)
        print_success("Done")


@app.command()
def show(base: str = option_base, no_link: bool = option_no_link):
    """
    Prints the stack.
    """
    _precheck(base)
    repo = Repo(REPO_PATH)
    commits = list(repo.iter_commits(f"{base}..HEAD"))
    if not commits:
        print(display_utils.yellow('No commits in the stack.'))
    else:
        phab_utils.fetch_matadata_from_commits(*commits)
    for i, commit in enumerate(commits):
        print(('| ' if i > 0 else '↑ ') + display_utils.commit_summary(commit, short=False))
        if not no_link:
            print('| ' + 5 * ' ' +
                  display_utils.underline(display_utils.blue(phab_utils.get_diff_link(commit))))
            print('| ')
    display_utils.print_base(base, repo.commit(f"{base}"))


@app.command()
def land(base: str = option_base, bypass_accepted_check: bool = False):
    """
    Lands the stack. This command does prechecks to ensure the land is successful.
    """
    _precheck(base)
    repo = Repo(REPO_PATH)
    commits = list(repo.iter_commits(f"{base}..HEAD"))
    if not phab_utils.are_commits_all_accepted(*commits) and not bypass_accepted_check:
        print_error("All the diffs must be accepted before you can land.")
        sys.exit(0)
    print_msg("Before landing, this script needs to pull and rebase.")
    print_cont_msg("Right now, Stackler only supports landing onto the git upstream, "
                   + "so the rebase command about to run is `git pull --rebase`. "
                   + "You could run into merge conflicts.'")
    if not click.confirm(display_utils.add_prefix_padding('Continue?'), default=True):
        print_error('Aborted.')
        sys.exit(1)
    else:
        print_msg('Starting pulling and rebasing.')

    try:
        shell_runner.run(['git', 'pull', '--rebase'], should_raise_instead_of_exit=True)
    except subprocess.CalledProcessError:
        print_warning(
            'Looks like something hit an error. Mostly likely a merge conflict.')
        print_cont_msg(
            'If that\'s the case, You may resolve it and try again, starting with `git status`.')
        sys.exit(1)

    current_branch = repo.active_branch
    print_msg('Starting landing.')
    arc_args = ['arc', 'land']
    try:
        shell_runner.run(arc_args, hide_output=False, should_raise_instead_of_exit=True)
    except subprocess.CalledProcessError:
        print_warning(
            "arc land failed. Please start over."
        )
        print_cont_msg(
            f"The command ran: {' '.join(arc_args)}"
        )
        sys.exit(1)

    # if landing a branchless stack, the repo is left detached, this hack resets it
    try:
        repo.active_branch
    except TypeError:
        repo.git.checkout(current_branch)


def _precheck(base: str):
    """
    Exits the command if precheck fails.
    Precheck checks for dirty repo, untracked files, and detached head.
    """
    repo = Repo(REPO_PATH)

    if not git_utils.get_commit_safe(base):
        print_error(
            f"The base {base} doesn't exist. Please double check the SHA.")
        sys.exit(1)

    if git_utils.is_detached():
        print_error(
            "The head is detached. Please attach it and try again.")
        print_cont_msg(
            "Usually the command to do so is `git checkout develop`")
        sys.exit(1)

    if git_utils.is_dirty():
        print_error("The repo is dirty.")
        print_cont_msg("Please commit or discard all your changes.")
        sys.exit(1)

    if git_utils.is_unstaged():
        print_error("There are untracked files:")
        file_str = '\n'.join(repo.untracked_files)
        print(file_str)
        print_msg("Please commit them by `git commit -am  <commit message>`")
        sys.exit(1)


@ app.callback()
def callback():
    """Stackler makes working with stacks easier."""
    # This makes Typer treat submit as an explict command
