def unwrap(value: str | None) -> str:
    if value is None:
        raise ValueError("called `unwrap()` on a `None` value")
    return value
