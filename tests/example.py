from pathlib import Path

# from licenser.config import Config
from licenser.interface import LicenserInterface


def run(arg_str: str):
    # config = Config(Path("example").absolute())
    cli = LicenserInterface(Path("example"))

    args = arg_str.split()
    cli.run(args)


if __name__ == "__main__":
    # run("create BSD-3-Clause --author John --email john@test.com --year 2024 -o")
    # run("create BSD-3-Clause -o")
    run('header -d . ".*.py"')
    # run("-h")
    # add_license_header(Path("example/test.py"), Path("example/.license_header"))
