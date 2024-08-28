import argparse
import datetime
import re
from pathlib import Path
from typing import List, Optional

import argcomplete

from . import services
from .config import Config


class LicenserInterface:

    def __init__(self, working_dir: Path) -> None:
        try:
            self.config = Config(working_dir)
        except FileNotFoundError as e:
            print(e)
            exit(1)

    def create_parser(self) -> argparse.ArgumentParser:

        parser = argparse.ArgumentParser(
            description="Generate license files with SPDX identifier."
        )

        subparsers = parser.add_subparsers(title="command", help="Licenser commands")

        create_parser = subparsers.add_parser("create", help="Create a license file")

        create_parser.add_argument(
            "spdx",
            type=str,
            help="SPDX identifier of the license to generate",
            choices=list(self.config.available_licenses.keys()),
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

        generate_config_parser = subparsers.add_parser(
            "generate_config",
            help="generates a default config file if not already existing",
        )
        generate_config_parser.set_defaults(func=self.generate_config_command)

        argcomplete.autocomplete(parser)
        return parser

    def run(self, args: Optional[List[str]] = None) -> None:
        parser = self.create_parser()
        if args:
            parsed_args = parser.parse_args(args)
        else:
            parsed_args = parser.parse_args()

        parsed_args.func(parsed_args)

    def create_command(self, args: argparse.Namespace) -> None:
        self.config.spdx = args.spdx

        if (self.config.working_dir / "LICENSE").exists() and not args.overwrite:
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

        try:
            services.create_license_file(
                str(args.spdx),
                int(args.year),
                str(args.author),
                str(args.email),
                self.config.working_dir,
            )
            self.config.write_config()
            print(f"{args.spdx} license file generated successfully.")
        except ValueError as e:
            print(e)
            exit(1)
        except FileNotFoundError:
            print(f"SPDX identifier :{args.spdx} is not supported")
            exit(1)

    def header_command(self, args: argparse.Namespace) -> None:
        if not self.config.config_file.exists():
            print(f"config not found at {self.config.config_file}.")
            exit(1)

        if not args.dir:
            services.add_license_header(
                args.path,
                self.config.header_content,
                spdx=self.config.spdx,
                author=self.config.author,
                email=self.config.email,
            )
            return

        def recursive_add_license_header(directory: Path) -> None:
            for path in directory.iterdir():
                if path.is_dir():
                    recursive_add_license_header(path)
                elif path.is_file() and args.regex and re.match(args.regex, path.name):
                    services.add_license_header(
                        path,
                        self.config.header_content,
                        spdx=self.config.spdx,
                        author=self.config.author,
                        email=self.config.email,
                    )

        recursive_add_license_header(args.path)

    def generate_config_command(self, args: argparse.Namespace) -> None:
        default_config_template = Path("src/licenser/templates/default.licenserConfig")
        if self.config.config_file.exists():
            print(".licenserConfig already exists")
            exit(1)

        config = Config(default_config_template)
        config.header_content = (
            config.header_content.replace("%%SPDX%%", config.spdx)
            .replace("%%AUTHOR%%", config.author)
            .replace("%%EMAIL%%", config.email)
        )
        config.write_config()
