from decimal import Decimal

from app.modules.boleto_analysis.domain.entities.boleto_validation_entity import (
    BoletoValidationEntity,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_amount_vo import (
    BoletoAmount,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import (
    BoletoCode,
)

from app.modules.boleto_analysis.domain.value_objects.due_date_vo import (
    DueDate,
)

from app.modules.boleto_analysis.infrastructure.models.boleto_validation_model import (
    BoletoValidationModel,
)


class BoletoValidationMapper:
    """
    Converte entre entidade de domínio e modelo ORM.
    """

    @staticmethod
    def to_model(
        entity: BoletoValidationEntity,
    ) -> BoletoValidationModel:
        """
        Entidade → ORM
        """

        return BoletoValidationModel(
            user_id=entity.user_id,
            code=str(entity.code),
            original_code=entity.code.original,
            boleto_type=entity.code.boleto_type.value,
            amount=entity.amount.value,
            due_date_factor=entity.code.due_date_factor,
            is_expired=entity.due_date.is_expired,
            days_overdue=entity.due_date.days_overdue,
            status=entity.status,
            reasons=list(entity.reasons),
            created_at=entity.created_at,
        )

    @staticmethod
    def to_entity(
        model: BoletoValidationModel,
    ) -> BoletoValidationEntity:
        """
        ORM → Entidade
        """

        # ----------------------------------------------------------
        # Reconstrói Value Objects
        # ----------------------------------------------------------

        code = BoletoCode.create(model.code)

        amount = BoletoAmount(
            value=Decimal(str(model.amount))
        )

        if model.due_date_factor:
            due_date = DueDate.from_factor(
                model.due_date_factor
            )
        else:
            due_date = DueDate.no_due_date()

        # ----------------------------------------------------------
        # Entidade
        # ----------------------------------------------------------

        return BoletoValidationEntity(
            user_id=model.user_id,
            code=code,
            amount=amount,
            due_date=due_date,
            status=model.status,
            reasons=list(model.reasons),
            created_at=model.created_at,
        )
