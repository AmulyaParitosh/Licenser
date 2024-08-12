import argparse
import datetime

# from os import path
from pathlib import Path

import argcomplete

from .config import Config
from .constants import available_licenses
from .utils import fetch_license_text

WORKING_DIR = Path.cwd()
print(WORKING_DIR)


class LicenserInterface:

    def __init__(self, config: Config) -> None:
        self.license_path = WORKING_DIR / "LICENSE"
        self.config = config

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
            "-f", type=str, help="Force overwrite existing LICENSE file"
        )

    def run(self) -> None:
        args = self.parser.parse_args()

        if self.license_path.exists() and not args.f:
            print("LICENSE file already exists. Use -f to force overwrite.")
            return

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

            with self.license_path.open("w", encoding="utf-8") as f:
                f.write(license_text)

            print(f"{self.args.spdx} license file generated successfully.")
        except ValueError as e:
            print(e)
