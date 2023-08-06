from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from .utils import to_unix_timestamp


@dataclass(frozen=True)
class JWTEncodeClaims:
    set_iat: bool = True
    iss: str | None = None
    aud: list[str] | None = None
    exp: timedelta | None = None
    nbf: timedelta | None = None

    def get_defined(self, timestamp: datetime) -> dict[str, Any]:
        claims: dict[str, Any] = {}
        if self.exp:
            claims["exp"] = to_unix_timestamp(timestamp + self.exp)
        if self.nbf:
            claims["nbf"] = to_unix_timestamp(timestamp + self.nbf)
        if self.iss:
            claims["iss"] = self.iss
        if self.aud:
            claims["aud"] = self.aud
        if self.set_iat:
            claims["iat"] = to_unix_timestamp(timestamp)
        return claims


@dataclass
class JWTDecodeClaims:
    issuer: str | None = None
    leeway: int | None = None
    audience: str | None = None
    require: list[str] = field(default_factory=lambda: ["exp", "iat", "nbf"])

    def get_defined(self) -> dict[str, Any]:
        claims: dict[str, Any] = {"options": {"require": self.require}}
        if self.issuer:
            claims["issuer"] = self.issuer
        if self.leeway:
            claims["leeway"] = self.leeway
        if self.audience:
            claims["audience"] = self.audience
        return claims
