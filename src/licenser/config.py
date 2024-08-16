import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, Union


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
    add_dir = Path(__file__).parent.parent.parent
    available_licenses: Dict[str, Dict[str, str]] = json.loads(
        Path("src/licenser/templates/licenses_index.json").read_text(encoding="utf-8")
    )
    pyproject_path = Path("pyproject.toml")

    @classmethod
    def test_config(cls) -> "Config":
        config = cls()
        config.working_dir = Path("example")
        config.pyproject_path = Path("example/pyproject.toml")
        return config


if __name__ == "__main__":
    x = Config()
    print(x.add_dir)
    print(x.email)
