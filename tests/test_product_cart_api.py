from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def login(role, username="aletha"):
    resp = client.post("/auth/login", json={"username": username, "role": role})
    assert resp.status_code == 200
    return resp.json()["access_token"]

def test_create_cart():
    admin_token = login("admin", "admin1")
    user_token = login("user", "aletha")

    #create product
    res = client.post("/products", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "sku":"TESTSKU","name":"Widget","price": 10.50
    })
    assert res.status_code == 200, res.text

    #listing products
    res = client.get("/products?page=1&pageSize=10")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1

    #create cart
    res = client.post("/cart/items", headers={"Authorization": f"Bearer {user_token}"}, json={"sku":"TESTSKU","qty":2})
    assert res.status_code == 200

    #listing cart
    res = client.get("/cart", headers={"Authorization": f"Bearer {user_token}"})
    assert res.status_code == 200
    cart = res.json()
    assert cart["itemCount"] == 2
    assert cart["subtotal"] == "21.00"
