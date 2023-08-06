from importlib import metadata


try:
    VERSION = metadata.version(__name__)
except:
    VERSION = 'unknown'
