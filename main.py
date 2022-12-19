from fastapi import FastAPI

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    #expose_headers = ["*"],
)

@app.get("/")
async def root():
    return {"message": "Enviado"}
    