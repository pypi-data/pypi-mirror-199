import logging
from datetime import datetime, timezone
from typing import Any

from jwt import PyJWT, PyJWTError, get_unverified_header

from .claims import JWTEncodeClaims
from .exceptions import JWTEncodeException
from .identities import Identity


class JWTEncoder:
    identity: Identity
    jwt: PyJWT
    logger: logging.Logger
    default_claims: JWTEncodeClaims

    def __init__(
        self,
        identity: Identity,
        claims: JWTEncodeClaims,
        py_jwt: PyJWT = PyJWT(),  # type: ignore
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        self.jwt = py_jwt
        self.logger = logger
        self.identity = identity
        self.default_claims = claims

    def encode(
        self,
        data: dict[str, Any],
        claims: JWTEncodeClaims | None = None,
        timestamp: datetime | None = None,
        extra_headers: dict[str, Any] = {},
    ) -> str:
        if timestamp is None:
            timestamp = datetime.now(tz=timezone.utc)
        if claims is None:
            claims = self.default_claims
        return self._encode(
            payload=self.create_payload(data, claims, timestamp),
            key=self.identity.get_encode_key(),
            algorithm=self.identity.algorithm.value,
            headers=extra_headers,
        )

    def create_payload(
        self,
        data: dict[str, Any],
        claims: JWTEncodeClaims,
        timestamp: datetime,
    ) -> dict[str, Any]:
        payload = claims.get_defined(timestamp)
        payload["payload"] = data
        return payload

    def _encode(self, **options: Any) -> str:
        try:
            self.logger.debug(f'Encoding "{options}".')
            return self.jwt.encode(**options)
        except PyJWTError as error:
            self.logger.debug(
                f'Interrupt encoding "{options}". Error: {error}'
            )
            raise JWTEncodeException(error) from error

    def get_headers(self, token: str) -> dict[str, str]:
        return get_unverified_header(token)

    def get_identity(self) -> Identity:
        return self.identity
