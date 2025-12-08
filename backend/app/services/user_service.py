from app.core import security
from app.schemas.user_schema import UserCreate
from app.models.user_model import User
from app.repositories.user_repo import UserRepository
from .base import BaseService, AsyncUnitOfWork


class UserService(BaseService[AsyncUnitOfWork]):
    """用户服务类"""

    async def create_user(self, user_create: UserCreate) -> User:
        hashed_password = security.get_password_hash(user_create.password)
        data = user_create.model_dump(exclude={"password"})
        data["hashed_password"] = hashed_password

        async with self._uow_factory() as uow:
            db_user = User.model_validate(data)
            user_repo = uow.get_repo(UserRepository)
            await user_repo.add(db_user)
            return db_user
