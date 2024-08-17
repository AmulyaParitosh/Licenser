from .config import Config, DefaultConfigPath
from .interface import LicenserInterface


def main():
    config = Config(DefaultConfigPath)
    cli = LicenserInterface(config)
    cli.run()
