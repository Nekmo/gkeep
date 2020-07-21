import sys

import click

from google_keep_tasks.auth import GoogleKeep
from google_keep_tasks.cli import GkeepGroup
from google_keep_tasks.items import items
from google_keep_tasks.labels import labels
from google_keep_tasks.notes import notes


@click.group(cls=GkeepGroup)
@click.option('--debug/--no-debug', default=None)
@click.pass_context
def cli(ctx, debug):
    google_keep = GoogleKeep()
    if sys.argv[-1] not in ctx.help_option_names:
        google_keep.login_or_input()
    ctx.obj = {'keep': google_keep.keep}


cli.add_command(items)
cli.add_command(notes)
cli.add_command(labels)
