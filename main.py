from fastapi import FastAPI, Depends
from fastapi.openapi.models import RequestBody
from starlette.requests import Request

from system.KafkaHandler import KafkaEventPublisher

from system.auth import get_current_user

app = FastAPI()

kafka_producer = KafkaEventPublisher()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/status")
async def status(user: dict = Depends(get_current_user)):
    return {"message": "We're up and running!", "user": user}


@app.post("/contact_me")
async def contact_me(request: Request):
    body = await request.body()
    kafka_producer.jh_com_post_contact_me(body)
