from fastapi import FastAPI
from api.transaction import router as transactions_router
from repository.Database import create_tables


app = FastAPI( title = "VaultMesh")
app.include_router(transactions_router, prefix = "/api/v1/transactions")


@app.on_event("startup")
def startup() -> None:
    create_tables()
