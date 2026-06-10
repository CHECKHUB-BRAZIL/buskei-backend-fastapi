from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        """
        Gera hash da senha.
        """
        ...

    @abstractmethod
    def verify(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verifica se a senha corresponde ao hash.
        """
        ...

    @abstractmethod
    def needs_rehash(
        self,
        hashed_password: str,
    ) -> bool:
        """
        Verifica se o hash precisa ser atualizado.
        """
        ...
