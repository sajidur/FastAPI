from pydantic import BaseModel
class categoryModel(BaseModel):
    id: int
    name: str
    descriptions:str
