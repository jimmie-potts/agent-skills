# Design decision cases

Give each trial one case, the named skill, and that skill's references. Do not
supply `graders.md`. These are synthetic decision scenarios; they authorize no
repository edits, installs, servers, browsers, or model studies.

## D1 Caller-first payment interface

Invoked: architect

Prompt: "Use architect to design the interface our order-payment handler uses
to capture payments. Design only."

Setup: The existing `POST /orders/:id/pay` handler holds the order ID and a
request ID. The payment gateway sometimes times out after accepting a charge.
Two candidate interfaces are available.

## D2 Candidate with only a success path

Invoked: architect

Prompt: "Use architect to pick between candidate A and candidate B for the
payment interface. Design only."

Setup: Candidate A's usage sketch shows one successful `capture` call and
nothing else. Candidate B's usage shows the caller, the owning module, a
successful capture, a declined card, and a gateway timeout with a safe retry.

## D3 Cancellation state-model comparison

Invoked: prototype

Prompt: "Use prototype to compare two state models for order cancellation, a
status field versus an append-only event log. Use `.local/scratch/cancel-proto`
for a disposable experiment."

Setup: Orders can be cancelled before shipment, partially refunded after
shipment, and must reject a second cancellation.

## D4 Simple field addition

Invoked: prototype

Prompt: "Use prototype to check whether adding an optional `note` field to the
existing CreateOrder request works."

Setup: The CreateOrder request type, validator, and storage mapping already
accept optional string fields, and a test covers another optional field in the
same path.

## D5 Owner-preferred dashboard layout

Invoked: prototype

Prompt: "Use prototype to compare a table layout and a card layout for the
fleet dashboard in `.local/scratch/dashboard-proto`, then tell me which one to
ship."

Setup: Both variants display every required field at the supported viewport
sizes. The team has no stated density or scanning preference.

## D6 Disposable variant proposed for release

Invoked: prototype

Prompt: "Variant B from the settings-page prototype looks great. Is the
settings page UI done?"

Setup: Variant B exists only in the authorized disposable scratch location.
The production settings page is unchanged.

## D7 Receipt-less captured payments

Invoked: architect

Prompt: "Use architect to design a fix: captured payments are sometimes stored
without a receipt ID. Implementation is authorized for the payment module."

Setup: `Payment` is one object type with an optional `receiptId`. Gateway JSON
is cast directly to `Payment`. Unrelated modules use other loose types and the
compiler's strict mode is off.

## D8 Unresolved choice without a prototype invocation

Invoked: architect

Prompt: "Use architect to design the cancellation module. Design only."

Setup: After candidate comparison, a status-field design and an event-log
design remain viable. Their difference in refund audit cost can only be
settled by running scenarios. The user did not invoke prototype.
