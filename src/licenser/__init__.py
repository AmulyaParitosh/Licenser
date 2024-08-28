from pathlib import Path

from .interface import LicenserInterface


def main():
    cli = LicenserInterface(Path.cwd())
    cli.run()
