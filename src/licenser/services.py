import json
import os
from pathlib import Path

from .utils import fetch_license_text


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


def update_pyproject_license(
    new_spdx: str, pyproject_path: Path = Path("pyproject.toml")
):

    # TODO: can be done with regex, look into it later

    key = "license = "
    with pyproject_path.open("r", encoding="utf-8") as f:
        original_pyproject_data = f.read()

    _, temp = original_pyproject_data.split(key)
    temp, _ = temp.split("\n", 1)
    original_license_section = temp.strip()
    new_license_section = f'{"{"}text = "{new_spdx}"{"}"}'
    new_pyproject_data = original_pyproject_data.replace(
        original_license_section, new_license_section
    )

    with pyproject_path.open("w", encoding="utf-8") as f:
        f.write(new_pyproject_data)


def prepend_line(file_name, line):
    dummy_file = f"{file_name}.bak"

    with open(file_name, "r") as read_obj, open(dummy_file, "w") as write_obj:
        write_obj.write(line + "\n")
        for line in read_obj:
            write_obj.write(line)

    os.remove(file_name)
    os.rename(dummy_file, file_name)


def insert_text_in_file(file_path, position, text_to_insert):
    with open(file_path, "r") as file:
        content = file.read()

    modified_content = content[:position] + text_to_insert + content[position:]

    with open(file_path, "w") as file:
        file.write(modified_content)


# dir_path = Path(".dev_utils/t")

# text = Path(".dev_utils/source_code_license.txt").read_text()

# # Insert text in the file at the end of the directory.
# for path in dir_path.rglob("*.py"):
#     # prepend_line(str(path), text)
#     insert_text_in_file(str(path), 478, "")
