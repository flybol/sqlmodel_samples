from sqlmodel.ext.asyncio.session import AsyncSession
from ..schemas.user_schema import UserCreate
from ..models.user_model import User
from ..core import security
from ..core.uow import get_uow_factory, UnitOfWorkFactory


class UserService:
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    async def create_user(self, user_in: UserCreate):
        """创建新用户
        :param session: 数据库会话
        :param user_in: 新用户数据
        :return: 新用户数据
        """
        hashed_password = security.get_password_hash(user_in.password)
        # 把 password 从 dict 排除掉，再塞入 hashed_password
        data = user_in.model_dump(exclude={"password"})
        data["hashed_password"] = hashed_password

        async with self.uow_factory() as uow:
            db_user = User.model_validate(data)
            if uow.session:
                uow.session.add(db_user)
                await uow.session.refresh(db_user)
            return db_user


async def get_user_service(session: AsyncSession) -> UserService:
    return UserService(uow_factory=get_uow_factory(session))
