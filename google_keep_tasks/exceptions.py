import sys


class GKeepError(Exception):
    body = ''

    def __init__(self, extra_body=''):
        self.extra_body = extra_body

    def __str__(self):
        msg = self.__class__.__name__
        if self.body:
            msg += ': {}'.format(self.body)
        if self.extra_body:
            msg += ('. {}' if self.body else ': {}').format(self.extra_body)
        return msg


class ItemNotFound(GKeepError):
    def __init__(self, text):
        super(ItemNotFound, self).__init__('Item text not found: {}'.format(text))


class LoginError(GKeepError):
    body = 'Check credentials file. The syntax is: <username> <password>.'


def catch(fn):
    def wrap(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except GKeepError as e:
            sys.stderr.write('[Error] GKeep Exception:\n{}\n'.format(e))
    return wrap
