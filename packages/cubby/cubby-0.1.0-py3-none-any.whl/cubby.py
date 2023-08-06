from __future__ import annotations

import subprocess
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import requests

host = os.environ.get("CUBBY_HOST", "https://cubby.reillybrothers.net")


@dataclass(frozen=True)
class CubbyStuff:
    cubby_hole: str
    stuff: Any
    createdAt: str
    updatedAt: str

    @property
    def _cubby(self) -> Cubby:
        return Cubby(Path(self.cubby_hole))

    def put(self, stuff: Any) -> CubbyStuff:
        return self._cubby.put(stuff)

    def update(self, stuff: Any) -> CubbyStuff:
        return self._cubby.update(stuff)

    def delete(self):
        return self._cubby.delete()

    @property
    def link(self) -> str:
        return self._cubby.link

    def web(self):
        self._cubby.web()


@dataclass(frozen=True)
class Cubby:
    _cubby_hole_path: Path = Path("")

    def web(self):
        subprocess.run(["open", self.link])

    @property
    def link(self) -> str:
        return f"{host}/cubbies/cubby/{self._cubby_hole}"

    @property
    def _cubby_hole(self) -> str:
        return str(self._cubby_hole_path).removeprefix(".").removeprefix("/")

    def __dir__(self) -> Iterable[str]:
        return (
            *dir(super()),
            *sorted(
                (
                    x.removeprefix(self._cubby_hole + "/").split("/")[0]
                    for x in requests.get(
                        f"{host}/api/cubbies/search?cubby_hole_prefix={self._cubby_hole}"
                    ).json()
                    if not self._cubby_hole or x.startswith(self._cubby_hole + "/")
                ),
                reverse=True,
            ),
        )

    def __getattr__(self, path: str) -> Cubby:
        return Cubby(self._cubby_hole_path / path)

    def take(self) -> CubbyStuff:
        return CubbyStuff(
            **requests.get(f"{host}/api/cubbies/{self._cubby_hole}").json()
        )

    def delete(self):
        requests.delete(f"{host}/api/cubbies/{self._cubby_hole}")

    def put(self, stuff) -> CubbyStuff:
        return CubbyStuff(
            **requests.post(
                f"{host}/api/cubbies/{self._cubby_hole}",
                json=dict(stuff=json.dumps(stuff)),
            ).json()
        )

    def update(self, stuff) -> CubbyStuff:
        return CubbyStuff(
            **requests.patch(
                f"{host}/api/cubbies/{self._cubby_hole}",
                json=dict(stuff=stuff),
            ).json()
        )


cubby = Cubby()

if __name__ != "__main__" and "pytest" not in sys.modules:
    sys.modules[__name__] = cubby  # type: ignore
