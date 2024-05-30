from pydantic import BaseModel, Field
from typing import Optional

class Imovel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    bairro: str
    areaM2: int
    suites: int
    dormitorios: int
    banheiros: int
    vagas: int
    preco: str = Field(alias=" preco ")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True  # Permite campos adicionais

        @classmethod
        def alias_generator(cls, string: str) -> str:
            if string == "_id":
                return "id"
            return string