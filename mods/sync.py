import subprocess
from os import remove, makedirs, listdir, path, fstat
from base64 import b64decode
from colorama import init, Fore
from time import sleep
from hashlib import sha256
import re

r = "repo_base64"
cf = "aHR0cHM6Ly9tZWRpYWZpbGV6LmZvcmdlY2RuLm5ldC9maWxlcy97fS97fS97fQ=="
index_file = "mods/index.txt"

def read_file(path: str):
    with open(path, "r") as file:
        return file.readlines()

def download_file(path: str, url: str):
    dir_path = path.rpartition('/')[0]
    makedirs(dir_path, exist_ok=True)
    subprocess.run(["curl", "-s", "-o", path, url])

def fetch_index(index_url: str):
    download_file(index_file, index_url)

def get_mods(dir_path: str):
    if not path.exists(dir_path): return []
    mod_pattern = re.compile(r"\w+(-\w+)*-\[[0-9a-f]{5}\]")
    return [file 
            for file in map(lambda f: f.rstrip('.jar'), listdir(dir_path)) 
            if not mod_pattern.fullmatch(file) == None]

def parse_index(index_path: str):
    index = {}
    
    if not path.exists(index_path): return index
    label = "default"
    lines = [line.rstrip('\n') for line in read_file(index_path) if not (line.startswith('#') or line.isspace())]

    for l in lines:
        if l.endswith(':'):
            label = l.rstrip(':')
        else:
            if not label in index:
                index[label] = {}

            name, id, res = l.split('/')
            digest = sha256(res.encode()).hexdigest()
            index[label][f"{name}-[{digest[:5]}]"] = {"id": id, "resource": res}
    
    return index

def is_server():
    return path.exists("server.properties") and path.exists("eula.txt")

def download_mod(name: str, info: dict):
    if not ("id" in info and "resource" in info): return
    id = str(info["id"])
    res = info["resource"]
    url = b64decode(cf).decode().format(id[:4], id[4:7].lstrip('0'), res)
    print(f"{name} ⌛", end=" ", flush=True)
    download_file(f"mods/{name}.jar", url)
    print(f"\r{name} {Fore.LIGHTCYAN_EX}✔")

init(autoreset=True) # Colorama

if not path.exists(index_file):
    print(f"{Fore.LIGHTRED_EX}No index file")
    sleep(3)
    exit()

# fetch_index(b64decode(r).decode())
index = parse_index(index_file)
remove(index_file)

required = index.get("default", {})
required.update(index.get("server-only" if is_server() else "client-only", {}))

installed = set(get_mods("mods"))

mod_names = set(required.keys())
correct = installed & mod_names
redundant = installed - mod_names
missing = mod_names - installed

print(f"{len(correct)} | {Fore.LIGHTRED_EX}-{len(redundant)}{Fore.RESET} | {Fore.LIGHTCYAN_EX}+{len(missing)}{Fore.RESET} | {len(required)}")

for mod in redundant: remove(f"mods/{mod}.jar")

for mod in missing: download_mod(mod, required[mod] or {})

print(f"\n{Fore.LIGHTGREEN_EX}Finished! Console will close in 5 seconds")
sleep(5)