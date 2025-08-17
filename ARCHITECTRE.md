# Architecture & Design
## Requirements
- Simpple and readable e‑commerce API with Products and a user based Cart
- user authentication with JWT access tokens
- Implemented Deterministic cart signature function (pure logic)

## Key aspects
- FastAPI, SQLAlchemy
- Postgres DB
- Role based authentication using JWT (HS256). 
    `/auth/login` issues access
- Pydantic validation, clear error messages
- Makefile + scripts for dev/test
- No secrets in repo: `.env.example` provided
- test cases implemted for prod ,cart API's and cart signature logic
- cart signature output given below which is printed during unit testing
```
Normalization 1: a-1:2|b-2:1
Normalization 2: a-1:2|b-2:1
Normalization: a-1:1|b-2:5
```

## DB design
- `Product(id, sku, name, price DECIMAL(10,2))`
- `Cart(id, user_name, sku Forign KEYK->Product.sku, qty)` unique `(user_name, sku)`

## API Endpoints
- Auth:
        `POST /auth/login`
- Admin: 
        `POST /products`, `PUT /products/{id}`, `DELETE /products/{id}`
- User: 
        `GET /products?page1&size=10`
        `POST /cart/items`,
        `PUT /cart/items/{sku}`,
        `DELETE /cart/items/{sku}`,
        `GET /cart`