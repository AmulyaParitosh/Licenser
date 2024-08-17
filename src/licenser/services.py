from pathlib import Path

from . import utils


def create_license_file(
    spdx_identifier: str,
    year: int,
    author: str,
    email: str,
    working_dir: Path,
) -> None:
    try:
        license_text = utils.fetch_license_text(spdx_identifier)
        license_text = (
            license_text.replace("[year]", str(year))
            .replace("[fullname]", author)
            .replace("[email]", email)
        )

        (working_dir / "LICENSE").write_text(license_text, encoding="utf-8")

        print(f"{spdx_identifier} license file generated successfully.")
    except ValueError as e:
        print(e)

    pyproject: Path = working_dir / "pyproject.toml"
    if pyproject.exists():
        utils.update_pyproject_license(spdx_identifier, pyproject)


def add_license_header(file_path: Path, license_header: str) -> None:
    content = file_path.read_text(encoding="utf-8")
    content_without_header = utils.remove_license_header(content)

    license_header = utils.prepare_license_header(license_header, file_path.suffix[1:])
    modified_content = license_header + "\n" + content_without_header

    file_path.write_text(modified_content, encoding="utf-8")
