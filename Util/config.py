import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('.\config.ini')
    return {
        "theme": config.get("Settings", "theme", fallback="light"),
        "language": config.get("Settings", "language", fallback="en")
    }

def save_config(config):
    config_parser = configparser.ConfigParser()
    config_parser['Settings'] = {
        "theme": config.get("theme", "light")
    }
    with open('config.ini', 'w') as configfile:
        config_parser.write(configfile)

config = load_config()

def create_default_config():
    if not config:
        default_config = {
            "theme": "system",
            "language": "en"
        }
        save_config(default_config)