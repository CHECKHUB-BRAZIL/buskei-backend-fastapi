from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    GetBoletoValidationInputDTO,
    ValidateBoletoOutputDTO,
)
from app.modules.boleto_analysis.application.dtos.boleto_validation_dto_mapper import (
    BoletoValidationDTOMapper,
)
from app.modules.boleto_analysis.application.exceptions.application_exceptions import (
    BoletoNotFoundError,
    map_domain_exception,
)
from app.modules.boleto_analysis.domain.exceptions.exceptions import (
    BoletoDomainError,
    BoletoValidationNotFoundError,
)
from app.modules.boleto_analysis.domain.repositories.boleto_validation_repository import (
    BoletoValidationRepository,
)
from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import BoletoCode


class GetBoletoValidationUseCase:
    """
    Caso de uso: recuperar a validação já realizada de um boleto pelo código.

    Fluxo:
        1. Constrói BoletoCode para normalizar e validar a entrada.
        2. Consulta o repositório pelo código normalizado (44 dígitos).
        3. Levanta BoletoNotFoundError se não existir.
        4. Retorna DTO de saída completo.
    """

    def __init__(self, repository: BoletoValidationRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: GetBoletoValidationInputDTO) -> ValidateBoletoOutputDTO:
        try:
            code = BoletoCode.create(input_dto.code)
        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        entity = self._repository.find_by_code(code)

        if entity is None:
            raise BoletoNotFoundError(
                f"Nenhuma validação encontrada para o código: '{input_dto.code}'"
            )

        return BoletoValidationDTOMapper.to_output_dto(entity)
