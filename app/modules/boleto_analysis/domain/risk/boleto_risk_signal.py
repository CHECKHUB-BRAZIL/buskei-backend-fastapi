from dataclasses import dataclass


@dataclass(frozen=True)
class BoletoRiskSignal:
    """
    Representa um sinal de risco detectado na análise do boleto.

    NÃO interrompe o fluxo.
    Apenas contribui para o cálculo do score de risco.
    """

    code: str
    message: str
    score: int

    def __str__(self) -> str:
        return self.message
