import re
from dataclasses import dataclass
from enum import Enum

from app.modules.boleto_analysis.domain.exceptions.exceptions import (
    InvalidBoletoCodeError,
)


class BoletoType(str, Enum):
    COBRANCA = "cobranca"
    CONVENIO = "convenio"


@dataclass(frozen=True)
class BoletoCode:
    """
    Value Object do código de boleto.

    Responsabilidades:
    - Normalizar entrada
    - Identificar tipo
    - Converter linha digitável em código de barras
    - Validar estrutura e DV
    - Expor flag de integridade (is_real)
    """

    value: str
    boleto_type: BoletoType
    original: str
    is_real: bool

    def __str__(self) -> str:
        return self.value

    # ==========================================================
    # FACTORY
    # ==========================================================

    @classmethod
    def create(cls, raw: str) -> "BoletoCode":

        original = raw
        normalized = re.sub(r"[\s.\-]", "", raw)

        if not normalized.isdigit():
            raise InvalidBoletoCodeError(
                raw,
                "Código deve conter apenas números.",
            )

        length = len(normalized)

        # ------------------------------------------------------
        # 44 → código de barras
        # ------------------------------------------------------

        if length == 44:
            barcode = normalized

        # ------------------------------------------------------
        # 47/48 → linha digitável
        # ------------------------------------------------------

        elif length in (47, 48):
            barcode = cls._linha_digitavel_to_barcode(normalized)

        else:
            raise InvalidBoletoCodeError(
                raw,
                f"Tamanho inválido: {length}. Esperado 44, 47 ou 48.",
            )

        # ------------------------------------------------------
        # Tipo de boleto
        # ------------------------------------------------------

        boleto_type = (
            BoletoType.CONVENIO
            if barcode.startswith("8")
            else BoletoType.COBRANCA
        )

        # ------------------------------------------------------
        # DV (apenas sinalização antifraude)
        # ------------------------------------------------------

        is_real = cls._validate_check_digit(
            barcode,
            boleto_type,
        )

        return cls(
            value=barcode,
            boleto_type=boleto_type,
            original=original,
            is_real=is_real,
        )

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def bank_code(self) -> str | None:
        if self.boleto_type == BoletoType.COBRANCA:
            return self.value[:3]
        return None

    @property
    def currency_code(self) -> str:
        return self.value[3]

    @property
    def raw_amount(self) -> str:
        if self.boleto_type == BoletoType.COBRANCA:
            return self.value[9:19]
        return self.value[4:14]

    @property
    def due_date_factor(self) -> str | None:
        if self.boleto_type == BoletoType.COBRANCA:
            return self.value[5:9]
        return None

    # ==========================================================
    # LINHA DIGITÁVEL → BARCODE
    # ==========================================================

    @classmethod
    def _linha_digitavel_to_barcode(cls, linha: str) -> str:

        if len(linha) == 47:

            campo1 = linha[0:9]
            campo2 = linha[10:20]
            campo3 = linha[21:31]

            dv_geral = linha[32]
            fator = linha[33:37]
            valor = linha[37:47]

            campo_livre = campo1[4:] + campo2 + campo3

            return campo1[0:4] + dv_geral + fator + valor + campo_livre

        # CONVÊNIO
        campo1 = linha[0:11]
        campo2 = linha[12:23]
        campo3 = linha[24:35]
        campo4 = linha[36:47]

        return (
            campo1[:-1]
            + campo2[:-1]
            + campo3[:-1]
            + campo4[:-1]
        )

    # ==========================================================
    # DV VALIDATION
    # ==========================================================

    @classmethod
    def _validate_check_digit(
        cls,
        barcode: str,
        boleto_type: BoletoType,
    ) -> bool:

        return (
            cls._modulo11_cobranca(barcode)
            if boleto_type == BoletoType.COBRANCA
            else cls._modulo10_convenio(barcode)
        )

    # ==========================================================
    # MODULO 11 (COBRANÇA)
    # ==========================================================

    @classmethod
    def _modulo11_cobranca(cls, barcode: str) -> bool:

        dv_esperado = int(barcode[4])
        numero = barcode[:4] + barcode[5:]

        peso = 2
        soma = 0

        for digito in reversed(numero):

            soma += int(digito) * peso
            peso += 1

            if peso > 9:
                peso = 2

        resto = soma % 11
        dv_calculado = 11 - resto

        if dv_calculado in (0, 10, 11):
            dv_calculado = 1

        return dv_calculado == dv_esperado

    # ==========================================================
    # MODULO 10 (CONVÊNIO) — corrigido
    # ==========================================================

    @classmethod
    def _modulo10_convenio(cls, barcode: str) -> bool:

        dv_esperado = int(barcode[3])
        numero = barcode[:3] + barcode[4:]

        soma = 0
        peso = 2

        for digito in reversed(numero):

            multiplicacao = int(digito) * peso

            if multiplicacao >= 10:
                multiplicacao = (multiplicacao // 10) + (multiplicacao % 10)

            soma += multiplicacao

            # FIX IMPORTANTE: alternância correta 2 → 1 → 2 → 1
            peso = 1 if peso == 2 else 2

        dv_calculado = (10 - (soma % 10)) % 10

        return dv_calculado == dv_esperado
