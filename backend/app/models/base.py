from sqlmodel import SQLModel, Field


class BaseEntity(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)
