from pathlib import Path

from .utils import (
    extract_license_from_pyproject,
    fetch_license_text,
    prepare_license_header,
    remove_license_header,
)


def create_file(
    spdx_identifier: str, year: int, author: str, email: str, file_path: Path
) -> None:
    try:
        license_text = fetch_license_text(spdx_identifier)
        license_text = (
            license_text.replace("[year]", str(year))
            .replace("[fullname]", author)
            .replace("[email]", email)
        )

        file_path.write_text(license_text, encoding="utf-8")

        print(f"{spdx_identifier} license file generated successfully.")
    except ValueError as e:
        print(e)


def update_pyproject_license(new_spdx: str, pyproject_path: Path) -> None:
    original_pyproject_data = pyproject_path.read_text(encoding="utf-8")
    original_license_section = extract_license_from_pyproject(pyproject_path)

    new_license_section = f'{"{"}text = "{new_spdx}"{"}"}'
    new_pyproject_data = original_pyproject_data.replace(
        original_license_section, new_license_section
    )

    pyproject_path.write_text(new_pyproject_data, encoding="utf-8")


def add_license_header(file_path: Path, license_header_path: Path) -> None:
    license_header = license_header_path.read_text()
    license_header = prepare_license_header(license_header)

    content = file_path.read_text(encoding="utf-8")
    content_without_header = remove_license_header(content)

    modified_content = license_header + "\n" + content_without_header
    file_path.write_text(modified_content, encoding="utf-8")
