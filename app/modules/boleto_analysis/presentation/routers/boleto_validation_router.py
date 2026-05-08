from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.presentation.http.dependencies.auth_deps import (
    get_current_user,
)

from app.shared.infrastructure.database.session import get_db

from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    DeleteBoletoValidationInputDTO,
    GetBoletoValidationInputDTO,
    ValidateBoletoInputDTO,
)

from app.modules.boleto_analysis.application.use_cases.validate_boleto_use_case import (
    ValidateBoletoUseCase,
)

from app.modules.boleto_analysis.application.use_cases.list_boleto_validations_use_case import (
    ListBoletoValidationsUseCase,
)

from app.modules.boleto_analysis.application.use_cases.get_boleto_validation_use_case import (
    GetBoletoValidationUseCase,
)

from app.modules.boleto_analysis.application.use_cases.delete_boleto_validation_use_case import (
    DeleteBoletoValidationUseCase,
)

from app.modules.boleto_analysis.infrastructure.repositories import (
    SQLAlchemyBoletoValidationRepository,
)

from app.modules.boleto_analysis.presentation.schemas.boleto_validation_schema import (
    BoletoValidationListResponse,
    BoletoValidationResponse,
    BoletoValidationSummaryResponse,
    DeleteBoletoValidationResponse,
    ValidateBoletoRequest,
)

router = APIRouter(
    prefix="/boletos",
    tags=["Boleto Validation"],
)


# ---------------------------------------------------------------------------
# POST /boletos/validate
# ---------------------------------------------------------------------------

@router.post(
    "/validate",
    response_model=BoletoValidationResponse,
    status_code=status.HTTP_201_CREATED,
)
def validate_boleto(
    body: ValidateBoletoRequest,
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user),
):
    repo = SQLAlchemyBoletoValidationRepository(db)
    use_case = ValidateBoletoUseCase(repo)

    user_id = str(current_user.id.value)

    output = use_case.execute(
        ValidateBoletoInputDTO(
            code=body.code,
            user_id=user_id,
        )
    )

    return BoletoValidationResponse(**output.__dict__)


# ---------------------------------------------------------------------------
# GET /boletos
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=BoletoValidationListResponse,
    status_code=status.HTTP_200_OK,
)
def list_boleto_validations(
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user),
):
    repo = SQLAlchemyBoletoValidationRepository(db)
    use_case = ListBoletoValidationsUseCase(repo)

    user_id = str(current_user.id.value)

    output = use_case.execute(user_id=user_id)

    items = [
        BoletoValidationSummaryResponse(
            code=item.code,
            boleto_type=item.boleto_type,
            amount_formatted=item.amount_formatted,
            due_date_formatted=item.due_date_formatted,
            status=item.status,
            created_at=item.created_at,
        )
        for item in output.items
    ]

    return BoletoValidationListResponse(
        total=output.total,
        items=items,
    )


# ---------------------------------------------------------------------------
# GET /boletos/validation
# ---------------------------------------------------------------------------

@router.get(
    "/validation",
    response_model=BoletoValidationResponse,
    status_code=status.HTTP_200_OK,
)
def get_boleto_validation(
    code: str = Query(
        ...,
        min_length=44,
        max_length=48,
    ),
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user),
):
    repo = SQLAlchemyBoletoValidationRepository(db)
    use_case = GetBoletoValidationUseCase(repo)

    user_id = str(current_user.id.value)

    output = use_case.execute(
        GetBoletoValidationInputDTO(
            code=code,
            user_id=user_id,
        )
    )

    return BoletoValidationResponse(**output.__dict__)


# ---------------------------------------------------------------------------
# DELETE /boletos/validation
# ---------------------------------------------------------------------------

@router.delete(
    "/validation",
    response_model=DeleteBoletoValidationResponse,
    status_code=status.HTTP_200_OK,
)
def delete_boleto_validation(
    code: str = Query(
        ...,
        min_length=44,
        max_length=48,
    ),
    db: Session = Depends(get_db),
    current_user: UserEntity = Depends(get_current_user),
):
    repo = SQLAlchemyBoletoValidationRepository(db)
    use_case = DeleteBoletoValidationUseCase(repo)

    user_id = str(current_user.id.value)

    use_case.execute(
        DeleteBoletoValidationInputDTO(
            code=code,
            user_id=user_id,
        )
    )

    return DeleteBoletoValidationResponse(
        message="Validação removida com sucesso.",
        code=code,
    )
