# Decision 1: Integer cents

Prices use integer cents. The pricing service accepts item subtotals and a
shipping charge, rejecting negative input. One entrypoint hides validation and
aggregation; callers do not duplicate either rule.
