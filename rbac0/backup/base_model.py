
from sqlmodel import SQLModel,Field
from datetime import datetime

class IDMixin(SQLModel):
    """统一主键字段"""
    id: int|None = Field(default=None, primary_key=True, index=True)
    
class TimestampMixin(SQLModel):
    """统一时间戳字段"""
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="创建时间（UTC）",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="最后更新时间（UTC）",
    )

class SoftDeleteMixin(SQLModel):
    """软删除标记（可选）"""
    is_deleted: bool = Field(
        default=False,
        nullable=False,
        description="是否已删除（软删除标记）",
    )

class RBACBase(SQLModel):
    """所有 RBAC 相关表的基类（方便将来统一配置）"""
    # 这里先留空，将来可以加：
    # - 多租户字段 tenant_id
    # - 审计字段 created_by / updated_by 等
    pass

class ORMBase(SQLModel):
    """所有 RBAC 相关表的基类（方便将来统一配置）"""
    # 这里先留空，将来可以加：
    # - 多租户字段 tenant_id
    # - 审计字段 created_by / updated_by 等
    pass