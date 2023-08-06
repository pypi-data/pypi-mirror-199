def read_file(file):
    with open(file, encoding="utf8") as f:
        text = f.read()
    return text

def write_file(file, text):
    with open(file, "w", encoding="utf8") as f:
        f.write(text)