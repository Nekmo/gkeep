

def get_auth():
    return [val.rstrip('\n\r') for val in open('auth.txt').read().split(' ')]
