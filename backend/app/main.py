from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import auth, customers, orders, products

app = FastAPI(title="ERPk Order Management", version="1.0.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return the first validation error as a plain string instead of a nested list."""
    messages = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        msg = error["msg"].replace("Value error, ", "")
        messages.append(f"{field}: {msg}" if field else msg)
    return JSONResponse(
        status_code=422,
        content={"detail": messages[0] if len(messages) == 1 else messages},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")


@app.get("/health")
async def health():
    """Liveness probe — returns 200 when the application is running."""
    return {"status": "ok"}
