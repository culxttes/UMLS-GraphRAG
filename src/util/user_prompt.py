def user_prompt(base: str, intent: str, request: str):
    return base.replace("{{INTENT}}", intent).replace("{{REQUEST}}", request)
