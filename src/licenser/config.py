# create a descriptor for git credentials

import subprocess
from typing import Optional


class GitUserCredential:

    def __init__(self, name: Optional[str] = None):
        self.credential_identifier = name

    def __set_name__(self, owner, name):
        if self.credential_identifier is None:
            self.credential_identifier = name

    def __get__(self, obj, objtype=None):
        try:
            credential = (
                subprocess.check_output(
                    ["git", "config", f"user.{self.credential_identifier}"]
                )
                .strip()
                .decode("utf-8")
            )
            return credential
        except subprocess.CalledProcessError:
            return None


class Config:

    author = GitUserCredential("name")
    email = GitUserCredential()


x = Config()
print(x.author)
print(x.email)
