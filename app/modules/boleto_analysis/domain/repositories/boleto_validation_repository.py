from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.boleto_analysis.domain.entities.boleto_validation_entity import (
    BoletoValidationEntity,
)
from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import BoletoCode


class BoletoValidationRepository(ABC):
    """
    Contrato (porta) do repositório de validações de boletos.

    Responsabilidades:
    - Definir as operações de persistência necessárias ao domínio.
    - Permanecer completamente agnóstico à tecnologia de storage.

    A implementação concreta fica na camada de infraestrutura,
    seguindo o princípio de Inversão de Dependência (DIP).
    """

    @abstractmethod
    def save(self, validation: BoletoValidationEntity) -> None:
        """
        Persiste uma nova validação de boleto.

        Raises:
            DuplicateBoletoValidationError: se já existir validação
                para o mesmo código (em implementações que não permitem duplicatas).
        """

    @abstractmethod
    def find_by_code(self, code: BoletoCode) -> Optional[BoletoValidationEntity]:
        """
        Busca a validação mais recente associada a um código de boleto.

        Returns:
            A entidade encontrada ou None se não houver registro.
        """

    @abstractmethod
    def find_all(self) -> List[BoletoValidationEntity]:
        """
        Retorna todas as validações armazenadas, ordenadas da mais recente.

        Returns:
            Lista de entidades (pode ser vazia).
        """

    @abstractmethod
    def delete_by_code(self, code: BoletoCode) -> None:
        """
        Remove a validação associada a um código de boleto.

        Raises:
            BoletoValidationNotFoundError: se não existir validação para o código.
        """

    @abstractmethod
    def exists(self, code: BoletoCode) -> bool:
        """
        Verifica se já existe uma validação registrada para o código.

        Returns:
            True se existir, False caso contrário.
        """
