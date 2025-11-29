
from typing import Annotated
from fastapi import Depends
from app.db import get_session,Session

SessionDep = Annotated[Session,Depends(get_session)]