import json
import re
import subprocess
from pathlib import Path
from typing import Dict, Optional, Union

_ParsedConfigItem = Union[str, "_ParsedConfig", Path]
_ParsedConfig = Dict[str, _ParsedConfigItem]

DefaultConfigPath = Path.cwd() / ".licenserConfig"

class GitUserCredential:

    def __init__(self, name: Optional[str] = None) -> None:
        self.credential_identifier = name

    def __set_name__(self, owner, name) -> None:
        if self.credential_identifier is None:
            self.credential_identifier = name

    def __get__(self, obj, objtype=None) -> Union[str, None]:
        try:
            credential = (
                subprocess.check_output(
                    ["git", "config", f"user.{self.credential_identifier}"]
                )
                .strip()
                .decode("utf-8")
            )
            return credential
        except subprocess.CalledProcessError:
            return None


class Config:

    author = GitUserCredential("name")
    email = GitUserCredential()
    working_dir = Path.cwd()
    app_dir = Path(__file__).parent.parent.parent
    available_licenses: Dict[str, Dict[str, str]] = json.loads(
        (app_dir / "src/licenser/templates/licenses_index.json").read_text(
            encoding="utf-8"
        )
    )
    spdx: str
    header: Dict[str, str]

    def __init__(self, config_file: Path) -> None:
        if config_file.exists():
            self.__config: _ParsedConfig = self._parse_config(config_file)
        else:
            self.__config: _ParsedConfig = {}

        self.author = self.__config.get("author", self.author)
        self.email = self.__config.get("email", self.email)
        self.spdx = self.__config.get("spdx", "MIT")

    def __getattr__(self, name: str) -> _ParsedConfigItem:
        return self.__config.get(name, "")

    @classmethod
    def test_config(cls) -> "Config":
        config = cls(DefaultConfigPath)
        config.working_dir = Path("example")
        return config

    @staticmethod
    def _parse_config(file_path: Path = DefaultConfigPath) -> _ParsedConfig:
        config = {}
        current_section = None
        multiline_content = []
        is_multiline = False

        for line in file_path.read_text(encoding="utf-8").split("\n"):
            line = line.strip()

            # Skip comments
            if line.startswith("#"):
                continue

            # Check for section headers
            section_match = re.match(r"\[(.*?)\]", line)
            if section_match:
                current_section = section_match.group(1)
                config[current_section] = {}
                continue

            # Check for multiline start/end
            if line == "'''":
                if is_multiline:
                    # End of multiline block
                    if current_section:
                        config[current_section]["content"] = "\n".join(
                            multiline_content
                        )
                    multiline_content = []
                is_multiline = not is_multiline
                continue

            if is_multiline:
                multiline_content.append(line)
            else:
                # Parse key-value pairs
                if "=" in line:
                    key, value = map(str.strip, line.split("=", 1))
                    if current_section:
                        config[current_section][key] = value
                    else:
                        config[key] = value

        return config

    @staticmethod
    def _encode_config(config: _ParsedConfig) -> str:
        lines = []

        # Add top-level key-value pairs
        for key, value in config.items():
            if not isinstance(value, dict):
                lines.append(f"{key} = {value}")

        # Add sections
        for section, content in config.items():
            if isinstance(content, dict):
                lines.append(f"\n[{section}]")
                for key, value in content.items():
                    if key != "content":
                        lines.append(f"{key} = {value}")
                if "content" in content:
                    lines.append("'''")
                    lines.append(content["content"])
                    lines.append("'''")

        return "\n".join(lines)

    def write_config(self, file_path: Path = DefaultConfigPath) -> None:
        file_path.write_text(self._encode_config(self.__config), encoding="utf-8")

    def update_spdx(self, spdx: str):
        self.__config["spdx"] = spdx
        self.write_config()


if __name__ == "__main__":
    x = Config(DefaultConfigPath)
    print(x.app_dir)
    print(x.author)
    print(x.email)
    print(x.spdx)
    print(x.working_dir)
    print(x.header.get("content"))
    x.update_spdx("MIT")
