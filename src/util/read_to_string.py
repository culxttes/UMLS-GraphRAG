def read_to_string(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
