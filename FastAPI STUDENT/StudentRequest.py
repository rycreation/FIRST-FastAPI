from typing import Optional
from pydantic import BaseModel, Field

class Srequest(BaseModel):
    id: Optional[int] = Field(ge=1,default=None, description="During student ID is not required")
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0,le=100)
    course:str= Field(min_length=2, max_length=50)
    is_completed: Optional[bool] = Field(default=False)
    

    model_config = {
        "json_schema_extra":{
            "example":{
                "id": 1,
                "name": "Student Name",
                "age": 25,
                "course": "Mathematics",
                "is_completed": False
            }
        }
    }