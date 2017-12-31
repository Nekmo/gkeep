import click
import gkeepapi

from google_keep_tasks.auth import get_auth
from google_keep_tasks.exceptions import ItemNotFound
from google_keep_tasks.management import cli


def search_item(items, text):
    for item in items:
        if item.text == text:
            return item
    raise ItemNotFound


@cli.command('add-item')
@click.option('--check/--uncheck', default=None)
@click.option('--duplicate/--no-duplicate', default=False)
@click.argument('id')
@click.argument('text')
def add_item(check, duplicate, id, text):
    keep = gkeepapi.Keep()
    success = keep.login(*get_auth())
    gnote = keep.get(id)
    try:
        item = search_item(gnote.items, text)
        check = item.checked if check is None else check
    except ItemNotFound:
        item = None
        check = False if check is None else check
    if item and not duplicate:
        item.checked = check
    else:
        gnote.add(text, check)
    keep.sync()


@cli.command('edit-item')
@click.option('--check/--uncheck', default=None)
@click.option('--new-text', default='')
@click.argument('id')
@click.argument('text')
def edit_item(check, new_text, id, text):
    keep = gkeepapi.Keep()
    success = keep.login(*get_auth())
    gnote = keep.get(id)
    item = search_item(gnote.items, text)
    item.text = new_text or item.text
    item.checked = item.checked if check is None else check
    keep.sync()


@cli.command('delete-item')
@click.argument('id')
@click.argument('text')
def delete_item(id, text):
    keep = gkeepapi.Keep()
    success = keep.login(*get_auth())
    gnote = keep.get(id)
    item = search_item(gnote.items, text)
    item.delete()
    keep.sync()


@cli.command('is-checked-item')
@click.argument('id')
@click.argument('text')
def delete_item(id, text):
    keep = gkeepapi.Keep()
    success = keep.login(*get_auth())
    gnote = keep.get(id)
    item = search_item(gnote.items, text)
    print(item.checked)
    keep.sync()
