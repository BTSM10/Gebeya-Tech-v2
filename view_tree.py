import os


def print_tree(path=".", prefix=""):
    """Print the directory tree starting from path."""
    entries = sorted(os.listdir(path))
    entries = [e for e in entries if e not in {"__pycache__", ".git", "anonymized"}]
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        print(prefix + connector + entry)
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            extension = "    " if i == len(entries) - 1 else "│   "
            print_tree(full_path, prefix + extension)


if __name__ == "__main__":
    print_tree()
