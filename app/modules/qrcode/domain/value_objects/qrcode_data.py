from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QRCodeData:
    # valor original
    raw_value: str

    # tipo
    qrcode_type: str

    # validade estrutural
    is_valid: bool

    # score antifraude
    risk_score: int

    # safe | attention | suspicious | fraud_suspect
    status: str

    # explicabilidade
    reasons: list[str]

    positives: list[str]

    # PIX
    pix_key: Optional[str] = None

    merchant_name: Optional[str] = None

    amount: Optional[float] = None

    # URL
    detected_url: Optional[str] = None

    # segurança
    is_suspicious_url: bool = False

    has_unknown_domain: bool = False
