import re
from dataclasses import dataclass
from enum import Enum

from app.modules.boleto_analysis.domain.exceptions.exceptions import InvalidBoletoCodeError, UnsupportedBoletoTypeError


class BoletoType(str, Enum):
    COBRANCA = "cobranca"   # bancos — código de barras começa com banco (3 dígitos)
    CONVENIO = "convenio"   # concessionárias/governo — começa com 8


@dataclass(frozen=True)
class BoletoCode:
    """
    Value Object que representa o código de um boleto bancário.

    Aceita dois formatos:
    - Código de barras: 44 dígitos
    - Linha digitável:  47 dígitos (cobrança) ou 48 dígitos (convênio)

    Responsabilidades:
    - Normalizar (remover espaços, pontos, hífens)
    - Identificar o tipo (cobrança ou convênio)
    - Validar tamanho e caracteres
    - Verificar dígito verificador (módulo 10 e módulo 11)
    """

    value: str  # sempre armazena o código de barras normalizado (44 dígitos)
    boleto_type: BoletoType
    original: str  # entrada original do usuário

    def __post_init__(self) -> None:
        # Validação já foi feita pela fábrica — nada extra aqui
        pass

    def __str__(self) -> str:
        return self.value

    # ------------------------------------------------------------------
    # Fábrica principal
    # ------------------------------------------------------------------

    @classmethod
    def create(cls, raw: str) -> "BoletoCode":
        """
        Normaliza, identifica o formato e valida o código.

        Raises:
            ValueError: se o código for inválido.
        """
        
        original = raw
        normalized = re.sub(r"[\s.\-]", "", raw)

        if not normalized.isdigit():
            raise InvalidBoletoCodeError(raw, "Código deve conter apenas dígitos.")

        length = len(normalized)

        if length == 44:
            barcode = normalized
        elif length in (47, 48):
            barcode = cls._linha_digitavel_to_barcode(normalized)
        else:
            raise InvalidBoletoCodeError(
                raw,
                f"Tamanho inválido: {length} dígitos. Esperado 44 (código de barras) "
                "ou 47/48 (linha digitável).",
            )

        # Identifica tipo
        if barcode[0] == "8":
            boleto_type = BoletoType.CONVENIO
        elif barcode[:1].isdigit() and int(barcode[:3]) > 0:
            boleto_type = BoletoType.COBRANCA
        else:
            raise UnsupportedBoletoTypeError(barcode[:1])

        # Valida dígito verificador geral
        if not cls._validate_check_digit(barcode, boleto_type):
            raise InvalidBoletoCodeError(raw, "Dígito verificador inválido.")

        return cls(value=barcode, boleto_type=boleto_type, original=original)

    # ------------------------------------------------------------------
    # Propriedades de domínio
    # ------------------------------------------------------------------

    @property
    def bank_code(self) -> str | None:
        """Código do banco (3 primeiros dígitos). Apenas para cobrança."""
        if self.boleto_type == BoletoType.COBRANCA:
            return self.value[:3]
        return None

    @property
    def currency_code(self) -> str:
        """Código da moeda (posição 4). '9' = Real."""
        return self.value[3]

    @property
    def raw_amount(self) -> str:
        """
        Valor bruto extraído do código de barras (10 dígitos, posições 10-19).
        Pode ser '0000000000' para boletos sem valor fixo.
        """
        if self.boleto_type == BoletoType.COBRANCA:
            return self.value[9:19]
        # Convênio: posições 5-14
        return self.value[4:14]

    @property
    def due_date_factor(self) -> str | None:
        """
        Fator de vencimento (posições 6-9) — apenas cobrança.
        '0000' indica sem vencimento.
        """
        if self.boleto_type == BoletoType.COBRANCA:
            return self.value[5:9]
        return None

    # ------------------------------------------------------------------
    # Conversão linha digitável → código de barras
    # ------------------------------------------------------------------

    @classmethod
    def _linha_digitavel_to_barcode(cls, linha: str) -> str:
        """
        Converte linha digitável (47/48 dígitos) para código de barras (44 dígitos).

        Cobrança (47 dígitos):
            Campo 1: posições  0–9   (10 dígitos, sendo o último o DV do campo)
            Campo 2: posições 10–20  (11 dígitos)
            Campo 3: posições 21–31  (11 dígitos)
            DV geral: posição 32     (1 dígito)
            Vencimento: posições 33–36 (4 dígitos)
            Valor: posições 37–46    (10 dígitos)

        Convênio (48 dígitos): layout próprio da Febraban.
        """
        if len(linha) == 47:
            # Cobrança
            bank_currency = linha[0:3]
            campo1_sem_dv = linha[0:4] + linha[5:9]     # banco+moeda + campo livre parte 1
            campo2_sem_dv = linha[10:20]                  # campo livre parte 2
            campo3_sem_dv = linha[21:31]                  # campo livre parte 3
            dv_geral      = linha[32]
            vencimento    = linha[33:37]
            valor         = linha[37:47]

            campo_livre = (
                linha[4:9]    # campo1 sem banco/moeda e sem DV
                + linha[10:20]
                + linha[21:31]
            )
            return bank_currency + linha[3] + dv_geral + vencimento + valor + campo_livre

        # Convênio (48 dígitos) — layout Febraban segmento 8
        # Produto(1) + Segmento(1) + RealValorOuRef(1) + DV(1) + Valor(14) + livre(25) + CNPJ/CPF
        campo1 = linha[0:9]
        campo2 = linha[10:20]
        campo3 = linha[21:31]
        dv     = linha[32]
        campo4 = linha[33:48]
        return campo1 + campo2 + campo3 + dv + campo4

    # ------------------------------------------------------------------
    # Validação de dígito verificador
    # ------------------------------------------------------------------

    @classmethod
    def _validate_check_digit(cls, barcode: str, boleto_type: BoletoType) -> bool:
        if boleto_type == BoletoType.COBRANCA:
            return cls._modulo11_cobranca(barcode)
        return cls._modulo10_convenio(barcode)

    @classmethod
    def _modulo11_cobranca(cls, barcode: str) -> bool:
        """
        Módulo 11 para boletos de cobrança (bancários).
        O DV geral fica na posição 4 (índice 4).
        """
        dv_esperado = int(barcode[4])
        numero = barcode[:4] + barcode[5:]  # remove o DV da sequência

        soma = 0
        peso = 2
        for digito in reversed(numero):
            soma += int(digito) * peso
            peso = 2 if peso == 9 else peso + 1

        resto = soma % 11
        if resto in (0, 1):
            dv_calculado = 1
        else:
            dv_calculado = 11 - resto

        return dv_calculado == dv_esperado

    @classmethod
    def _modulo10_convenio(cls, barcode: str) -> bool:
        """
        Módulo 10 para boletos de convênio (concessionárias/governo).
        O DV geral fica na posição 3 (índice 3).
        """
        dv_esperado = int(barcode[3])
        numero = barcode[:3] + barcode[4:]

        soma = 0
        multiplicador = 2
        for digito in reversed(numero):
            resultado = int(digito) * multiplicador
            soma += resultado // 10 + resultado % 10
            multiplicador = 1 if multiplicador == 2 else 2

        dv_calculado = (10 - (soma % 10)) % 10
        return dv_calculado == dv_esperado
