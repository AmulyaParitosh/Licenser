from pathlib import Path

from . import utils
from .config import Config


def create_license_file(
    spdx_identifier: str,
    year: int,
    author: str,
    email: str,
    working_dir: Path,
) -> None:
    license_text = (
        (Config.app_dir / f"src/licenser/templates/{spdx_identifier}.txt")
        .read_text(encoding="utf-8")
        .replace("[year]", str(year))
        .replace("[fullname]", author)
        .replace("[email]", email)
    )

    (working_dir / "LICENSE").write_text(license_text, encoding="utf-8")

    pyproject_path = Config.working_dir / "pyproject.toml"
    if pyproject_path.exists():
        utils.update_pyproject_license(spdx_identifier, pyproject_path)


def add_license_header(file_path: Path, license_header: str, **kwargs) -> None:
    content = file_path.read_text(encoding="utf-8")

    license_header = utils.prepare_license_header(
        license_header, file_path.suffix[1:], **kwargs
    )

    file_path.write_text(
        license_header + "\n" + utils.remove_license_header(content),
        encoding="utf-8",
    )
