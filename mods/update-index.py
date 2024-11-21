import subprocess
from urllib.parse import quote
from os import makedirs, listdir, path
from time import sleep

def parse_mods():
    with open("mods.txt", "r") as file:
        mods = {}
        label = "default"
        lines = [line.rstrip('\n') for line in file.readlines() if not (line.startswith('#') or line.isspace())]
        for line in lines:
            if line.endswith(':'):
                label = line.rstrip(':')
            else:
                if not label in mods:
                    mods[label] = []
                path, _, res = line.rpartition('/')
                mods[label].append('/'.join([path, quote(res)]))
    return mods

mods = parse_mods()

makedirs("mods", exist_ok=True)
with open("mods/index.txt", "w") as index:
    for label, links in mods.items():
        index.write(f"{label}:\n")
        index.writelines(['/'.join((l[-4], l[-2], l[-1]))+'\n' for l in map(lambda x: x.split('/'), links) if len(l) >= 4])
        index.write('\n')
