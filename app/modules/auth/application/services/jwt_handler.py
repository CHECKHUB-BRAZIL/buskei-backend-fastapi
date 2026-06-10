from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional


class JWTHandler(ABC):
    @abstractmethod
    def create_access_token(
        self,
        user_id: str,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        ...

    @abstractmethod
    def create_refresh_token(
        self,
        user_id: str,
    ) -> str:
        ...

    @abstractmethod
    def decode_token(
        self,
        token: str,
        expected_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_user_id_from_token(
        self,
        token: str,
    ) -> str:
        ...

    @abstractmethod
    def verify_token_type(
        self,
        token: str,
        expected_type: str,
    ) -> bool:
        ...

    @abstractmethod
    def get_token_expiration(
        self,
        token: str,
    ) -> datetime:
        ...

    @abstractmethod
    def is_token_expired(
        self,
        token: str,
    ) -> bool:
        ...
