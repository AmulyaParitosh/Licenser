def fetch_license_text(spdx_identifier: str) -> str:
    try:
        with open(
            f"src/licenser/templates/{spdx_identifier}.txt", "r", encoding="utf-8"
        ) as f:
            return f.read()

    except FileNotFoundError as err:
        raise ValueError(
            f"Failed to fetch license text for SPDX identifier: {spdx_identifier}"
        ) from err
