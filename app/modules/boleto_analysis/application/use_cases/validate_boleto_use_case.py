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
from app.modules.boleto_analysis.domain.exceptions.exceptions import BoletoDomainError
from app.modules.boleto_analysis.domain.repositories.boleto_validation_repository import (
    BoletoValidationRepository,
)
from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import BoletoCode


class ValidateBoletoUseCase:
    """
    Caso de uso: validar a autenticidade e situação de um boleto.

    Fluxo:
        1. Constrói o BoletoCode (valida estrutura e dígito verificador).
        2. Delega a análise de domínio para BoletoValidationEntity.validate().
        3. Persiste o resultado via repositório.
        4. Retorna DTO de saída completo para a apresentação.

    Não conhece HTTP, banco de dados ou framework.
    """

    def __init__(self, repository: BoletoValidationRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: ValidateBoletoInputDTO) -> ValidateBoletoOutputDTO:
        try:
            code = BoletoCode.create(input_dto.code)
        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        try:
            entity: BoletoValidationEntity = BoletoValidationEntity.validate(code)
            self._repository.save(entity)
        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        return BoletoValidationDTOMapper.to_output_dto(entity)
