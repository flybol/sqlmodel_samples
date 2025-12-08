from sqlmodel import select, or_
from app.models.user_model import User
from .base import BaseRepository, register_repository, AsyncSession


@register_repository()  # 注册名：uow.user
class UserRepository(BaseRepository[User]):
    model = User

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_identity(self, identity: str):
        """根据用户名、邮箱、手机号查询用户"""
        stmt = select(User).where(
            or_(
                User.username == identity,
                User.email == identity,
                User.phone == identity,
            )
        )
        result = await self.session.exec(stmt)
        return result.one()
