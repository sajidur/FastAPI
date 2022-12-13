from pydantic import BaseModel
from view_model.categoryModel import categoryModel
from view_model.ssh_execute import SSHExecute
class category_command_response(BaseModel):
    category: categoryModel
    command: list