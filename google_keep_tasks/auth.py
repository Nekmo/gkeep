import json
import os

import click
import gkeepapi
from click import Abort
from gkeepapi.exception import LoginException

from google_keep_tasks.cli import choices_prompt
from google_keep_tasks.exceptions import UnavailableLoginError, LoginError
from google_keep_tasks._compat import JSONDecodeError

AUTH_FILE = os.path.expanduser('~/.config/gkeep/auth.json')


def get_auth(file='auth.txt'):
    return [val.rstrip('\n\r') for val in open(file).read().split(' ')]


class GoogleKeepFileAuth(object):
    def __init__(self, file=None):
        self.file = file or AUTH_FILE

    def save_credentials(self, username, password):
        data = {'username': username, 'password': password}
        directory = os.path.dirname(AUTH_FILE)
        if not os.path.exists(directory):
            os.makedirs(directory, 0o700)
        json.dump(data, open(self.file, 'w'))

    def get_credentials(self):
        if not os.path.lexists(self.file):
            raise UnavailableLoginError('Credential files "{}" does not exists'.format(self.file))
        try:
            data = json.load(open(self.file))
        except JSONDecodeError as e:
            raise LoginError('Invalid json from credentials file: {}. Error: {}'.format(
                self.file, e
            ))
        if not isinstance(data, dict) or 'username' not in data or 'password' not in data:
            raise LoginError('Invalid credentials format file. username and password are required.')
        return data['username'], data['password']


class GoogleKeep(object):
    def __init__(self):
        self.keep = gkeepapi.Keep()
        self.auth = GoogleKeepFileAuth()

    def login_or_input(self):
        auth_changed = False
        input_login = False
        username = password = None
        try:
            username, password = self.auth.get_credentials()
        except UnavailableLoginError:
            click.echo('Welcome to Google Keep. Enter your username and password below. '
                       'If your account is protected, you need an application password: '
                       'https://support.google.com/mail/answer/185833')
            input_login = True
        except LoginError as e:
            click.echo('The credentials file is corrupt: {}. Credentials must be re-entered.'.format(e))
            input_login = True
        while True:
            if input_login:
                # Request new credentials
                auth_changed = True
                username, password = self.get_credencials_assistant(username)
            try:
                self.keep.login(username, password)
            except LoginException:
                choice = choices_prompt('Authentication failed, what do you want to do?', [
                    'Enter new credentials',
                    'retry',
                    'abort',
                ], 'e')
                if choice == 'e':
                    input_login = True
                elif choice == 'r':
                    input_login = False
                elif choice == 'a':
                    raise Abort
            else:
                if auth_changed:
                    self.auth.save_credentials(username, password)
                break

    def get_credencials_assistant(self, default_username):
        username = click.prompt('Enter your Google username', type=str,
                                show_default=True, default=default_username)
        password = click.prompt('Enter your password', hide_input=True)
        return username, password
