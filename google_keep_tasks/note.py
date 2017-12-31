import click
import gkeepapi

from google_keep_tasks.auth import get_auth
from google_keep_tasks.management import cli


def search_item(items, text):
    for item in items:
        if item.text == text:
            return item


@cli.command('add-item')
@click.option('--check/--uncheck', default=False)
@click.option('--duplicate/--no-duplicate', default=False)
@click.argument('id')
@click.argument('text')
def add_item(check, duplicate, id, text):
    keep = gkeepapi.Keep()
    success = keep.login(*get_auth())
    gnote = keep.get(id)
    item = search_item(gnote.items, text)
    if item and not duplicate:
        item.checked = check
    else:
        gnote.add(text, check)
    keep.sync()
