import click

from google_keep_tasks.exceptions import ItemNotFound
# from google_keep_tasks.management import cli


def search_item(items, text):
    for item in items:
        if item.text == text:
            return item
    raise ItemNotFound(text)


@click.group()
def items():
    pass


@items.command('add')
@click.option('--check/--uncheck', default=None)
@click.option('--duplicate/--no-duplicate', default=False)
@click.argument('id')
@click.argument('text')
@click.pass_context
def add_item(ctx, check, duplicate, id, text):
    keep = ctx.obj['keep']
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


@items.command('edit')
@click.option('--check/--uncheck', default=None)
@click.option('--new-text', default='')
@click.argument('id')
@click.argument('text')
@click.pass_context
def edit_item(ctx, check, new_text, id, text):
    keep = ctx.obj['keep']
    gnote = keep.get(id)
    item = search_item(gnote.items, text)
    item.text = new_text or item.text
    item.checked = item.checked if check is None else check
    keep.sync()


@items.command('delete')
@click.argument('id')
@click.argument('text')
@click.pass_context
def delete_item(ctx, id, text):
    keep = ctx.obj['keep']
    gnote = keep.get(id)
    item = search_item(gnote.items, text)
    item.delete()
    keep.sync()


@items.command('is-checked')
@click.argument('id')
@click.argument('text')
@click.pass_context
def delete_item(ctx, id, text):
    keep = ctx.obj['keep']
    gnote = keep.get(id)
    item = search_item(gnote.items, text)
    print(item.checked)
    keep.sync()
