from fastapi import FastAPI
from .database import engine, Base
from .routers import authentication, products, cart

app = FastAPI(title="Aletha Assesment")

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status":"ok"}

app.include_router(authentication.router)
app.include_router(products.router)
app.include_router(cart.router)
