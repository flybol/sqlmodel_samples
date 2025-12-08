from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import func, Column, DateTime


class IDMixin(SQLModel, table=False):
    """ " 主键Id"""

    id: int | None = Field(default=None, primary_key=True, description="主键Id")


class AuditMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="创建时间",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="更新时间",
    )

    created_by: int = Field(nullable=False, description="创建人Id")
    updated_by: Optional[int] = Field(
        default=None, nullable=True, description="更新人Id"
    )


class SoftDeleteMixin(SQLModel, table=False):
    """软删除"""

    is_deleted: bool = Field(default=False, description="是否删除")
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="删除时间",
    )
    deleted_by: Optional[int] = Field(
        default=None, nullable=True, description="删除人Id"
    )


class ORMBase(IDMixin, table=False):
    pass
