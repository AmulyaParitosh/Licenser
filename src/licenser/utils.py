from pathlib import Path

LICENSE_TAG = "%license_header%"

LANG_COMMENT_MAP = {
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


def extract_license_from_pyproject(pyproject_path: Path) -> str:
    # TODO: can be done with regex, look into it later

    pyproject_data = pyproject_path.read_text(encoding="utf-8")

    key = "license = "
    _, temp = pyproject_data.split(key)
    temp, _ = temp.split("\n", 1)
    return temp.strip()


def update_pyproject_license(new_spdx: str, pyproject_path: Path) -> None:
    original_pyproject_data = pyproject_path.read_text(encoding="utf-8")
    original_license_section = extract_license_from_pyproject(pyproject_path)

    new_license_section = f'{"{"}text = "{new_spdx}"{"}"}'
    new_pyproject_data = original_pyproject_data.replace(
        original_license_section, new_license_section
    )

    pyproject_path.write_text(new_pyproject_data, encoding="utf-8")


def prepare_license_header(
    license_header_text: str, file_extension: str, **kwargs
) -> str:
    license_header = (
        license_header_text.replace("%%SPDX%%", kwargs.get("spdx", "%%SPDX%%"))
        .replace("%%AUTHOR%%", kwargs.get("author", "%%AUTHOR%%"))
        .replace("%%EMAIL%%", kwargs.get("email", "%%EMAIL%%"))
    )
    license_header = (
        "\n" + LICENSE_TAG + "\n" + license_header + "\n" + LICENSE_TAG + "\n"
    )

    # For Python & R, we need to handle line by line comment addition
    if file_extension in {"py", "r"}:
        text = license_header.replace("\n", "\n# ")
        return text

    # Retrieve the comment template
    try:
        comment_template = LANG_COMMENT_MAP[file_extension]
    except KeyError as e:
        raise ValueError(f"Unsupported file extension: {file_extension}") from e

    return comment_template.format(license_header)


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

    return "\n".join(content)
