from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PixPayloadData:
    pix_key: Optional[str]
    merchant_name: Optional[str]
    city: Optional[str]
    amount: Optional[float]
    txid: Optional[str]
    is_valid_crc: bool
