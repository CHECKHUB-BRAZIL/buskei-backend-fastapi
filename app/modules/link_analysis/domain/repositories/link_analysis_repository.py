from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.link_analysis.domain.entities.link_entity import LinkAnalysisEntity
from app.modules.link_analysis.domain.value_objects.url_vo import URL


class LinkAnalysisRepository(ABC):
    """
    Contrato (porta) do repositório de análises de links.

    Responsabilidades:
    - Definir as operações de persistência necessárias ao domínio.
    - Permanecer completamente agnóstico à tecnologia de storage
      (banco relacional, NoSQL, cache, memória, etc.).

    A implementação concreta fica na camada de infraestrutura,
    seguindo o princípio de Inversão de Dependência (DIP).
    """

    @abstractmethod
    async def save(self, analysis: LinkAnalysisEntity) -> None:
        """
        Persiste uma nova análise.

        Args:
            analysis: Entidade de análise a ser salva.

        Raises:
            DuplicateAnalysisError: Se já existir análise para a mesma URL
                                    em implementações que não permitem duplicatas.
        """

    @abstractmethod
    async def find_by_url(self, url: URL) -> Optional[LinkAnalysisEntity]:
        """
        Busca a análise mais recente associada a uma URL.

        Args:
            url: Value Object da URL pesquisada.

        Returns:
            A entidade encontrada ou None se não houver registro.
        """

    @abstractmethod
    async def find_all(self) -> List[LinkAnalysisEntity]:
        """
        Retorna todas as análises armazenadas.

        Returns:
            Lista de entidades (pode ser vazia).
        """

    @abstractmethod
    async def delete_by_url(self, url: URL) -> None:
        """
        Remove a análise associada a uma URL.

        Args:
            url: Value Object da URL cujo registro deve ser excluído.

        Raises:
            AnalysisNotFoundError: Se não existir análise para a URL informada.
        """

    @abstractmethod
    async def exists(self, url: URL) -> bool:
        """
        Verifica se já existe uma análise registrada para a URL.

        Args:
            url: Value Object da URL a verificar.

        Returns:
            True se existir, False caso contrário.
        """
