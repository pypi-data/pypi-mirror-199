# twofer.server.config

import os

import dotenv


__all__ = [
    'TWITTER_CLIENT_ID', 'TWITTER_CLIENT_SECRET', 'TWITTER_BEARER_TOKEN',
    'FLASK_SECRET_KEY',
    'SERVER_HOST', 'SERVER_PORT', 'SERVER_GATEWAY_URL',
    'SERVER_DATA_FILE', 'SERVER_OWNER', 'SERVER_MEMBERS',
    'SERVER_TEMPLATE_DIR'
]


dotenv.load_dotenv()
twofer_server_env = os.getenv('TWOFER_SERVER_ENV', 'twofer-server.env')
dotenv.load_dotenv(twofer_server_env)

# These environment values are requied and cannot be started without them.
TWITTER_CLIENT_ID = os.environ['TWOFER_TWITTER_CLIENT_ID']
TWITTER_CLIENT_SECRET = os.environ['TWOFER_TWITTER_CLIENT_SECRET']
TWITTER_BEARER_TOKEN = os.environ['TWOFER_TWITTER_BEARER_TOKEN']
FLASK_SECRET_KEY = os.environ['TWOFER_FLASK_SECRET_KEY']

# These values are set to its default when they are not explicitly set,
# you want to basically specify them though.
SERVER_HOST = os.getenv('TWOFER_SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(os.getenv('TWOFER_SERVER_PORT', '8080'))
SERVER_GATEWAY_URL = os.getenv('TWOFER_SERVER_GATEWAY_URL', 'https://localhost')
SERVER_DATA_FILE = os.getenv('TWOFER_SERVER_DATA_FILE', 'twofer-server-data.json')
SERVER_OWNER = os.getenv('TWOFER_SERVER_OWNER', '_mshibata')
SERVER_MEMBERS = [x.strip() for x in os.getenv('TWOFER_SERVER_MEMBERS', '').split(',')]

# These values are optional.
SERVER_TEMPLATE_DIR = os.getenv('TWOFER_SERVER_TEMPLATE_DIR',
                                os.path.join(os.path.dirname(__file__), 'data', 'templates'))


if __name__ == '__main__':
    d = globals()
    for varname in __all__:
        print(f'{varname}: {d[varname]!r}')
