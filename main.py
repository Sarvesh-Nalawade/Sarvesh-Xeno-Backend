from fastapi import FastAPI, APIRouter 
from routers.auth import router as auth_router 
from routers.user import router as user_router
from routers.shopify import router as shopify_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://sarvesh-xeno-frontend.vercel.app",
    "http://localhost:3001",
    "http://localhost:3000",
    "https://localhost:3000",
    "https://localhost:3001",
]

# Add the CORSMiddleware to your application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(shopify_router)      


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run("main:app", reload=True, port=8000)


# uvicorn main:app --host 0.0.0.0 --port 8000
