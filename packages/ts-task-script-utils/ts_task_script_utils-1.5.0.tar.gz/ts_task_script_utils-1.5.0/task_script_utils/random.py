"""Utility to generate a random UUID"""
import random as _py_random
import uuid as _uuid
from hashlib import sha512
from typing import Hashable


class NoPreviouslyCreatedSingletonError(Exception):
    pass


class Singleton(type):
    _instances = {}
    _last_created_instance = None

    def __call__(cls, *args, **kwargs):
        key = (cls, args)
        if key not in cls._instances:
            cls._instances[key] = super(Singleton, cls).__call__(*args, **kwargs)
        cls._last_created_instance = cls._instances[key]
        return cls._instances[key]

    def get_last_created(cls):
        if cls._last_created_instance is None:
            raise NoPreviouslyCreatedSingletonError()
        return cls._last_created_instance


class TSRandom:
    """
    Generate random values that are not available from Python 3.7's random module.
    """

    def __init__(self, *seed: Hashable):
        self._is_seeded = False
        self._random = _py_random.Random()

        if len(seed) > 0:
            self.seed(*seed)

    def seed(self, *content: Hashable) -> None:
        """
        Seed the random number generator.
        """
        content = (
            part.encode()
            if isinstance(part, str)
            else str(hash(part)).encode()
            if not isinstance(part, bytes)
            else part
            for part in content
        )

        try:
            hash_ = sha512(next(content))
        except StopIteration:
            return

        for part in content:
            hash_.update(part)
        rng_seed = hash_.digest()
        self._random.seed(rng_seed)
        self._is_seeded = True

    def randbytes(self, n: int) -> bytes:
        """Generate n random bytes."""
        if hasattr(self._random, "randbytes"):
            return self._random.randbytes(n)

        # Adapted from the Python 3.9+ random.randbytes method.
        return self._random.getrandbits(n * 8).to_bytes(n, "little")

    def uuid(self) -> _uuid.UUID:
        """Create a pseudo random UUID"""
        return _uuid.UUID(bytes=self.randbytes(16))


class TaskScriptUUIDGenerator(TSRandom, metaclass=Singleton):
    def __init__(self, task_script_identifier: str, file_identifier: Hashable):
        super().__init__(task_script_identifier, file_identifier)

    @classmethod
    def from_task_script_identifier_parts(
        cls, namespace: str, slug: str, version: str, file_identifier: Hashable
    ) -> "TaskScriptUUIDGenerator":
        """
        A convenience method that takes the parts of a task script identifier (namespace, slug, and version) and an
        identifier for the file (e.g. file location, file contents), then returns an instance of the generator class.
        """
        return cls(f"{namespace}/{slug}:{version}", file_identifier)
