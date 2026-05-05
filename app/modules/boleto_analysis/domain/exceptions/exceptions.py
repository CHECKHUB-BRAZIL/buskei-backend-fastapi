class BoletoDomainError(Exception):
    """
    Exceção base do domínio de validação de boletos.
    Todas as exceções de domínio herdam desta classe,
    permitindo captura genérica na camada de aplicação.
    """
    

class InvalidBoletoCodeError(BoletoDomainError):
    """
    Levantada quando o código do boleto é inválido.

    Causas possíveis:
    - Tamanho incorreto (não é 44, 47 ou 48 dígitos)
    - Contém caracteres não numéricos
    - Dígito verificador incorreto
    """

    def __init__(self, code: str, reason: str = "Código de boleto inválido.") -> None:
        self.code = code
        self.reason = reason
        super().__init__(f"Código inválido: '{code}' — {reason}")


class InvalidAmountError(BoletoDomainError):
    """
    Levantada quando o valor monetário extraído do boleto é inválido.

    Causas possíveis:
    - Valor negativo
    - Formato não numérico
    - Sequência de dígitos de valor com tamanho incorreto
    """

    def __init__(self, raw: str, reason: str = "Valor monetário inválido.") -> None:
        self.raw = raw
        self.reason = reason
        super().__init__(f"Valor inválido: '{raw}' — {reason}")


class UnsupportedBoletoTypeError(BoletoDomainError):
    """
    Levantada quando o tipo do boleto não é reconhecido.

    O domínio suporta apenas boletos de cobrança (bancários)
    e de convênio (concessionárias/governo — iniciam com '8').
    """

    SUPPORTED_TYPES = ("cobranca", "convenio")

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(
            f"Tipo de boleto não suportado identificado por: '{identifier}'. "
            f"Tipos aceitos: {', '.join(self.SUPPORTED_TYPES)}."
        )


class BoletoValidationNotFoundError(BoletoDomainError):
    """
    Levantada quando uma validação buscada por código não existe
    no repositório.
    """

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Nenhuma validação encontrada para o código: '{code}'")


class DuplicateBoletoValidationError(BoletoDomainError):
    """
    Levantada quando se tenta persistir uma validação para um código
    de boleto que já foi validado anteriormente.
    """

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Já existe uma validação registrada para o código: '{code}'")
