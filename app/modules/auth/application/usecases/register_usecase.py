import uuid

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.password_vo import Password
from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
)
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


class RegisterUseCase:
    """
    Caso de uso: Registrar novo usuário.
    
    Responsabilidades:
    - Validar dados de entrada
    - Verificar se email já existe
    - Criar hash da senha
    - Criar novo usuário
    
    NÃO gera tokens JWT - isso é responsabilidade da camada de apresentação.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
    
    async def execute(
        self,
        nome: str,
        email: str,
        senha: str,
    ) -> UserEntity:
        """
        Executa o caso de uso de registro.
        
        Args:
            nome: Nome do usuário
            email: Email do usuário
            senha: Senha em texto plano
            
        Returns:
            UserEntity: Entidade do usuário criado
            
        Raises:
            UserAlreadyExistsException: Email já cadastrado
            ValueError: Dados inválidos
        """
        
        # Valida email usando Value Object
        email_vo = Email(email)
        
        # Verifica se email já existe
        if await self._user_repository.exists_by_email(email_vo.value):
            raise UserAlreadyExistsException(email_vo.value)
        
        # Valida senha usando Value Object
        password_vo = Password(senha)
        
        # Cria hash da senha
        hashed_password = self._password_hasher.hash(password_vo.value)
        
        # Cria entidade do usuário
        user_entity = UserEntity(
            id=str(uuid.uuid4()),
            nome=nome.strip(),
            email=email_vo.value,
            is_active=True,
        )
        
        # Persiste no repositório
        created_user = await self._user_repository.create(
            user=user_entity,
            hashed_password=hashed_password,
        )
        
        return created_user
