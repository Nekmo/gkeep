import json
import os

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
