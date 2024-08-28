import json
import re
import subprocess
from pathlib import Path
from typing import Dict, TypedDict, Union, cast


class ConfigDict(TypedDict):
    author: str
    email: str
    spdx: str
    header: Dict[str, str]


RawConfigDict = Dict[str, Union[str, Dict[str, str]]]
TEMPLATE_DIR = Path(__file__).parent / "templates"


def get_git_credentials(name: str) -> str:
    try:
        return (
            subprocess.check_output(["git", "config", f"user.{name}"])
            .strip()
            .decode("utf-8")
        )
    except subprocess.CalledProcessError:
        return ""


class ConfigParser:

    @staticmethod
    def decode(file_path: Path) -> RawConfigDict:
        config = {}
        current_section = None
        multiline_content = []
        is_multiline = False

        for line in file_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            if section_match := re.match(r"\[(.*?)\]", line):
                current_section = section_match.group(1)
                config[current_section] = {}
            elif line == "'''":
                if is_multiline:
                    if current_section:
                        config[current_section]["content"] = "\n".join(
                            multiline_content
                        )
                    multiline_content = []
                is_multiline = not is_multiline
            elif is_multiline:
                multiline_content.append(line)
            elif "=" in line:
                key, value = map(str.strip, line.split("=", 1))
                if current_section:
                    config[current_section][key] = value
                else:
                    config[key] = value

        return config

    @staticmethod
    def encode(config: Union[ConfigDict, RawConfigDict]) -> str:
        lines = []
        for key, value in config.items():
            if isinstance(value, dict):
                lines.append(f"\n[{key}]")
                for subkey, subvalue in value.items():
                    if subkey != "content":
                        lines.append(f"{subkey} = {subvalue}")
                if "content" in value:
                    lines.extend(["'''", value["content"], "'''"])
            else:
                lines.append(f"{key} = {value}")
        return "\n".join(lines)


class Config:
    author: str = get_git_credentials("name")
    email: str = get_git_credentials("email")
    working_dir: Path = Path.cwd()
    config_path: Path = working_dir / ".licenserConfig"
    default_config_template: Path = TEMPLATE_DIR / "default.licenserConfig"

    def __init__(self, working_dir: Path) -> None:
        self.working_dir = working_dir
        self.config_file = working_dir / ".licenserConfig"

        if not self.config_file.exists():
            with self.config_file.open("w+", encoding="utf-8") as f:
                f.write(self.default_config_template.read_text(encoding="utf-8"))

        self.__config: ConfigDict = cast(
            ConfigDict, ConfigParser.decode(self.config_file)
        )

        self.available_licenses = json.loads(
            (TEMPLATE_DIR / "licenses_index.json").read_text(encoding="utf-8")
        )

        self.author = (
            self.__config["author"] if self.__config["author"] else self.author
        )
        self.email = self.__config["email"] if self.__config["email"] else self.email
        self.spdx = self.__config.get("spdx", "MIT")
        self.header_content: str = self.__config["header"]["content"]

    def write_config(self) -> None:
        self.__config["author"] = self.author
        self.__config["email"] = self.email
        self.__config["spdx"] = self.spdx
        self.__config["header"]["content"] = self.header_content

        self.config_file.write_text(
            ConfigParser.encode(self.__config), encoding="utf-8"
        )


if __name__ == "__main__":
    test_config = Config(Path.cwd())
    print(f"Author: {test_config.author}")
    print(f"Email: {test_config.email}")
    print(f"SPDX: {test_config.spdx}")
    print(f"Working Directory: {test_config.working_dir}")
    test_config.spdx = "Apache-2.0"
    test_config.write_config()
