import yaml
import io
import logging
from discord.utils import get
from discord.ext.commands import Bot

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Constants:

    def __init__(self, bot, color) -> None:
        self.bot = bot
        self.color = color


class SmetchBot:

    def __init__(self, prefix: str, token: str) -> None:
        self.prefix = prefix
        self.token = token
        return


class Color:

    def __init__(self, color_dict) -> None:
        color = color_dict[0]
        for color_name in color:
            current_hex = color[color_name]
            current_hex = current_hex.replace('#', '0x')
            color[color_name] = hex(int(current_hex, 16))
            setattr(self, color_name, color[color_name])


class Roles:

    def __init__(self, bot: Bot, roles: dict) -> None:
        for role in roles:
            discord_role = get(bot.guilds[0].roles, roles[role])
            if discord_role is None:
                continue
            else:
                setattr(self, role.lower(), discord_role)
        return


def load_config_file(config_filename: str = 'config.yml'):
    '''Load all configuration constants from file'''
    try:
        config_file: io.TextIOWrapper = io.open(config_filename)
        log.info(f'Successfully opened the {config_filename} file')
        return config_file
    except FileNotFoundError as err:
        log.critical(
            f"No {config_filename} file was found. \
            Please make sure the file is called '{config_filename}'. \
            Make sure it is in the top level directory."
        )
        log.exception(f'Missing {config_filename}', exc_info=True)
        raise err


def parse_config_file(config_file: io.TextIOWrapper):
    '''Parse the config file into a dictionary'''
    try:
        config: dict = yaml.safe_load(config_file)
        log.info('Successfully parsed the config file')
        return config
    except Exception as err:
        log.critical('Failed to parse the config file for an unknown reason')
        log.exception('Failed YAML parsing', exc_info=True)
        raise err


def load_configuration(config_filename: str = 'config.yml'):
    config_file = load_config_file(config_filename)
    config_dict = parse_config_file(config_file)

    required: list = ['bot-token', 'prefix']

    for key in required:
        try:
            config_dict.__getitem__(key)
            log.info(f'Successfully loaded the required constant: \'{key}\'')
        except KeyError as err:
            log.critical(f'Missing {key} from {config_filename}')
            log.exception(f'Missing {key}', exc_info=True)
            raise err

    config = {}
    for yaml_key in config_dict:
        new_key = yaml_key.upper().replace('-', '_')
        config[new_key] = config_dict[yaml_key]

    return config


def get_constants(bot: Bot, config_filename: str = 'config.yml'):
    config = load_configuration(config_filename)
    constants = Constants(
        bot=Bot(
            prefix=config['PREFIX'],
            token=config['BOT_TOKEN']
        ),
        color=Color(
            color_dict=config['COLOR']
        ),
        roles=Roles(
            bot=bot,
            roles=config['ROLES']
            )
    )
    return constants
