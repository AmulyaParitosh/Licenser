import argparse
import datetime
import re
from pathlib import Path
from typing import List, Optional

import argcomplete

from . import services
from .config import Config


class LicenserInterface:

    config: Config
    args: argparse.Namespace

    def __init__(self, config: Config = Config()) -> None:
        self.config = config

        self.parser = argparse.ArgumentParser(
            description="Generate license files with SPDX identifier."
        )
        argcomplete.autocomplete(self.parser)

        subparsers = self.parser.add_subparsers(
            title="command", help="Licenser commands"
        )

        create_parser = subparsers.add_parser("create", help="Create a license file")

        create_parser.add_argument(
            "spdx",
            type=str,
            help="SPDX identifier of the license to generate",
            choices=list(config.available_licenses.keys()),
        )
        create_parser.add_argument(
            "-i",
            "--interactive",
            help="Interactive mode",
            action="store_true",
        )
        create_parser.add_argument("--author", type=str, help="Author name")
        create_parser.add_argument("--email", type=str, help="Author email")
        create_parser.add_argument("--year", type=str, help="Year")
        create_parser.add_argument(
            "-o",
            "--overwrite",
            help="Overwrite existing LICENSE file",
            action="store_true",
        )
        create_parser.set_defaults(func=self.create_command)

        header_parser = subparsers.add_parser(
            "header", help="Add license header to files"
        )
        header_parser.add_argument(
            "-d",
            "--dir",
            help="Add license header to all files in directory",
            action="store_true",
        )
        header_parser.add_argument(
            "path",
            type=Path,
            help="path to add license header to",
        )
        header_parser.add_argument(
            "regex",
            type=str,
            help="regex pattern to match files",
        )
        header_parser.set_defaults(func=self.header_command)

    def run(self, args: Optional[List[str]] = None) -> None:
        if args:
            parsed_args = self.parser.parse_args(args)
        else:
            parsed_args = self.parser.parse_args()

        parsed_args.func(parsed_args)

    def create_command(self, args: argparse.Namespace) -> None:
        working_dir: Path = self.config.working_dir
        license_path: Path = working_dir / "LICENSE"

        if license_path.exists() and not args.overwrite:
            raise FileExistsError(
                "LICENSE file already exists. Use -o to force overwrite."
            )

        if not args.author:
            if args.interactive:
                args.author = input(f"Author name({self.config.author}): ")
            if not args.author:
                args.author = self.config.author

        if not args.email:
            if args.interactive:
                args.email = input(f"Author email({self.config.email}): ")
            if not args.email:
                args.email = self.config.email

        if not args.year:
            if args.interactive:
                args.year = input(f"Year({datetime.datetime.now().year}): ")
            if not args.year:
                args.year = datetime.datetime.now().year

        services.create_license_file(
            args.spdx,
            int(args.year),
            str(args.author),
            str(args.email),
            working_dir,
        )
        self.config.update_spdx(args.spdx)

    def header_command(self, args: argparse.Namespace) -> None:
        if not args.dir:
            services.add_license_header(
                args.path, self.config.header.get("content", "")
            )
            return

        def recursive_add_license_header(directory: Path) -> None:
            for path in directory.iterdir():
                if path.is_dir():
                    recursive_add_license_header(path)
                elif path.is_file() and args.regex and re.match(args.regex, path.name):
                    services.add_license_header(
                        path, self.config.header.get("content", "")
                    )

        recursive_add_license_header(args.path)
