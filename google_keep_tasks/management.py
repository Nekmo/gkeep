import sys

import click

from google_keep_tasks.auth import GoogleKeep
from google_keep_tasks.items import items
from google_keep_tasks.notes import notes


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.option('--auth', default='auth.txt')
@click.pass_context
def cli(ctx, debug, auth):
    google_keep = GoogleKeep()
    if sys.argv[-1] not in ctx.help_option_names:
        google_keep.login_or_input()
    ctx.obj = {'keep': google_keep.keep}


cli.add_command(items)
cli.add_command(notes)
