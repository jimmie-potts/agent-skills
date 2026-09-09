from service import quote


def checkout(items):
    return {"total_cents": quote(items, 500)}


def preview(items):
    return {"total_cents": quote(items, 500)}
