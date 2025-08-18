# Aletha Product and Cart API

Used FastAPI app with Products , user based cart and authenticated using JWT auth

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

## API Collection
- Collectionn exported in the file name of "aletha_api_collection.json" and placed in root folder

## Steps to get auth token to use in API headers
    this api desined to get auth token using username and role
    Endpoint:
    `POST /auth/login`
    request payload:
    {"username":"admin1","role":"admin"}


## To use auth tokens:
        Authorization: Bearer <access_token>
        In postman or any api testing tools, we can use this after selecting 
        auth type as "Bearer token"

## Shortcuts & Assumptions
- Role based login (so no password required)

## Environment Variables are
`.env.example` for: `DATABASE_URL`, `JWT_SECRET`, `ACCESS_TOKEN_EXPIRE_MINUTES`

## TO run this project please run these below commands one by one
    ```
    ###windows
    python -m venv venv
    venv\Scripts\Activate
    ##Linuxs
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    to create DB and insert pre requises tables with data
    python -m seed_scripts.seed
    to run dev local server:
    uvicorn app.main:app --reload
    to run unit test:
    pytest -s
```
