#!/usr/bin/env python3
"""Cycle content.proxy between SOCKS5 and system, announcing which is active."""
import os
import subprocess

QUTE_CONFIG_DIR = os.path.expanduser("~/.config/qutebrowser")
STATE_FILE = os.path.join(QUTE_CONFIG_DIR, "proxy_index")

PROXIES = [
    ("SOCKS5", "socks5://127.0.0.1:1080"),
    ("System", "system"),
]


def main():
    current_index = 0
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                current_index = int(f.read().strip())
            except ValueError:
                current_index = 0

    current_index = (current_index + 1) % len(PROXIES)

    with open(STATE_FILE, "w") as f:
        f.write(str(current_index))

    name, value = PROXIES[current_index]

    subprocess.run([
        "qutebrowser", "--set", "content.proxy", value,
    ])

    print(f"Proxy: {name}")


if __name__ == "__main__":
    main()
