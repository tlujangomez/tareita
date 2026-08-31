from pydantic import BaseModel, Field


class AutorCrear(BaseModel):
    nombre: str = Field(min_length=1)
    pais: str | None = None
    nacimiento: int | None = Field(default=None, ge=0)


class AutorActualizar(BaseModel):
    nombre: str = Field(min_length=1)
    pais: str | None = None
    nacimiento: int | None = Field(default=None, ge=0)