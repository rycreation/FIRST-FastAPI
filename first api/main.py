from fastapi import FastAPI,Body

app = FastAPI()

AVENGERS = [
    {"id": 1 , "name":"peter", "course": "python","is_completed": False},
    {"id": 2 , "name":"tony", "course": "java","is_completed": True},
    {"id": 3 , "name":"bruse", "course": "c+","is_completed": False},
    {"id": 4 , "name":"steve", "course": "nothing","is_completed": True},
    {"id": 5 , "name":"thor", "course": "god","is_completed": False},
]    

#HOME
@app.get("/")
def HELLO_WORLD():
    return "THE AVENGERS"


#GET ALL MEMBERS
@app.get("/avengers/all")
def get_all_avengers():
    return AVENGERS


#GET DATA BY CONDITION
@app.get("/avengers/completed")
def get_completed_avengers(is_completed: bool):
    result = []

    for avengers in AVENGERS:
        if avengers["is_completed"] == is_completed:
            result.append(avengers)

    return result



#CREATE A MEMBERS
@app.post("/avengers/create")
def create_avengers(new_avengers: dict = Body(...)):
    AVENGERS.append(new_avengers)
    return {"message":"APPROVED"}


#UPDATE MEMBER ONLY 1ST
@app.put("/avengers/update")
def update_avengers(exiting_avengers=Body()):      # THIS CODE ONLY UPDATE 1 DATA OR MEMBER.
    AVENGERS[0]= exiting_avengers
    return{"message":"UPDATE SUCCESS"}


#DELETE MEMBERS DATA BY ID
@app.delete("/avengers/{id}")
def delete_by_id(id: int):
    for index in range(len(AVENGERS)):
        if AVENGERS[index]["id"] == id:
            AVENGERS.pop(index)
            return {"message": "successfully deleted"}
    return {"message": "member not found"}





