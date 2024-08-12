class LicenseNotSupportedError(Exception):
    def __init__(self, license_name: str) -> None:
        return super().__init__(
            f"Unknown or UnSupported SPDX identifier {license_name}"
        )


def fetch_license_text(spdx_identifier: str) -> str:
    try:
        with open(
            f"src/licenser/templates/{spdx_identifier}.txt", "r", encoding="utf-8"
        ) as f:
            return f.read()

    except FileNotFoundError as err:
        raise LicenseNotSupportedError(spdx_identifier) from err
