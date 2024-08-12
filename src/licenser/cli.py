import argparse
import datetime

import argcomplete

from .config import Config
from .constants import available_licenses
from .utils import LicenseNotSupportedError, fetch_license_text


class LicenserInterface:

    def __init__(self, config: Config) -> None:
        self.config = config
        self.license_path = config.WORKING_DIR / "LICENSE"

        self.parser = argparse.ArgumentParser(
            description="Generate license files with SPDX identifier."
        )
        argcomplete.autocomplete(self.parser)

        self.parser.add_argument(
            "spdx",
            type=str,
            help="SPDX identifier of the license to generate",
            choices=list(available_licenses.keys()),
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

        if self.license_path.exists() and not args.f:
            raise FileExistsError(
                "LICENSE file already exists. Use -f to force overwrite."
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

    def create_file(self) -> None:
        try:
            license_text = fetch_license_text(self.args.spdx)
            license_text = (
                license_text.replace("[year]", self.args.year)
                .replace("[fullname]", self.args.author)
                .replace("[email]", self.args.email)
            )

            self.license_path.write_text(license_text, encoding="utf-8")

            print(f"{self.args.spdx} license file generated successfully.")
        except ValueError as e:
            print(e)

    def run(self):
        try:
            self.parse_args()

        except FileExistsError as err:
            print(err)
            exit(1)

        except LicenseNotSupportedError as err:
            print(err)
            exit(1)
