from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AnalyzeLinkInputDTO:
    url: str


@dataclass(frozen=True)
class AnalyzeLinkOutputDTO:
    url: str

    risk: str
    risk_score: int

    reasons: List[str]
    positives: List[str]
