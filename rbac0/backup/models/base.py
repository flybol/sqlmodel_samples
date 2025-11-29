from datetime import datetime
from sqlmodel import SQLModel,Field

class IDMixin(SQLModel):
    """ 默认的ID字段 """
    id: int|None = Field(default=None, primary_key=True)

class SoftDeleteMixin(SQLModel):
    """ 默认的软删除字段 """
    is_deleted: bool = Field(
        default=False,
        nullable=False,
        index=True,
        description="是否已删除（软删除标记）",
    )
    deleted_at: datetime = Field(
        default_factory=datetime.now,
        nullable=True,
        description="删除时间（UTC）",
    )

class TimestampMixin(SQLModel):
    """ 默认的创建时间、更新时间字段 """
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="创建时间（UTC）",
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        description="最后更新时间（UTC）",
    )

class ActiveMixin(SQLModel):
    """ 默认的状态字段 """
    is_active: bool = Field(
        default=False,
        nullable=False,
        description="是否启用",
    )

class ORMBase(SoftDeleteMixin, TimestampMixin):
    """ 所有 ORM 表的基础类，单独建表 """
class ORMBaseWithActive(SoftDeleteMixin, TimestampMixin, ActiveMixin):
    """ 所有 ORM 表的基础类，单独建表 """