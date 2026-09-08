"""Known working solution used to verify the grader, not given to workers."""


def retry(operation, max_attempts):
    if max_attempts < 1:
        raise ValueError('max_attempts must be positive')
    for attempt in range(max_attempts):
        try:
            return operation()
        except RuntimeError:
            if attempt == max_attempts - 1:
                raise
