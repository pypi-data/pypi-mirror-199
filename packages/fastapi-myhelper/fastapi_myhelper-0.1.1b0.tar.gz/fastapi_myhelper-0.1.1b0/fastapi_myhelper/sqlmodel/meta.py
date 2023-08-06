from fastapi_myhelper.pydantic.meta import ConfigMeta
from sqlmodel.main import SQLModelMetaclass


class SQLModelMetaConfig(ConfigMeta, SQLModelMetaclass):
    pass

from sqlmodel import SQLModel, Field

class A(SQLModel, metaclass=SQLModelMetaConfig):
    id: int = Field(primary_key=True)

class B(A, table=True):
    pass


class C(A, table=True):
    id_: int = Field(primary_key=True)
    class Config:
        include = []

print(C.__table__)
