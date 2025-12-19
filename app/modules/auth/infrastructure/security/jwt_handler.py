from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt

from app.core.config import settings
from app.core.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException


class JWTHandler:
    """
    Classe responsável por criação e validação de tokens JWT.
    
    Tokens contêm:
    - sub: ID do usuário
    - type: tipo do token (access ou refresh)
    - exp: timestamp de expiração
    - iat: timestamp de criação
    """
    
    def __init__(self):
        self._secret_key = settings.SECRET_KEY
        self._algorithm = settings.ALGORITHM
        self._access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_access_token(
        self,
        user_id: str,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Cria token de acesso JWT.
        
        Args:
            user_id: ID do usuário
            additional_claims: Claims adicionais (opcional)
            
        Returns:
            str: Token JWT
        """
        
        expire = datetime.utcnow() + timedelta(minutes=self._access_token_expire)
        
        claims = {
            "sub": user_id,
            "type": TOKEN_TYPE_ACCESS,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        if additional_claims:
            claims.update(additional_claims)
        
        return jwt.encode(claims, self._secret_key, algorithm=self._algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """
        Cria token de refresh JWT.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            str: Token JWT
        """
        
        expire = datetime.utcnow() + timedelta(days=self._refresh_token_expire)
        
        claims = {
            "sub": user_id,
            "type": TOKEN_TYPE_REFRESH,
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        return jwt.encode(claims, self._secret_key, algorithm=self._algorithm)
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decodifica e valida token JWT.
        
        Args:
            token: Token JWT
            
        Returns:
            Dict[str, Any]: Claims do token
            
        Raises:
            InvalidTokenException: Token inválido ou expirado
        """
        
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm]
            )
            return payload
        except JWTError as e:
            raise InvalidTokenException(f"Token inválido: {str(e)}")
    
    def get_user_id_from_token(self, token: str) -> str:
        """
        Extrai ID do usuário do token.
        
        Args:
            token: Token JWT
            
        Returns:
            str: ID do usuário
            
        Raises:
            InvalidTokenException: Token inválido
        """
        
        payload = self.decode_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise InvalidTokenException("Token não contém ID do usuário")
        
        return user_id
    
    def verify_token_type(self, token: str, expected_type: str) -> bool:
        """
        Verifica se token é do tipo esperado.
        
        Args:
            token: Token JWT
            expected_type: Tipo esperado (access ou refresh)
            
        Returns:
            bool: True se tipo corresponde
        """
        
        try:
            payload = self.decode_token(token)
            token_type = payload.get("type")
            return token_type == expected_type
        except InvalidTokenException:
            return False
    
    def get_token_expiration(self, token: str) -> datetime:
        """
        Retorna timestamp de expiração do token.
        
        Args:
            token: Token JWT
            
        Returns:
            datetime: Data/hora de expiração
            
        Raises:
            InvalidTokenException: Token inválido
        """
        
        payload = self.decode_token(token)
        exp = payload.get("exp")
        
        if not exp:
            raise InvalidTokenException("Token não contém expiração")
        
        return datetime.fromtimestamp(exp)
    
    def is_token_expired(self, token: str) -> bool:
        """
        Verifica se token está expirado.
        
        Args:
            token: Token JWT
            
        Returns:
            bool: True se expirado
        """
        
        try:
            expiration = self.get_token_expiration(token)
            return datetime.utcnow() > expiration
        except InvalidTokenException:
            return True
