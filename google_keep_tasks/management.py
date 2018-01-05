import click

import gkeepapi

from google_keep_tasks.auth import get_auth
from google_keep_tasks.exceptions import LoginError


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.option('--auth', default=None)
@click.pass_context
def cli(ctx, debug, auth):
    keep = gkeepapi.Keep()
    try:
        keep.login(*get_auth(auth))
    except gkeepapi.LoginException:
        raise LoginError
    ctx.obj = {'keep': keep}


import google_keep_tasks.note
