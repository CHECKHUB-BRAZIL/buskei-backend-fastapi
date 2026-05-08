from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    ValidateBoletoInputDTO,
    ValidateBoletoOutputDTO,
)

from app.modules.boleto_analysis.application.dtos.boleto_validation_dto_mapper import (
    BoletoValidationDTOMapper,
)

from app.modules.boleto_analysis.application.exceptions.application_exceptions import (
    map_domain_exception,
)

from app.modules.boleto_analysis.domain.entities.boleto_validation_entity import (
    BoletoValidationEntity,
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


class ValidateBoletoUseCase:
    """
    Caso de uso: validar boleto.
    """

    def __init__(
        self,
        repository: BoletoValidationRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        input_dto: ValidateBoletoInputDTO,
    ) -> ValidateBoletoOutputDTO:

        # ----------------------------------------------------------
        # Cria Value Object do código
        # ----------------------------------------------------------

        try:
            code = BoletoCode.create(input_dto.code)

        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        # ----------------------------------------------------------
        # Executa validação de domínio
        # ----------------------------------------------------------

        try:
            entity: BoletoValidationEntity = (
                BoletoValidationEntity.validate(
                    code=code,
                    user_id=input_dto.user_id,
                )
            )

            self._repository.save(entity)

        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        # ----------------------------------------------------------
        # Retorno
        # ----------------------------------------------------------

        return BoletoValidationDTOMapper.to_output_dto(
            entity
        )
