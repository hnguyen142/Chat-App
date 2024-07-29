from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Ideally, store sensitive keys in environment variables.
PRIVATE_KEY = "4ad25e0e-9d7e-48c8-9df5-2d31e09305b1"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str

@app.post('/authenticate')
async def authenticate(user: User):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                'https://api.chatengine.io/users/',
                data={
                    "username": user.username,
                    "secret": user.username,
                    "first_name": user.username,
                },
                headers={"Private-Key": PRIVATE_KEY}
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Request failed: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"An error occurred: {exc}")

    return response.json()