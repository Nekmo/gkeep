# -*- coding: utf-8 -*-
import click
import gkeepapi
import sys
import re

from gkeepapi.node import List

from google_keep_tasks.cli import GkeepGroup
from google_keep_tasks.exceptions import InvalidColor


COLORS = {
    gkeepapi.node.ColorValue.Gray: {'bg': 'black', 'fg': 'white'},
    gkeepapi.node.ColorValue.Red: {'bg': 'red', 'fg': 'white'},
    gkeepapi.node.ColorValue.Green: {'bg': 'green'},
    gkeepapi.node.ColorValue.Yellow: {'bg': 'green', 'fg': 'black'},
    gkeepapi.node.ColorValue.Blue: {'bg': 'cyan', 'fg': 'white'},
    gkeepapi.node.ColorValue.DarkBlue: {'bg': 'blue', 'fg': 'white'},
    gkeepapi.node.ColorValue.Purple: {'bg': 'magenta', 'fg': 'white'},
    gkeepapi.node.ColorValue.White: {'bg': 'white', 'fg': 'black'},
}
COLOR_NAMES = [color.name.lower() for color in gkeepapi.node.ColorValue]

placeholder = '__placeholder__'


def get_color(color):
    if not color:
        return
    if isinstance(color, gkeepapi.node.ColorValue):
        return color
    color = color.title()
    if color and not hasattr(gkeepapi.node.ColorValue, color):
        raise InvalidColor(color)
    return getattr(gkeepapi.node.ColorValue, color)


def get_click_color(ctx, param, value):
    return get_color(value)


def find_or_create_label(keep, label_name):
    label = keep.findLabel(label_name)
    if not label:
        label = keep.createLabel(label_name)
    return label


def add_labels(keep, note, labels):
    if not labels:
        return
    for label in labels:
        note.labels.add(find_or_create_label(keep, label))


def get_labels(keep, labels):
    return list(filter(bool, map(keep.findLabel, labels)))


def comma_separated(ctx, param, value):
    return value.split(',') if value else []


def query_params(keep, **kwargs):
    kwargs['colors'] = (list(filter(bool, [get_color(kwargs.pop('color'))])) if 'color' in kwargs else []) or None
    labels = get_labels(keep, kwargs.pop('labels', []))
    deleted = kwargs.pop('deleted', None)
    title = kwargs.pop('title', None)
    text = kwargs.pop('text', None)
    if any(filter(lambda x: x is not None, [deleted, title, text])) or labels:
        kwargs['func'] = lambda x: all(filter(lambda y: isinstance(y, bool),
                                              [x.deleted == deleted if deleted is not None else None,
                                               x.title == title if title is not None else None,
                                               x.text == text if text is not None else None,
                                               set(x.labels.all()) == set(labels) if labels is not None else None]))
    return kwargs

def format_note_item(item):
    return u'%s%s %s' % (
        '  ' if item.indented else '',
        u'- [x]' if item.checked else u'- [ ]',
        item.text
    )

def format_note(note):
    if not isinstance(note, List):
        return note.text
    text = ""
    for item in note.items:
        text += "%s | %s\n" % (item.id.ljust(30), format_note_item(item))
    return text


def print_note(note):
    params = COLORS.get(note.color, {})
    note_id = (u'⚲ ' if note.pinned else '') + '(note id {})'.format(note.id)
    note_id += u' 🗑' if note.deleted or note.trashed else ''
    click.echo(click.style(note_id, **params))
    click.echo(click.style('"' * len(note_id), **params))
    if note.title:
        click.echo(click.style(note.title, bold=True))
        click.echo('-' * len(note_id))
    click.echo(format_note(note))
    click.echo('-' * len(note_id))
    if note.labels:
        click.echo(' '.join(click.style('[{}]'.format(label.name), underline=True, bold=True)
                            for label in note.labels.all()))
    click.echo(click.style('"' * len(note_id), **params))
    click.echo('\n')


