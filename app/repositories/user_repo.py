from .base import BaseRepository, AsyncSession, register_repository
from app.models.user_model import User


@register_repository("user_repo")
class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
