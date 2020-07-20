import click

from google_keep_tasks.utils import pretty_date


@click.group()
def labels():
    """Gkeep can manage Google Keep labels using ``labels`` command.
    This command has subcommands for adding, searching, editing, or
    deleting labels. To see all subcommands of ``labels`` use ``--help``::

        gkeep labels --help

    An example of a subcommand is ``add``. To see help use
    ``gkeep labels add --help``.
    """
    pass


@labels.command('list')
@click.pass_context
def list_labels(ctx):
    """List labels on Google Keep. For example:

    .. code-block:: shell

        gkeep labels list

    The syntax is:
    """
    keep = ctx.obj['keep']
    # TODO: created & updated must be optional
    click.echo(u'\n'.join([
        u'━ {} (created {}, updated {})'.format(
            label.name,
            pretty_date(label.timestamps.created),
            pretty_date(label.timestamps.updated),
        ) for label in keep.labels()]
    ))
