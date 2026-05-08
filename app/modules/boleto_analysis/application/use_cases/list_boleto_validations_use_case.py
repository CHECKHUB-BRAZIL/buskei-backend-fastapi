from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    BoletoValidationSummaryDTO,
    ListBoletoValidationsInputDTO,
    ListBoletoValidationsOutputDTO,
)

from app.modules.boleto_analysis.application.dtos.boleto_validation_dto_mapper import (
    BoletoValidationDTOMapper,
)

from app.modules.boleto_analysis.domain.repositories.boleto_validation_repository import (
    BoletoValidationRepository,
)


class ListBoletoValidationsUseCase:
    """
    Caso de uso: listar validações do usuário.
    """

    def __init__(
        self,
        repository: BoletoValidationRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        input_dto: ListBoletoValidationsInputDTO,
    ) -> ListBoletoValidationsOutputDTO:

        entities = self._repository.find_all_by_user_id(
            user_id=input_dto.user_id,
        )

        items: list[BoletoValidationSummaryDTO] = [
            BoletoValidationDTOMapper.to_summary_dto(entity)
            for entity in entities
        ]

        return ListBoletoValidationsOutputDTO(
            total=len(items),
            items=items,
        )
