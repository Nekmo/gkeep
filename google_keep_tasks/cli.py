import click


def choices_prompt(text, choices, default_choice):
    choices_descriptions = ['  [{}]{}'.format(choice[0].upper() if default_choice == choice[0] else choice[0],
                                              choice[1:])
                            for choice in choices]
    choices_letters = [choice[0].upper() if default_choice == choice[0] else choice[0] for choice in choices]
    choice = click.prompt(
        '{}\n\n'.format(text) +
        '\n'.join(choices_descriptions) +
        '\nEnter a choice [{}]'.format('/'.join(choices_letters)),
        default=default_choice, show_default=False
    )
    if not next(iter(filter(lambda x: x == choice.lower(), map(lambda x: x.lower(), choices_letters))), None):
        return default_choice
    return choice.lower()


class GkeepHelpFormatter(click.HelpFormatter):
    def write(self, string):
        """Remove rst characters."""
        return super().write(string.replace('``', ''))


class GkeepContext(click.Context):
    def make_formatter(self):
        return GkeepHelpFormatter(width=self.terminal_width,
                                  max_width=self.max_content_width)


class GkeepGroup(click.Group):
    def make_context(self, info_name, args, parent=None, **extra):
        for key, value in self.context_settings.items():
            if key not in extra:
                extra[key] = value
        ctx = GkeepContext(self, info_name=info_name, parent=parent, **extra)
        with ctx.scope(cleanup=False):
            self.parse_args(ctx, args)
        return ctx