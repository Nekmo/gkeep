import click

from google_keep_tasks.cli import GkeepGroup
from google_keep_tasks.exceptions import ItemNotFound
# from google_keep_tasks.management import cli


def search_item(items, text):
    for item in items:
        if item.text == text:
            return item
    raise ItemNotFound(text)


@click.group(cls=GkeepGroup)
def items():
    """Use ``items`` command to work with the note checkboxes. This command has
    subcommands for adding, editing, deleting or check/uncheck items. To see all
    subcommands of ``items`` use ``--help``::

        gkeep items --help

    An example of a subcommand is ``add``. To see help use
    ``gkeep items add --help``.  In all ``items`` subcommands, note ``id`` argument is
    mandatory. To get note ``id`` use ``gkeep notes search`` or ``gkeep notes get``.
    """


@items.command('add')
@click.option('--check/--uncheck', default=None, help='Item is checked or not')
@click.option('--duplicate/--no-duplicate', default=False,
              help='By default if the element already exists, it is not duplicated. '
                   'If you want duplicate the element, use the this parameter')
@click.argument('id')
@click.argument('text')
@click.pass_context
def add_item(ctx, check, duplicate, id, text):
    """Add a item to an existing note. By default if the element already exists,
    it is not duplicated. To duplicate the element use ``--duplicate`` param. By
    default the item is created unchecked.

    .. code-block:: shell

        gkeep items add 75e4202b0c1.9fc0b868a7b34952 "Chip cookies" --check

    The syntax is:
    """
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
@click.option('--check/--uncheck', default=None, help='Item is checked or not')
@click.option('--new-text', default='New element text')
@click.argument('id')
@click.argument('text')
@click.pass_context
def edit_item(ctx, check, new_text, id, text):
    """Edit an existing item. Use this command to change the text or
    check or uncheck the item. For example:

    .. code-block:: shell

        gkeep items edit 75e4202b0c1.9fc0b868a7b34952 "Chip cookies" --uncheck

    Another example:

    .. code-block:: shell

        gkeep items edit 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"
                         --new-text "Chocolate orange cookies"

    The syntax is:
    """
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
    """Delete a item to an existing note.

    .. code-block:: shell

        gkeep items delete 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"

    The syntax is:
    """
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
    """Returns ``True`` if the item is checked and ``False`` if it is unchecked.

    .. code-block:: shell

        gkeep items is-checked 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"

    The syntax is:
    """
    keep = ctx.obj['keep']
    gnote = keep.get(id)
    item = search_item(gnote.items, text)
    print(item.checked)
    keep.sync()
