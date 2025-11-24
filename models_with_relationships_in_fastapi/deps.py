from typing import Annotated
from fastapi import Depends
from models import *
from db import *
SessionDep = Annotated[Session, Depends(get_session)]