def get_file_contents(filename):
    with open(filename, encoding='utf-8', errors='ignore') as f:
        return f.read()
