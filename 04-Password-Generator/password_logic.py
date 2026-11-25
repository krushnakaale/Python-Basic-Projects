import secrets
import string


def generate(length=16, upper=True, lower=True, digits=True, symbols=True, exclude=False):
    if not 8 <= length <= 128:
        raise ValueError('Length must be between 8 and 128.')
    groups = [s for enabled, s in zip((upper, lower, digits, symbols), (string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation)) if enabled]
    if exclude:
        groups = [''.join(c for c in s if c not in 'Il1O0o|') for s in groups]
    if not groups:
        raise ValueError('Select at least one character type.')
    pool = ''.join(groups)
    while True:
        password = ''.join(secrets.choice(pool) for _ in range(length))
        if all(any(c in group for c in password) for group in groups):
            return password
