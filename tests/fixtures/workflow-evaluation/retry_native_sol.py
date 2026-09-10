def retry(operation, max_attempts):
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    for attempt in range(max_attempts):
        try:
            return operation()
        except RuntimeError:
            if attempt == max_attempts - 1:
                raise
