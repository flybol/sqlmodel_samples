from typing import Annotated
from fastapi import Depends
from models_with_relationships_in_fastapi.models import *
from models_with_relationships_in_fastapi.db import *
SessionDep = Annotated[Session, Depends(get_session)]