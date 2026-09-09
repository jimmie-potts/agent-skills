def quote(item_cents, shipping_cents):
    values = [*item_cents, shipping_cents]
    if any(type(value) is not int or value < 0 for value in values):
        raise ValueError("Prices must be nonnegative integer cents")
    return sum(values)
