
import yaml
import secrets
from pathlib import Path
from os.path import exists

ROOT_DIR = Path(__file__).parents[2]
config_file = f'{ROOT_DIR}/cfg/config.yml'


def test_config_file():
    # Check if database exists. If not, create it.
    file_exists = exists(config_file)
    if not file_exists:
        print(f'Configfile aanmaken..')
        token = secrets.token_urlsafe()
        with open(config_file, 'x') as f:
            f.write(f'appName: werfklas \n\
logLevel: WARN \n\
\n\
database: \n\
    path: \'{ROOT_DIR}/\'\n\
    name: \'werfklas.db\' \n\
\n\
flask: \n\
  secretKey: \'{token}\' \
        ')
        f.close()


def load_config():
    with open(config_file, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg