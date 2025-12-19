class LogoutUseCase:
    """
    Caso de uso: Logout do usuário.
    
    No contexto de JWT stateless, o logout é geralmente tratado
    no lado do cliente (removendo o token).
    
    Este use case pode ser expandido para:
    - Blacklist de tokens
    - Invalidação de refresh tokens
    - Logs de auditoria
    """
    
    def __init__(self):
        pass
    
    async def execute(self, user_id: str) -> bool:
        """
        Executa o caso de uso de logout.
        
        Args:
            user_id: ID do usuário fazendo logout
            
        Returns:
            bool: True se logout foi bem-sucedido
        """
        
        # TODO: Implementar lógica de blacklist/invalidação
        # Por enquanto, apenas retorna True
        # O cliente deve remover o token do storage
        
        return True
