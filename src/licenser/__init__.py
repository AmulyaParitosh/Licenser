from .config import Config
from .interface import LicenserInterface


def main():
    cli = LicenserInterface(Config.config_path)
    cli.run()