def edit_note_checkboxes(note):
    text = click.edit(format_note(note)).strip()
    lines = text.split("\n")
    regex = re.compile(r"([\w.]*) *\| ( *)- \[(x| )\] (.*)")

    last_old_note = 'top'
    current_items = []
    for line in lines:
        id, indent, check_mark, content = regex.match(line).groups()
        found = list(filter(lambda item: item.id == id, note.items))
        old_note = found[0] if len(found) > 0 else None
        indented = len(indent) > 1
        checked = check_mark == 'x'
        current_items.append({
            'id': id,
            'previous': last_old_note,
            'old': old_note,
            'indented': indented,
            'checked': checked,
            'content': content
        })
        last_old_note = old_note
    
    # Deletion
    for item in note.items:
        if item.id not in [parts['id'] for parts in current_items]:
            item.delete()

    last_added = None
    for parts in current_items:
        previous = parts['previous'] if parts['previous'] != None else last_added

        # Addition
        if parts['old'] == None:
            sort = int(previous.sort) - 1 if previous != None and previous != 'top' else gkeepapi.node.NewListItemPlacementValue.Top 
            added = note.add(parts['content'], parts['checked'], sort)
            if parts['indented']:
                previous.indent(added)
            last_added = added

        # Modification
        else:
            if parts['old'].indented and not parts['indented']:
                if previous != None:
                    previous.dedent(parts['old'])
            if not parts['old'].indented and parts['indented']:
                if previous != None:
                    previous.indent(parts['old'])

            if parts['old'].checked and not parts['checked']:
                parts['old'].checked = False
            if not parts['old'].checked and parts['checked']:
                parts['old'].checked = True

            if parts['old'].text != parts['content']:
                parts['old'].text = parts['content']


def get_note_instance(keep, id=None, **kwargs):
    if id:
        note = keep.get(id)
    else:
        notes = keep.find(**query_params(keep, **kwargs))
        note = next(notes, None)
    return note


@click.group(cls=GkeepGroup)
def notes():
    """Manage Google Keep notes using ``notes`` command.
    This command has subcommands for adding, searching, editing, or
    deleting notes. To see all subcommands of ``notes`` use ``--help``::

        gkeep notes --help

    An example of a subcommand is ``add``. To see help use
    ``gkeep notes add --help``.
    """
    pass


@notes.command('add', options_metavar='[options]')
@click.option('--color', default='', callback=get_click_color, metavar='<color>',
              help='Set note color. Choices: {}'.format(', '.join(COLOR_NAMES)))
@click.option('--labels', default='', callback=comma_separated, metavar='<label>',
              help='Set note labels. Add multiple labels separated by commas')
@click.argument('title', metavar='<title>')
@click.argument('text', metavar='<note_content>')
@click.pass_context
def add_note(ctx, color, labels, title, text):
    """Add a new note to Google Keep.
    A title and a message body are required for the new note. For example:

    .. code-block:: shell

        gkeep notes add "Today's tasks" "Install gkeep cli and configure it"

    The syntax is:
    """
    keep = ctx.obj['keep']
    gnote = keep.createNote(title, text)
    if color:
        gnote.color = color
    add_labels(keep, gnote, labels)
    keep.sync()


@notes.command('search', options_metavar='[options]')
@click.option('--color', default='', callback=get_click_color, metavar='<color>',
              help='Filter by note color. Choices: {}'.format(', '.join(COLOR_NAMES)))
@click.option('--labels', default='', callback=comma_separated, metavar='<labels>',
              help='Filter by label notes. Filter by multiple labels separated by commas.')
@click.option('--deleted/--not-deleted', default=None,
              help='Filter by deleted notes or not')
@click.option('--trashed/--not-trashed', default=None,
              help='Filter by deleted notes or not')
@click.option('--pinned/--not-pinned', default=None,
              help='Filter by pinned notes or not')
@click.option('--archived/--not-archived', default=None,
              help='Filter by archived notes or not')
@click.option('--title', default=None, metavar='<title>',
              help='Filter by title note')
@click.option('--text', default=None, metavar='<note_content>',
              help='Search in note content')
@click.argument('query', default='', metavar='[query]')
@click.pass_context
def search_notes(ctx, **kwargs):
    """Search for notes using filters or/and use query text. For example:

    .. code-block:: shell

        gkeep notes search --not-deleted "GKeep installed"

    The syntax is:
    """
    keep = ctx.obj['keep']
    for note in keep.find(**query_params(keep, **kwargs)):
        print_note(note)


