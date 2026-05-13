class LinkAnalysisDomainError(Exception):
    """
    Exceção base do domínio de análise de links.
    Todas as exceções de domínio herdam desta classe,
    permitindo captura genérica na camada de aplicação.
    """
    pass


class InvalidURLError(LinkAnalysisDomainError):
    """
    Levantada quando a URL fornecida não pode ser parseada
    ou não possui scheme/netloc válidos.

    Exemplos:
        - "nao-e-uma-url"
        - "ftp://" (sem netloc)
        - "" (vazia)
    """

    def __init__(self, url: str) -> None:
        self.url = url
        super().__init__(f"URL inválida ou malformada: '{url}'")


class URLTooLongError(LinkAnalysisDomainError):
    """
    Levantada quando a URL excede o comprimento máximo permitido.
    URLs excessivamente longas são um indicador comum de phishing.

    Limite: 2083 caracteres (padrão amplamente adotado por browsers).
    """

    MAX_LENGTH = 2083

    def __init__(self, url: str) -> None:
        self.url = url
        self.length = len(url)
        super().__init__(
            f"URL excede o comprimento máximo de {self.MAX_LENGTH} caracteres "
            f"(recebido: {self.length})."
        )


class UnsupportedSchemeError(LinkAnalysisDomainError):
    """
    Levantada quando o scheme da URL não é suportado pela análise.
    O domínio suporta apenas 'http' e 'https'.

    Exemplos de schemes não suportados: ftp, mailto, javascript.
    """

    SUPPORTED_SCHEMES = ("http", "https")

    def __init__(self, scheme: str) -> None:
        self.scheme = scheme
        super().__init__(
            f"Scheme '{scheme}' não suportado. "
            f"Schemes aceitos: {', '.join(self.SUPPORTED_SCHEMES)}."
        )
