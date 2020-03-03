#!/usr/bin/env python3
"""Generate DynamoDB exceptions.

Boto3 creates exceptions dynamically from a service model which is not
desirable, because it breaks static analysis. This script generates a Python
file from the dynamically loaded Boto3 exceptions and puts it in
dokklib_db/exceptions.py

"""
import boto3


IGNORE_EXCEPTIONS = {
    # We provide our own ClientError implementation for type checking coverage
    'ClientError',
    # We provide our own TransactionCanceledException that contains
    # cancellation reasons.
    'TransactionCanceledException'
}

MISSING_EXCEPTIONS = {
    # These exceptions are not raised by Boto3, but they are returned as
    # transaction cancellation reasons.
    'ThrottlingError',
    'ValidationError'
}


def _get_exception(name):
    return [
        f'class {name}(ClientError):',
        '    """Please check DynamoDB docs for documentation."""',
        '',
        ''
    ]


# Must match earliest support version
assert boto3.__version__ == '1.10.34', boto3.__version__


lines = [
    '"""Autogenerated DynamoDB exceptions.',
    '',
    'This file was autogenerated by scripts/generate_exceptions.py.',
    'Do not edit it manually!',
    '',
    '"""',
    'from dokklib_db.errors.client import ClientError',
    '',
    ''
]

client = boto3.client('dynamodb')
for name in dir(client.exceptions):
    if name[0].isupper() and name not in IGNORE_EXCEPTIONS:
        assert name not in MISSING_EXCEPTIONS, name
        lines.extend(_get_exception(name))

for name in MISSING_EXCEPTIONS:
    lines.extend(_get_exception(name))

# Remove duplicate empty line
lines = lines[:-1]
with open('dokklib_db/errors/exceptions.py', 'w') as f:
    f.write('\n'.join(lines))
