from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    DeleteBoletoValidationInputDTO,
)
from app.modules.boleto_analysis.application.exceptions.application_exceptions import (
    BoletoNotFoundError,
    map_domain_exception,
)
from app.modules.boleto_analysis.domain.exceptions.exceptions import BoletoDomainError
from app.modules.boleto_analysis.domain.repositories.boleto_validation_repository import (
    BoletoValidationRepository,
)
from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import BoletoCode


class DeleteBoletoValidationUseCase:
    """
    Caso de uso: remover a validação de um boleto pelo seu código.

    Fluxo:
        1. Constrói BoletoCode para normalizar a entrada.
        2. Verifica existência antes de tentar deletar.
        3. Delega a exclusão ao repositório.
    """

    def __init__(self, repository: BoletoValidationRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: DeleteBoletoValidationInputDTO) -> None:
        try:
            code = BoletoCode.create(input_dto.code)
        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        exists = self._repository.exists(code)
        if not exists:
            raise BoletoNotFoundError(
                f"Nenhuma validação encontrada para o código: '{input_dto.code}'"
            )

        try:
            self._repository.delete_by_code(code)
        except BoletoDomainError as exc:
            raise map_domain_exception(exc)
