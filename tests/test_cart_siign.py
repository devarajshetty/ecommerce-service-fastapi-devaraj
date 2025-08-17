from app.cart_sign import generate_cart_signature

def test_same_items_diff_order():
    cart1 = [{"sku": "b-2", "qty": 1}, {"sku": "a-1", "qty": 2}]
    cart2 = [{"sku": "a-1", "qty": 2}, {"sku": "b-2", "qty": 1}]

    sig1, norm1 = generate_cart_signature(cart1)
    sig2, norm2 = generate_cart_signature(cart2)

    print(f"Normalization 1: {norm1}")
    print(f"Normalization 2: {norm2}")

    assert norm1 == norm2
    assert sig1 == sig2

def test_duplicate_sku_merge():
    cart = [
        {"sku": "b-2", "qty": 3},
        {"sku": "a-1", "qty": 1},
        {"sku": "b-2", "qty": 2},
    ]

    sig, norm = generate_cart_signature(cart)

    print(f"Normalization: {norm}")
    assert norm == "a-1:1|b-2:5"
    assert isinstance(sig, str) and len(sig) == 64