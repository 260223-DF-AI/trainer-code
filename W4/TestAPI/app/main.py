from fastapi import FastAPI, Body
from pydantic import BaseModel
import json

app = FastAPI()

class item(BaseModel):
    my_string: str

LoudList = []

# get
# www.google.com/
# 127.0.0.1/
@app.get("/")
def get_root():
    """
    Get Root

    This is the root of the API, this is a smoke-check to validat the app is actually running at all.
    """
    return "Hello World"

# post
@app.post("/")
def post_root(wrapper: item):
    """
    Post Root
    
    A simple post request endpoint, to accept a value from the client.
    """
    LoudList.append(wrapper.my_string.upper())
    return json.dumps({"Greeting" : wrapper.my_string.upper()})

@app.get("/loudlist")
def get_loudlist():
    """
    Get LoudList
    
    A simple get request endpoint, to return a list of values from the client.
    """
    return json.dumps({"LoudList" : LoudList})

@app.delete("/benslist")
def delete_benslist():
    """
    Delete Ben's List
    
    A simple delete request endpoint, to clear a list of values from the client.
    """
    LoudList.clear()
    return json.dumps({"LoudList" : LoudList})

@app.put("/loudlist/{list_index}")
def update_list(list_index:int, wrapper: str=Body()):
    """
    Update Loud List
    
    A simple put request endpoint, to update a list value from the client.
    """
    LoudList[list_index] = wrapper
    return json.dumps({"LoudList" : LoudList})



## JSON Notation: JavaScript Object Notation

# "Hello World"
# {"Key" : "Value"}
# {"Greeting" : "Hello World"}


# put

# patch
# delete
# head
# options
# connect