from enum import Enum


class Algorithms(Enum):
    pass


class PlainAlgorithms(Algorithms):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"


class PemAlgorithms(Algorithms):
    ES256 = "ES256"
    ES256K = "ES256K"
    ES384 = "ES384"
    ES512 = "ES512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    PS256 = "PS256"
    PS384 = "PS384"
    PS512 = "PS512"
    EdDSA = "EdDSA"
