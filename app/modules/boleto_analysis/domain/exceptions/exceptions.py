class BoletoDomainError(Exception):
    """
    Exceção base do domínio de validação de boletos.

    Usada apenas para erros que impedem o processamento do boleto
    (erros estruturais, parsing inválido, etc).
    """
    pass


# ==========================================================
# ERROS DE VALIDAÇÃO (BLOQUEANTES)
# ==========================================================

class InvalidBoletoCodeError(BoletoDomainError):
    """
    Levantada quando o código do boleto é estruturalmente inválido.

    Casos reais:
    - Contém caracteres não numéricos
    - Tamanho inválido impossível de interpretar
    - Falha na conversão de linha digitável
    """

    def __init__(self, code: str, reason: str = "Código de boleto inválido.") -> None:
        self.code = code
        self.reason = reason
        super().__init__(f"Código inválido: '{code}' — {reason}")


class InvalidAmountError(BoletoDomainError):
    """
    Levantada quando o valor monetário extraído do boleto é inválido.

    Casos reais:
    - Formato inválido
    - Conversão impossível
    - Valor corrompido estruturalmente
    """

    def __init__(self, raw: str, reason: str = "Valor monetário inválido.") -> None:
        self.raw = raw
        self.reason = reason
        super().__init__(f"Valor inválido: '{raw}' — {reason}")


class UnsupportedBoletoTypeError(BoletoDomainError):
    """
    Levantada quando o boleto não pertence aos tipos suportados
    pelo domínio (cobrança ou convênio).
    """

    SUPPORTED_TYPES = ("cobranca", "convenio")

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(
            f"Tipo de boleto não suportado: '{identifier}'. "
            f"Tipos aceitos: {', '.join(self.SUPPORTED_TYPES)}."
        )
