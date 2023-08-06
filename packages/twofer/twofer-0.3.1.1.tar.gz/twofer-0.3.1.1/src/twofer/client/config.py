# twofer.client.config

import os

import appdirs
import dotenv


__all__ = [
    'USER_DATA_DIR', 'CLIENT_DATA_FILE', 'CLIENT_CA_FILE', 'CLIENT_TIMEOUT'
]


USER_DATA_DIR = appdirs.user_data_dir('twofer')

# dotenv
dotenv.load_dotenv()
twofer_client_env = os.getenv('TWOFER_CLIENT_ENV', 'twofer-client.env')
dotenv.load_dotenv(twofer_client_env)

CLIENT_DATA_FILE = os.getenv('TWOFER_CLIENT_DATA_FILE',
                             os.path.join(USER_DATA_DIR, 'twofer-client-data.json'))
CLIENT_CA_FILE = os.getenv('TWOFER_CLIENT_CA_FILE')
CLIENT_TIMEOUT = int(os.getenv('TWOFER_CLIENT_TIMEOUT', 60))


if __name__ == '__main__':
    d = globals()
    for varname in __all__:
        print(f'{varname}: {d[varname]!r}')
