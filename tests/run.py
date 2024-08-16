from pathlib import Path

from licenser.config import Config
from licenser.interface import LicenserInterface
from licenser.services import add_license_header


def run(arg_str: str):
    config = Config.test_config()
    cli = LicenserInterface(config)

    args = arg_str.split()
    cli.run(args)


if __name__ == "__main__":
    # run("BSD-3-Clause --author John --email john@test.com --year 2024 -o")
    add_license_header(Path("example/test.py"), Path("example/.license_header"))
