from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.boleto_analysis.domain.entities.boleto_validation_entity import (
    BoletoValidationEntity,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import (
    BoletoCode,
)


class BoletoValidationRepository(ABC):
    """
    Contrato (porta) do repositório de validações de boletos.
    """

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    @abstractmethod
    def save(
        self,
        validation: BoletoValidationEntity,
    ) -> None:
        """
        Persiste uma nova validação.
        """

    # ------------------------------------------------------------------
    # Find by code
    # ------------------------------------------------------------------

    @abstractmethod
    def find_by_code(
        self,
        code: BoletoCode,
        user_id: str,
    ) -> Optional[BoletoValidationEntity]:
        """
        Busca uma validação de boleto do usuário.
        """

    # ------------------------------------------------------------------
    # Find all
    # ------------------------------------------------------------------

    @abstractmethod
    def find_all(
        self,
        user_id: str,
    ) -> List[BoletoValidationEntity]:
        """
        Lista todas as validações do usuário.
        """

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    @abstractmethod
    def delete_by_code(
        self,
        code: BoletoCode,
        user_id: str,
    ) -> None:
        """
        Remove uma validação do usuário.
        """

    # ------------------------------------------------------------------
    # Exists
    # ------------------------------------------------------------------

    @abstractmethod
    def exists(
        self,
        code: BoletoCode,
        user_id: str,
    ) -> bool:
        """
        Verifica se o usuário já possui validação
        para esse boleto.
        """

    # ------------------------------------------------------------------
    # Find by status
    # ------------------------------------------------------------------

    @abstractmethod
    def find_by_status(
        self,
        status: str,
        user_id: str,
    ) -> List[BoletoValidationEntity]:
        """
        Busca validações por status para um usuário.
        """
