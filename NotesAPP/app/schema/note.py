from pydantic import BaseModel,Field
from typing import Annotated
class Note(BaseModel):
    id:Annotated[int,Field(ge=1)]
    title:str
    content:str
