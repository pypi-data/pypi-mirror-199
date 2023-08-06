from datetime import datetime, timezone
from typing import Any

from .claims import JWTEncodeClaims
from .decoder import JWTDecoder
from .encoder import JWTEncoder


ACCESS_TOKEN_GRANT_TYPE = "access"
REFRESH_TOKEN_GRANT_TYPE = "refresh"


class JWTTokenPairIssuer:
    def __init__(
        self,
        encoder: JWTEncoder,
        decoder: JWTDecoder,
        access_token_claims: JWTEncodeClaims,
        refresh_token_claims: JWTEncodeClaims,
    ) -> None:
        self.encoder = encoder
        self.decoder = decoder
        self.access_token_claims = access_token_claims
        self.refresh_token_claims = refresh_token_claims

    def create_pair(self, data: dict[str, Any]) -> tuple[str, str]:
        """
        Creates access and refresh token with the same data,
        but with different claims. Access and refresh token has
        one additional header "grant_type" to distinguish
        tokens between each other.
            For access_token "grant_type"="access".
            For refresh_token "grant_type"="refresh".
        """
        timestamp = datetime.now(tz=timezone.utc)
        return (
            self.encoder.encode(
                data,
                claims=self.access_token_claims,
                timestamp=timestamp,
                extra_headers={"grant_type": ACCESS_TOKEN_GRANT_TYPE},
            ),
            self.encoder.encode(
                data,
                claims=self.refresh_token_claims,
                timestamp=timestamp,
                extra_headers={"grant_type": REFRESH_TOKEN_GRANT_TYPE},
            ),
        )

    def refresh(self, refresh_token: str) -> str:
        payload = self.decoder.decode(refresh_token)
        headers = self.decoder.get_headers(refresh_token)
        if headers.get("grant_type", None) != REFRESH_TOKEN_GRANT_TYPE:
            raise ValueError('"grant_type" header missing or invalid')
        return self.encoder.encode(
            payload["payload"],
            claims=self.access_token_claims,
            extra_headers={"grant_type": ACCESS_TOKEN_GRANT_TYPE},
        )


def decode_access_token(
    decoder: JWTDecoder, access_token: str
) -> dict[str, Any]:
    payload = decoder.decode(access_token)
    headers = decoder.get_headers(access_token)
    if headers.get("grant_type", None) != ACCESS_TOKEN_GRANT_TYPE:
        raise ValueError('"grant_type" header missing or invalid')
    return payload["payload"]  # type: ignore


def decode_refresh_token(
    decoder: JWTDecoder, refresh_token: str
) -> dict[str, Any]:
    payload = decoder.decode(refresh_token)
    headers = decoder.get_headers(refresh_token)
    if headers.get("grant_type", None) != REFRESH_TOKEN_GRANT_TYPE:
        raise ValueError('"grant_type" header missing or invalid')
    return payload["payload"]  # type: ignore
