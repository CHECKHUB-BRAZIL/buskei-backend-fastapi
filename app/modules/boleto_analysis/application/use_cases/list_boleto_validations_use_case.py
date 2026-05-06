from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    BoletoValidationSummaryDTO,
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
    Caso de uso: listar todas as validações de boletos já realizadas.

    Retorna uma versão resumida (SummaryDTO) para economizar payload,
    adequada para listagens e dashboards.

    Fluxo:
        1. Busca todas as entidades no repositório (ordenadas por data desc).
        2. Converte cada uma para SummaryDTO.
        3. Retorna envelope com total e itens.
    """

    def __init__(self, repository: BoletoValidationRepository) -> None:
        self._repository = repository

    def execute(self) -> ListBoletoValidationsOutputDTO:
        entities = self._repository.find_all()

        items: list[BoletoValidationSummaryDTO] = [
            BoletoValidationDTOMapper.to_summary_dto(entity)
            for entity in entities
        ]

        return ListBoletoValidationsOutputDTO(
            total=len(items),
            items=items,
        )
