from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print("Before request processing")

    print(f"Method: {request.method}")
    print(f"Path: {request.url.path}")

    response = await call_next(request)

    print("After request processing")

    return response

@app.get("/hello")
async def say_hello():
    return {
        "message": "Hello, Welcome to FastAPI!"
    }

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "The requested resource was not found"}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )