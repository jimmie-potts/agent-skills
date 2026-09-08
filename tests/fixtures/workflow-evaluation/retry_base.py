def retry(operation, max_attempts):
    for attempt in range(max_attempts + 1):
        try:
            return operation()
        except Exception:
            if attempt == max_attempts:
                raise
