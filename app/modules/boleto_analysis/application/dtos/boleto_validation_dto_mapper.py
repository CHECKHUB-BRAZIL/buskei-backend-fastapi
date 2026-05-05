from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    BoletoValidationSummaryDTO,
    ValidateBoletoOutputDTO,
)
from app.modules.boleto_analysis.domain.entities.boleto_validation_entity import (
    BoletoValidationEntity,
)


class BoletoValidationDTOMapper:
    """
    Converte entidades de domínio para DTOs de saída da camada de aplicação.

    Centraliza o mapeamento em um único lugar, mantendo os use cases limpos
    e evitando duplicação de lógica de conversão.
    """

    @staticmethod
    def to_output_dto(entity: BoletoValidationEntity) -> ValidateBoletoOutputDTO:
        return ValidateBoletoOutputDTO(
            code=str(entity.code),
            original_code=entity.code.original,
            boleto_type=entity.code.boleto_type.value,
            amount=entity.amount.value,
            amount_formatted=str(entity.amount),
            due_date=entity.due_date.value,
            due_date_formatted=str(entity.due_date),
            is_expired=entity.due_date.is_expired,
            days_overdue=entity.due_date.days_overdue,
            days_until_due=entity.due_date.days_until_due,
            status=entity.status,
            reasons=list(entity.reasons),
            created_at=entity.created_at,
        )

    @staticmethod
    def to_summary_dto(entity: BoletoValidationEntity) -> BoletoValidationSummaryDTO:
        return BoletoValidationSummaryDTO(
            code=str(entity.code),
            boleto_type=entity.code.boleto_type.value,
            amount_formatted=str(entity.amount),
            due_date_formatted=str(entity.due_date),
            status=entity.status,
            created_at=entity.created_at,
        )
