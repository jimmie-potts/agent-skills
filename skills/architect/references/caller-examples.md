# Caller examples and invariant boundaries

Read before writing caller usage for a consequential interface, before encoding
an invariant in types, and before explaining the chosen design to its owner.

## Write the caller example first

A consequential interface is one that other modules, services, jobs, or people
will call, or one that owns state they depend on. For each one, write a caller
example from real code before endorsing a candidate. Name:

- **Caller and real setup:** the existing module or actor that calls, and what
  it already holds at that point, such as configuration, identifiers, handles,
  and permissions. Take this from current code, not an idealized caller.
- **Owner:** the module that owns the state the operation reads or changes, and
  which actors may write it.
- **Smallest useful operation:** the one call the caller needs, with its inputs
  and result.
- **Success path:** what the caller receives and does next.
- **Failure and recovery path:** how each failure appears to the caller, what
  state remains afterward, and what the caller does next, such as retry,
  compensate, or report. For mutable state, include a repeated call and an
  interrupted operation.
- **Caller knowledge:** what the caller must know to use the interface
  correctly, and what stays behind it.

Do not endorse a candidate whose example lacks an owner or a failure and
recovery path. Complete the example, or record the gap under open questions.
An internal helper or a local change with no new public contract needs no
separate example; a one-line call in the design package is enough.

This TypeScript example shows the level of detail. Use the project's language
and vocabulary.

```ts
// Caller: the POST /orders/:id/pay handler. Setup: it holds orderId from the
// route and the request ID; `payments` was constructed at startup.
const result = await payments.capture({ orderId, idempotencyKey: requestId });
switch (result.kind) {
  case "captured":
    return { status: 200, body: { receiptId: result.receiptId } };
  case "declined":
    // No payment state changed. The customer may retry with another card.
    return { status: 402, body: { reason: result.reason } };
  case "pending":
    // Gateway timeout. Retrying with the same idempotencyKey cannot charge twice.
    return { status: 202, body: { retryAfterSeconds: result.retryAfterSeconds } };
}
```

- Owner: `payments` owns the payment record and the gateway call. The handler
  never writes payment state.
- Behind the interface: the gateway protocol, gateway retries, and idempotency
  storage.
- Caller knowledge: the three outcomes, and that a retry must reuse the key.

## Encode invariants selectively

Encode a valid state or a checked external boundary in types when it prevents a
demonstrated class of error: an observed defect, a review finding, or an
invalid combination that the caller example shows callers can construct.
Otherwise keep a runtime check or a test.

Change only the types on the path the design touches. Do not start a
repository-wide type migration, compiler-strictness change, or blanket style
rule, such as banning comments or a type everywhere, as part of a design.

```ts
// Before: nothing rejects { status: "captured", receiptId: undefined }.
type Payment = {
  status: "pending" | "captured" | "declined";
  receiptId?: string;
  reason?: string;
};

// After: each status carries exactly the fields that are valid for it.
type Payment =
  | { status: "pending" }
  | { status: "captured"; receiptId: string }
  | { status: "declined"; reason: string };

// External boundary: gateway JSON becomes a Payment only after this check.
function parseGatewayPayment(raw: unknown): Payment | GatewayParseError;
```

The compiler now rejects a captured payment without a receipt in internal
code, and `parseGatewayPayment` rejects it in external data. Modules that only
read payments through existing accessors need no change; update only the code
that constructed the invalid shape. In other languages, use the equivalent sum
type or validating constructor.

## Explain the chosen shape

After choosing, explain the design to its owner in a few sentences of project
vocabulary. Cover what the caller does, who owns the state, what happens on
failure, and what the design gives up. Point to the caller example rather than
restating it. Add a small diagram only when ownership or data flow crosses
several modules and prose is hard to follow. Do not create a slide deck, report
page, or other presentation artifact unless the user asks for one.
