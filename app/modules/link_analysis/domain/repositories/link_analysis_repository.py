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
    def save(self, analysis: LinkAnalysisEntity, user_id: str) -> None:
        """
        Persiste uma nova análise associada a um usuário.
        """

    @abstractmethod
    def find_by_url(self, url: URL, user_id: str) -> Optional[LinkAnalysisEntity]:
        """
        Busca análise de uma URL pertencente a um usuário.
        """

    @abstractmethod
    def find_all(self, user_id: str) -> List[LinkAnalysisEntity]:
        """
        Retorna todas as análises de um usuário.
        """

    @abstractmethod
    def delete_by_url(self, url: URL, user_id: str) -> None:
        """
        Remove a análise de uma URL pertencente a um usuário.
        """

    @abstractmethod
    def exists(self, url: URL, user_id: str) -> bool:
        """
        Verifica se existe análise para URL dentro do escopo do usuário.
        """
