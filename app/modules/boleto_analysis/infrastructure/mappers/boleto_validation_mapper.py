from decimal import Decimal

from app.modules.boleto_analysis.domain.entities.boleto_validation_entity import (
    BoletoValidationEntity,
)
from app.modules.boleto_analysis.domain.value_objects.boleto_amount_vo import BoletoAmount
from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import BoletoCode
from app.modules.boleto_analysis.domain.value_objects.due_date_vo import DueDate
from app.modules.boleto_analysis.infrastructure.models.boleto_validation_model import (
    BoletoValidationModel,
)


class BoletoValidationMapper:
    """
    Converte entre a entidade de domínio (BoletoValidationEntity)
    e o modelo ORM (BoletoValidationModel).

    Responsabilidades:
    - Serializar Value Objects para tipos primitivos armazenáveis.
    - Reconstruir Value Objects ao ler do banco, sem chamar lógicas de validação
      (os dados já foram validados na entrada — apenas reconstroem o estado).

    O domínio nunca importa o modelo ORM.
    O ORM nunca conhece as regras de negócio.
    """

    @staticmethod
    def to_model(entity: BoletoValidationEntity) -> BoletoValidationModel:
        """Entidade de domínio → modelo ORM."""
        return BoletoValidationModel(
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
    def to_entity(model: BoletoValidationModel) -> BoletoValidationEntity:
        """
        Modelo ORM → entidade de domínio.

        Reconstrói os Value Objects diretamente a partir dos dados persistidos,
        sem reexecutar validações de dígito verificador (já foram feitas na entrada).
        """
        # Reconstrói BoletoCode via fábrica — dados já normalizados no banco
        code = BoletoCode.create(model.code)

        # Reconstrói BoletoAmount
        amount = BoletoAmount(value=Decimal(str(model.amount)))

        # Reconstrói DueDate
        if model.due_date_factor:
            due_date = DueDate.from_factor(model.due_date_factor)
        else:
            due_date = DueDate.no_due_date()

        return BoletoValidationEntity(
            code=code,
            amount=amount,
            due_date=due_date,
            status=model.status,
            reasons=list(model.reasons),
            created_at=model.created_at,
        )
