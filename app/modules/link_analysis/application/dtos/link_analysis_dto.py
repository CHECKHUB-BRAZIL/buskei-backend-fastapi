from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class AnalyzeLinkInputDTO:
    """
    Dados de entrada para o caso de uso de análise de link.
    Recebido diretamente da camada de apresentação (controller/endpoint).
    """
    url: str  # string bruta — o caso de uso valida e converte para URL VO
    user_id: str 


@dataclass(frozen=True)
class AnalyzeLinkOutputDTO:
    """
    Dados de saída após a análise de um link.
    Exposto para a camada de apresentação — sem objetos de domínio.
    """
    url: str
    risk: str                  # "safe" | "medium" | "high"
    reasons: List[str]
    created_at: datetime
    user_id: str 


@dataclass(frozen=True)
class GetAnalysisInputDTO:
    """
    Dados de entrada para buscar uma análise já existente por URL.
    """
    url: str
    user_id: str 


@dataclass(frozen=True)
class DeleteAnalysisInputDTO:
    url: str
    user_id: str


@dataclass(frozen=True)
class GetAnalysisOutputDTO:
    """
    Dados de saída ao recuperar uma análise existente.
    Idêntico ao OutputDTO de análise — mantido separado por
    clareza semântica e para permitir evolução independente.
    """
    url: str
    risk: str
    reasons: List[str]
    created_at: datetime
    user_id: str 


@dataclass(frozen=True)
class ListAnalysesInputDTO:
    user_id: str
