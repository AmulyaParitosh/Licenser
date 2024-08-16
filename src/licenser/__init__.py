from .config import Config
from .interface import LicenserInterface


def main():
    config = Config()
    cli = LicenserInterface(config)
    cli.run()
