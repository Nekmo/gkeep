import click

import gkeepapi
from gkeepapi.exception import LoginException

from google_keep_tasks.auth import get_auth, GoogleKeepFileAuth, GoogleKeep
from google_keep_tasks.exceptions import LoginError


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.option('--auth', default='auth.txt')
@click.pass_context
def cli(ctx, debug, auth):
    google_keep = GoogleKeep()
    google_keep.login_or_input()
    ctx.obj = {'keep': google_keep.keep}


import google_keep_tasks.items
import google_keep_tasks.notes
