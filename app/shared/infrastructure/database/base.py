from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid


Base = declarative_base()


class BaseModel(Base):
    """
    Classe base para todos os models SQLAlchemy.
    
    Fornece campos comuns:
    - id: UUID único
    - created_at: timestamp de criação
    - updated_at: timestamp de última atualização
    """
    
    __abstract__ = True
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
