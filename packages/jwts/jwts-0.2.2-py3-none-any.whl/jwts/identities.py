import abc
from dataclasses import dataclass
from typing import Any, Callable

from .algorithms import Algorithms, PemAlgorithms, PlainAlgorithms


class Identity(abc.ABC):
    algorithm: Algorithms

    @abc.abstractmethod
    def get_encode_key(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_decode_key(self) -> Any:
        raise NotImplementedError


@dataclass
class PlainIdentity(Identity):
    secret_key_loader: Callable[[], str]
    algorithm: PlainAlgorithms

    secret_key: str | None = None

    def get_encode_key(self) -> Any:
        if self.secret_key is None:
            return self.load_secret_key()
        return self.secret_key

    def load_secret_key(self) -> str:
        self.secret_key = self.secret_key_loader()
        return self.secret_key

    def get_decode_key(self) -> Any:
        if self.secret_key is None:
            return self.load_secret_key()
        return self.secret_key


@dataclass
class PemIdentity(Identity):
    algorithm: PemAlgorithms
    public_key_loader: Callable[[], bytes] | None = None
    private_key_loader: Callable[[], bytes] | None = None

    public_key: bytes | None = None
    private_key: bytes | None = None

    def get_encode_key(self) -> Any:
        if self.private_key is None:
            return self.load_private_key()
        return self.private_key

    def load_private_key(self) -> bytes:
        if self.private_key_loader is None:
            raise ValueError("Private key loader is not defined")
        self.private_key = self.private_key_loader()
        return self.private_key

    def get_decode_key(self) -> Any:
        if self.public_key is None:
            return self.load_public_key()
        return self.public_key

    def load_public_key(self) -> bytes:
        if self.public_key_loader is None:
            raise ValueError("Public key loader is not defined")
        self.public_key = self.public_key_loader()
        return self.public_key
