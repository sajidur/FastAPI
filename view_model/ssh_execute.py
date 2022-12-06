from pydantic import BaseModel
class SSHExecute(BaseModel):
    id: int
    name: str
    command:str