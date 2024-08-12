from .cli import LicenserInterface
from .config import Config


def main():
    config = Config()
    cli = LicenserInterface(config)
    cli.run()
    cli.create_file()
