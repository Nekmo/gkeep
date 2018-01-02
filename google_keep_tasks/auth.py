

def get_auth(file='auth.txt'):
    return [val.rstrip('\n\r') for val in open(file).read().split(' ')]
