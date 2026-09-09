class LedgerUnavailable(Exception):
    pass


def post(client, cents):
    try:
        return client.post(cents)
    except TimeoutError as exc:
        raise LedgerUnavailable("Ledger unavailable") from exc
