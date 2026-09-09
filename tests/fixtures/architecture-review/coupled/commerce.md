# Commerce rules

Order subtotal: the sum of item prices in integer cents.
Shipping charge: 500 cents below a 5000-cent subtotal, otherwise zero.
Checkout and invoice must charge the same amount. The quote response field is
total_cents; the invoice response field is amount_due. Keep those fields stable.
