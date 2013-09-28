# Python imports
import json
import os.path
from functools import partial


# Constants
_DIRNAME = os.path.abspath(
    os.path.dirname(__file__)
)
_MIMETYPES_PATH = os.path.join(_DIRNAME, 'mimetypes.json')
_EXCEPTIONS_PATH = os.path.join(_DIRNAME, 'exceptions.json')

MIMETYPES = json.load(open(_MIMETYPES_PATH))

# Extensions that are readable but aren't part of text/*
EXCEPTIONS = json.load(open(_EXCEPTIONS_PATH))


# Functions
def mimetype(url):
    """Get a mimetype for any given url or file path"""
    base, extension = os.path.splitext(url)
    return MIMETYPES.get(extension)


def _is_type(mimetype_base, url):
    mtype = mimetype(url)
    if not mtype:
        return False
    btype = mtype.split('/')[0]
    return mimetype_base == btype or mimetype_base == mtype


def is_type(*args):
    return _is_type(*reversed(args))


is_text = partial(_is_type, 'text')
is_audio = partial(_is_type, 'audio')
is_video = partial(_is_type, 'video')
is_image = partial(_is_type, 'image')
is_application = partial(_is_type, 'application')


def is_binary(url):
    """Says if a file should contain binary data or not"""
    mime = mimetype(url)
    return all([
        mime,
        not(is_text(url)),
        not(mime in EXCEPTIONS)
    ])


def is_readable(url):
    """Says if a file should contain text or not"""
    return not is_binary(url)