@notes.command('get', options_metavar='[options]')
@click.argument('id', default=None, required=False, metavar='[id]')
@click.option('--title', default=None,
              help='Filter by title note', metavar='<title>')
@click.option('--query', default='', help='Search in any note field', metavar='<term>')
@click.pass_context
def get_note(ctx, **kwargs):
    """Get a note by its id or by its title or text. If the id is unknown,
    you can use the ``--title`` and/or ``--text`` filters. For example:

    .. code-block:: shell

        gkeep notes get 161d1ad8c82.b2ed17d26167c9bc

    The syntax is:
    """
    keep = ctx.obj['keep']
    note = get_note_instance(keep, **kwargs)
    if note:
        print_note(note)
    else:
        click.echo('The note was not found', err=True)
        sys.exit(2)


@notes.command('edit', options_metavar='[options]')
@click.option('--title', default=None, required=False, metavar='<new title>',
              help='Change the note title')
@click.option('--text', default=None, required=False, is_flag=False, flag_value=placeholder, metavar='[new_note_content]',
              help='Change the note text')
@click.option('--filter-id', default=None, required=False, metavar='<id>',
              help='Filter by id note. This is the preferred way to ensure editing the correct note')
@click.option('--filter-title', default=None, metavar='<title>',
              help='Filter by note title. The titles of the notes are not unique')
@click.option('--filter-query', default='', metavar='<term>',
              help='search in titles and body of the notes. This is the least accurate filter')
@click.option('--color', default='', callback=get_click_color, metavar='<color>',
              help='Change note color. Choices: {}'.format(', '.join(COLOR_NAMES)))
@click.option('--archived/--not-archived', default=None,
              help='Archive or unarchive note.')
@click.option('--pinned/--not-pinned', default=None,
              help='Pin or unpin note.')
@click.option('--labels', default='', callback=comma_separated, metavar='<new labels>',
              help='Set note labels')
@click.pass_context
def edit_note(ctx, title, text, color, labels, archived, pinned, filter_id, filter_title, filter_query):
    """It is possible to edit an existing note. The following parameters
    are available to choose the note to edit. For example:

    .. code-block:: shell

        gkeep notes edit --filter-title "Today's tasks" --text "GKeep installed, continue reading the docs"

    The syntax is:
    """
    keep = ctx.obj['keep']
    note = get_note_instance(keep, id=filter_id, title=filter_title, query=filter_query)
    if not note:
        click.echo('The note was not found', err=True)
        sys.exit(2)
    if text == placeholder:
        if isinstance(note, List):
            edit_note_checkboxes(note)
            text = None
        else:
            text = click.edit(note.text).strip()
    updated = {}
    boolean_nullables = ['archived', 'pinned']  # 3 state params
    for param in ['title', 'text', 'color', 'labels'] + boolean_nullables:
        value = locals()[param]
        if value or (param in boolean_nullables and value is not None):
            updated[param] = (getattr(note, param), value)
            setattr(note, param, value)
    if labels:
        add_labels(keep, note, labels)
    keep.sync()
    click.echo('Updated note fields:\n\n' + ('\n'.join([u'{}: {} 🠞 {}'.format(param, values[0], values[1])
                                                        for param, values in updated.items()])))


@notes.command('delete', options_metavar='[options]')
@click.argument('id', default=None, required=False, metavar='[id]')
@click.option('--title', default=None, help='Filter by title note', metavar='<title>')
@click.option('--query', default='', help='Search in any note field', metavar='<term>')
@click.pass_context
def delete_note(ctx, **kwargs):
    """It works just like get-note. Delete a note by its id or by its title
    or text. If the id is unknown, you can use the --title and/or --text filters.
    For example:

    .. code-block:: shell

        gkeep notes delete 161d1ad8c82.b2ed17d26167c9bc

    The syntax is:
    """
    keep = ctx.obj['keep']
    note = get_note_instance(keep, **kwargs)
    if note and (note.deleted or note.trashed):
        click.echo('The note "{}" had already been deleted.'.format(note.title))
    elif note:
        note.delete()
        keep.sync()
        click.echo('Note with title "{}" deleted.'.format(note.title))
    else:
        click.echo('The note was not found', err=True)
        sys.exit(2)