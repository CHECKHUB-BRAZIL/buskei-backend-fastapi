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
)

from app.modules.boleto_analysis.domain.repositories.boleto_validation_repository import (
    BoletoValidationRepository,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import (
    BoletoCode,
)


class GetBoletoValidationUseCase:
    """
    Caso de uso: buscar validação de boleto do usuário.
    """

    def __init__(
        self,
        repository: BoletoValidationRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        input_dto: GetBoletoValidationInputDTO,
    ) -> ValidateBoletoOutputDTO:

        # ----------------------------------------------------------
        # Normaliza e valida o código
        # ----------------------------------------------------------

        try:
            code = BoletoCode.create(input_dto.code)

        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        # ----------------------------------------------------------
        # Busca no repositório
        # ----------------------------------------------------------

        entity = self._repository.find_by_code_and_user_id(
            code=code,
            user_id=input_dto.user_id,
        )

        # ----------------------------------------------------------
        # Não encontrado
        # ----------------------------------------------------------

        if entity is None:
            raise BoletoNotFoundError(
                f"Nenhuma validação encontrada para o código: '{input_dto.code}'"
            )

        # ----------------------------------------------------------
        # Retorno
        # ----------------------------------------------------------

        return BoletoValidationDTOMapper.to_output_dto(entity)
