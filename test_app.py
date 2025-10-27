
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Test API', version='1.0.0')

class User(BaseModel):
    name: str
    email: str

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('/users')
async def create_user(user: User):
    return user
