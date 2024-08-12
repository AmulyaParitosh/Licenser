import json
import subprocess

# import requests
from urllib import request

from .constants import available_licenses


def fetch_license_text(spdx_identifier: str):
    url = available_licenses[spdx_identifier]["url"]
    response = request.urlopen(url)

    if response.status == 200:
        license_data = json.loads(response.read().decode("utf-8"))
        return license_data["body"]

    raise ValueError(
        f"Failed to fetch license text for SPDX identifier: {spdx_identifier}"
    )
