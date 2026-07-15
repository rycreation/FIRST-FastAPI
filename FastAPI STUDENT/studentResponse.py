from pydantic import BaseModel

class studentResponse(BaseModel):
    id: int
    name: str
    age: int
    course: str
   

    
     