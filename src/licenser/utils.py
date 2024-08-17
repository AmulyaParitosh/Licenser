from pathlib import Path

from .config import Config


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


LICENSE_TAG = "%license_header%"


def convert_to_multiline_comment(text, file_extension):
    comments = {
        "js": "/*{}*/",  # JavaScript
        "java": "/*{}*/",  # Java
        "c": "/*{}*/",  # C
        "cpp": "/*{}*/",  # C++
        "cs": "/*{}*/",  # C#
        "php": "/*{}*/",  # PHP
        "rb": "=begin\n{}\n=end",  # Ruby
        "swift": "/*{}*/",  # Swift
        "kt": "/*{}*/",  # Kotlin
        "html": "<!--{}-->",  # HTML
        "css": "/*{}*/",  # CSS
        "sql": "/*{}*/",  # SQL
        "sh": ": '{}'",  # Bash
        "go": "/*{}*/",  # Go
        "r": "# {}",  # R (line by line)
        "py": "# {}",  # Python (line by line)
        "m": "%{{\n{}\n%}}",  # MATLAB
    }

    # For Python & R, we need to handle line by line comment addition
    if file_extension in {"py", "r"}:
        text = text.replace("\n", "\n# ")
        return text

    if file_extension not in comments:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    # Retrieve the comment template
    comment_template = comments[file_extension]

    return comment_template.format(text)


def prepare_license_header(license_header_text: str, file_extension: str) -> str:
    spdx: str = str(Config._parse_config().get("spdx"))
    license_header = (
        "\n" + LICENSE_TAG + "\n" + license_header_text + "\n" + LICENSE_TAG + "\n"
    )
    license_header = convert_to_multiline_comment(license_header, file_extension)
    license_header = license_header.replace("%%SPDX%%", spdx)

    return license_header


def remove_license_header(file_content: str) -> str:
    content = file_content.split("\n")
    i = 0
    n = len(content)

    while i < n:
        line = content[i]

        if LICENSE_TAG in line[-len(LICENSE_TAG) :]:
            content.pop(i - 1)
            i -= 1
            content.pop(i)
            line = content[i]
            while LICENSE_TAG not in line:
                content.pop(i)
                line = content[i]
            content.pop(i)
            content.pop(i)
            return "\n".join(content)

        i += 1

    print("remaining content", content)
    return "\n".join(content)


def update_pyproject_license(new_spdx: str, pyproject_path: Path) -> None:
    original_pyproject_data = pyproject_path.read_text(encoding="utf-8")
    original_license_section = extract_license_from_pyproject(pyproject_path)

    new_license_section = f'{"{"}text = "{new_spdx}"{"}"}'
    new_pyproject_data = original_pyproject_data.replace(
        original_license_section, new_license_section
    )

    pyproject_path.write_text(new_pyproject_data, encoding="utf-8")
