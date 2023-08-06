import os
from pathlib import Path


def find_files(root_dir, name, ext: str):
    file_paths = []
    while ext.startswith("."):
        ext = ext.removeprefix(".")
    key = f".{ext}"
    for dirpath, _, filenames in os.walk(root_dir):
        if file_paths:
            break
        for filename in filenames:
            basename = str(filename)
            if basename.endswith(key):
                basename = basename[: basename.rindex(".")]
                if basename == name:
                    file_path = os.path.join(dirpath, filename)
                    file_paths.append(file_path)
                    break
    return file_paths


def get_accountKeyPath(root_dir: str, accountKeyName: str, ext: str = "json"):
    name = accountKeyName
    root_dir = Path(root_dir)
    if not root_dir.is_dir():
        root_dir = root_dir.parent
    accountKeyPaths = find_files(root_dir=root_dir, name=name, ext=ext)
    if not accountKeyPaths:
        root_dir = root_dir.parent
        accountKeyPaths = find_files(root_dir=root_dir, name=name, ext=ext)
    return accountKeyPaths[0]
