import os
import sys
from typing import Dict, List, Optional


DIRS = ["/interface", "/ip", "/routing", "/system", "/tool", "/queue"]


def get_folder(fname: str) -> str:
    for d in DIRS:
        if fname.startswith(d):
            return fname.split(" ")[0].strip("/")
    return ""


def make_fname(fname: str) -> str:
    filename = fname.lstrip("/").replace(" ", "-").strip("\n")
    folname = get_folder(fname)
    if folname:
        os.makedirs(folname, exist_ok=True)
        return f"{folname}/{filename}"
    return filename


def save_dirf(fname: str, contents: List[str], headers: Optional[List[str]] = None):
    filename = make_fname(fname)
    with open(f"{filename}.rsc", "w") as writer:
        if headers:
            writer.writelines(headers)
        writer.write(fname)
        writer.writelines(contents)


def main():
    if len(sys.argv) < 2:
        return print(f"Usage: {sys.argv[0]} <filename>")
    filename = sys.argv[1]
    with open(filename, "r") as reader:
        contents = reader.readlines()
        if not contents:
            return print(f"{filename} empty!")
    headers = list()
    dirf = dict()
    dirt = None
    for content in contents:
        if not dirt and content.startswith("#"):
            headers.append(content)
            continue
        if content.startswith("/"):
            dirt = content
            continue
        if not dirt:
            continue
        if dirt not in dirf:
            dirf[dirt] = list()
        dirf[dirt].append(content)
    for k, v in dirf.items():
        save_dirf(k, v, headers)


if __name__ == "__main__":
    main()
