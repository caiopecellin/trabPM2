from pydantic import BaseModel, Field
from typing import Optional

class Imovel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    bairro: str
    areaM2: int
    suites: int
    dormitorios: int
    banheiros: int
    vagas: int
    preco: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
