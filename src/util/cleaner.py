import re

# Matches an entire string wrapped in triple backticks, optionally with a language tag.
_CODE_FENCE_RE = re.compile(
    r"\s*```\n(.*?)\n```\s*$",
    re.DOTALL,
)


def strip_code_fences(text: str) -> str:
    """
    If the input is wrapped in a triple-backtick code fence (optionally with a language),
    return only the inner content. Otherwise, return the text unchanged.

    Parameters:
        text (str): The input text, possibly fenced with ```.

    Returns:
        str: The unfenced inner content, or the original text if no full fence matches.

    Examples:
        >>> strip_code_fences("```\\nprint('hi')\\n```")
        "print('hi')"
        >>> strip_code_fences("```python\\nprint('hi')\\n```")
        "print('hi')"
        >>> strip_code_fences("no fences here")
        "no fences here"
    """
    m = _CODE_FENCE_RE.fullmatch(text)
    return m.group(1) if m else text
