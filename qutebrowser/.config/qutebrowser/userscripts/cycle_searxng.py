#!/usr/bin/env python3
import os
import subprocess

QUTE_CONFIG_DIR = os.path.expanduser("~/.config/qutebrowser")
STATE_FILE = os.path.join(QUTE_CONFIG_DIR, "searxng_index")

INSTANCES = [
    ("searx1_DEFAULT", "https://opnxng.com"),
    ("searx2_DEFAULT", "https://searx.namejeff.xyz"),
    ("searx3_DEFAULT", "https://search.hbubli.cc"),
]

def main():
    current_index = 0
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                current_index = int(f.read().strip())
            except ValueError:
                current_index = 0

    current_index = (current_index + 1) % len(INSTANCES)

    with open(STATE_FILE, "w") as f:
        f.write(str(current_index))

    url = INSTANCES[current_index][1] + "/search?q={}"
    
    subprocess.run([
        "qutebrowser", "--set", "url.searchengines", "DEFAULT", url
    ])

    print(f"Switched to instance {current_index + 1}: {INSTANCES[current_index][1]}")

if __name__ == "__main__":
    main()
