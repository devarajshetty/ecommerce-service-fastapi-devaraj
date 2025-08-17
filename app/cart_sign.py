import hashlib
from typing import List, Dict

def generate_cart_signature(cart_items: List[Dict[str, int]]) -> str:
    """
    Generate a deterministic cart signature.

    Rules:
    - Merge duplicate items by sku (sum qty).
    - Sort items by sku ascending.
    - Build normalization string: sku:qty joined by |
    - Compute SHA-256 hex digest of normalization string.

    Args:
        cart_items (List[Dict]): List of dicts with 'sku' and 'qty'.

    Returns:
        str: SHA-256 hex digest.
    """
    # Merge duplicates
    merged = {}
    for item in cart_items:
        sku = item["sku"]
        qty = item["qty"]
        merged[sku] = merged.get(sku, 0) + qty

    # Sort by SKU
    sorted_items = sorted(merged.items(), key=lambda x: x[0])

    # Build normalization string
    normalization_str = "|".join([f"{sku}:{qty}" for sku, qty in sorted_items])

    # Compute SHA-256
    signature = hashlib.sha256(normalization_str.encode("utf-8")).hexdigest()

    return signature, normalization_str