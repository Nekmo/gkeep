import click
import os

import gkeepapi
from click import ClickException, FileError

from google_keep_tasks.auth import get_auth


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.option('--auth', default=None)
@click.pass_context
def cli(ctx, debug, auth):
    keep = gkeepapi.Keep()
    success = keep.login(*get_auth(auth))
    ctx.obj = {'keep': keep}


import google_keep_tasks.note
