import logging
from typing import Any

from jwt import PyJWT, PyJWTError, get_unverified_header

from .claims import JWTDecodeClaims
from .exceptions import JWTDecodeException
from .identities import Identity


class JWTDecoder:
    identity: Identity
    jwt: PyJWT
    logger: logging.Logger
    default_claims: JWTDecodeClaims

    def __init__(
        self,
        identity: Identity,
        claims: JWTDecodeClaims,
        py_jwt: PyJWT = PyJWT(),  # type: ignore
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        self.jwt = py_jwt
        self.logger = logger
        self.identity = identity
        self.default_claims = claims

    def decode(
        self, token: str, claims: JWTDecodeClaims | None = None
    ) -> dict[str, Any]:
        if claims is None:
            claims = self.default_claims
        return self._decode(
            jwt=token,
            key=self.identity.get_decode_key(),
            algorithms=[self.identity.algorithm.value],
            **claims.get_defined(),
        )

    def _decode(self, **options: Any) -> dict[str, Any]:
        try:
            self.logger.debug(f'Decoding "{options}".')
            return self.jwt.decode(**options)
        except PyJWTError as error:
            self.logger.debug(
                f'Interrupt decoding "{options}". Error: {error}'
            )
            raise JWTDecodeException(error) from error

    def get_headers(self, token: str) -> dict[str, str]:
        return get_unverified_header(token)

    def get_identity(self) -> Identity:
        return self.identity
