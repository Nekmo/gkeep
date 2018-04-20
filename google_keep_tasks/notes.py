import click
import gkeepapi

from google_keep_tasks.exceptions import InvalidColor
from google_keep_tasks.management import cli


def add_color(note, color):
    if not color:
        return
    color = color.title()
    if color and not hasattr(gkeepapi.node.ColorValue, color):
        raise InvalidColor(color)
    note.color = getattr(gkeepapi.node.ColorValue, color)


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


def comma_separated(ctx, param, value):
    return value.split(',') if value else []


@cli.command('add-note')
@click.option('--color', default='')
@click.option('--labels', default='', callback=comma_separated)
@click.argument('title')
@click.argument('text')
@click.pass_context
def add_note(ctx, color, labels, title, text):
    keep = ctx.obj['keep']
    gnote = keep.createNote(title, text)
    add_color(gnote, color)
    add_labels(keep, gnote, labels)
    keep.sync()
