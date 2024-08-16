import argparse
import datetime
from pathlib import Path

import argcomplete

from .config import Config
from .services import create_file, update_pyproject_license
from .utils import LicenseNotSupportedError


class LicenserInterface:

    config: Config = Config()
    args: argparse.Namespace

    def __init__(self, config: Config) -> None:
        self.config = config
        self.license_path: Path = config.WORKING_DIR / "LICENSE"

        self.parser = argparse.ArgumentParser(
            description="Generate license files with SPDX identifier."
        )
        argcomplete.autocomplete(self.parser)

        self.parser.add_argument(
            "spdx",
            type=str,
            help="SPDX identifier of the license to generate",
            choices=list(config.available_licenses.keys()),
        )
        self.parser.add_argument("--author", type=str, help="Author name")
        self.parser.add_argument("--email", type=str, help="Author email")
        self.parser.add_argument("--year", type=str, help="Year")
        self.parser.add_argument(
            "-o",
            help="Overwrite existing LICENSE file",
            action="store_true",
        )

    def parse_args(self) -> None:
        args = self.parser.parse_args()

        if self.license_path.exists() and not args.o:
            raise FileExistsError(
                "LICENSE file already exists. Use -o to force overwrite."
            )

        if not args.author:
            args.author = input(f"Author name({self.config.author}): ")
            if args.author == "":
                args.author = self.config.author

        if not args.email:
            args.email = input(f"Author email({self.config.email}): ")
            if args.email == "":
                args.email = self.config.email

        if not args.year:
            args.year = input(f"Year({datetime.datetime.now().year}): ")
            if args.year == "":
                args.year = str(datetime.datetime.now().year)

        self.args = args

    def run(self):
        try:
            self.parse_args()
            create_file(
                self.args.spdx,
                self.args.year,
                self.args.author,
                self.args.email,
                self.config.WORKING_DIR / "LICENSE",
            )
            update_pyproject_license(self.args.spdx)

        except FileExistsError as err:
            print(err)
            exit(1)

        except LicenseNotSupportedError as err:
            print(err)
            exit(1)
