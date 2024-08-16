from pathlib import Path


class LicenseNotSupportedError(Exception):

    def __init__(self, license_name: str) -> None:
        super().__init__(f"Unknown or UnSupported SPDX identifier {license_name}")


def fetch_license_text(spdx_identifier: str) -> str:
    try:
        with open(
            f"src/licenser/templates/{spdx_identifier}.txt", "r", encoding="utf-8"
        ) as f:
            return f.read()

    except FileNotFoundError as err:
        raise LicenseNotSupportedError(spdx_identifier) from err


def extract_license_from_pyproject(pyproject_path: Path) -> str:
    # TODO: can be done with regex, look into it later

    with pyproject_path.open("r", encoding="utf-8") as f:
        original_pyproject_data = f.read()

    key = "license = "
    _, temp = original_pyproject_data.split(key)
    temp, _ = temp.split("\n", 1)
    return temp.strip()


LICENSE_TAG = "# %license_header%"


def prepare_license_header(license_header_text: str) -> str:
    license_header = "\n" + license_header_text
    license_header = license_header.replace("\n", "\n# ")

    _, spdx, _ = extract_license_from_pyproject(Path("pyproject.toml")).split('"')
    license_header = license_header.replace("%%SPDX%%", spdx)

    license_header = LICENSE_TAG + license_header + LICENSE_TAG

    return license_header


def remove_license_header(file_content: str) -> str:
    content = file_content.splitlines()
    i = 0
    in_header = False
    while i < len(content):
        line = content[i]
        if not line or line[0] != "#":
            break

        if LICENSE_TAG in line and not in_header:
            in_header = True
        elif LICENSE_TAG in line and in_header:
            content.pop(i)
            break

        if in_header:
            content.pop(i)

    return "\n".join(content)
