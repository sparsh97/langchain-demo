import os
from dotenv import load_dotenv
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age:int
    movie:str


person = Person(name="Sparsh", age=24, movie="avatar")
print(person)
load_dotenv()

os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")