import click
import gkeepapi

from google_keep_tasks.exceptions import InvalidColor
from google_keep_tasks.management import cli


def get_color(color):
    if not color:
        return
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


@cli.command('add-note')
@click.option('--color', default='', callback=get_click_color)
@click.option('--labels', default='', callback=comma_separated)
@click.argument('title')
@click.argument('text')
@click.pass_context
def add_note(ctx, color, labels, title, text):
    keep = ctx.obj['keep']
    gnote = keep.createNote(title, text)
    if color:
        gnote.color = color
    add_labels(keep, gnote, labels)
    keep.sync()


@cli.command('search-notes')
@click.option('--color', default='', callback=get_click_color)
@click.option('--labels', default='', callback=comma_separated)
@click.option('--deleted/--not-deleted', default=None)
@click.option('--trashed/--not-trashed', default=None)
@click.option('--pinned/--not-pinned', default=None)
@click.option('--archived/--not-archived', default=None)
@click.option('--title', default=None)
@click.option('--text', default=None)
@click.argument('query', default='')
@click.pass_context
def search_notes(ctx, **kwargs):
    keep = ctx.obj['keep']
    # print(list(keep.find(query='Papel')))
    print(list(keep.find(**query_params(keep, **kwargs))))
