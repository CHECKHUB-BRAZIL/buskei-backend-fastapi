from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QRCodeData:
    # valor original lido
    raw_value: str

    # tipo detectado
    qrcode_type: str

    # validação estrutural
    is_valid: bool

    # antifraude
    risk_score: int
    status: str

    # explicabilidade
    reason: Optional[str] = None

    # PIX
    pix_key: Optional[str] = None
    merchant_name: Optional[str] = None
    amount: Optional[float] = None

    # links
    detected_url: Optional[str] = None

    # segurança
    is_suspicious_url: bool = False
    has_unknown_domain: bool = False
