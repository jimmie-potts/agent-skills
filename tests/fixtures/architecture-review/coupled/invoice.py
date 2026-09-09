def invoice(item_cents):
    if any(value < 0 for value in item_cents):
        raise ValueError("Negative price")
    subtotal = sum(item_cents)
    shipping = 0 if subtotal >= 6000 else 500
    return {"amount_due": subtotal + shipping}
