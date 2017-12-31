import click
import os
from click import ClickException, FileError



@click.group()
@click.option('--debug/--no-debug', default=None)
@click.option('--auth', default=None)
@click.pass_context
def cli(ctx, debug, auth):
    pass


import google_keep_tasks.note
