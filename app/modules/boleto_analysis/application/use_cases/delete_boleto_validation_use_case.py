from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    DeleteBoletoValidationInputDTO,
)

from app.modules.boleto_analysis.application.exceptions.application_exceptions import (
    BoletoNotFoundError,
    map_domain_exception,
)

from app.modules.boleto_analysis.domain.exceptions.exceptions import (
    BoletoDomainError,
)

from app.modules.boleto_analysis.domain.repositories.boleto_validation_repository import (
    BoletoValidationRepository,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import (
    BoletoCode,
)


class DeleteBoletoValidationUseCase:
    """
    Caso de uso: remover validação de boleto do usuário.
    """

    def __init__(
        self,
        repository: BoletoValidationRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        input_dto: DeleteBoletoValidationInputDTO,
    ) -> None:

        # ----------------------------------------------------------
        # Normaliza e valida código
        # ----------------------------------------------------------

        try:
            code = BoletoCode.create(input_dto.code)

        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        # ----------------------------------------------------------
        # Verifica existência
        # ----------------------------------------------------------

        exists = self._repository.exists_by_code_and_user_id(
            code=code,
            user_id=input_dto.user_id,
        )

        if not exists:
            raise BoletoNotFoundError(
                f"Nenhuma validação encontrada para o código: '{input_dto.code}'"
            )

        # ----------------------------------------------------------
        # Remove
        # ----------------------------------------------------------

        try:
            self._repository.delete_by_code_and_user_id(
                code=code,
                user_id=input_dto.user_id,
            )

        except BoletoDomainError as exc:
            raise map_domain_exception(exc)
