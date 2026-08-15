import os, base64
from urllib.request import urlopen, Request

README_INPUT_FILE = os.path.join("build", "README_src.md")
README_OUTPUT_FILE = os.path.join("README.md")

CACHE_FILE = os.path.join("build", "cache")

SHIELDS_OUTPUT_FOLDER = "shields"

cache: list[str] = []
new_cache: list[str] = []

with open(CACHE_FILE, "r") as d:
    cache = d.readlines()

def create_shield(output_file: str, input_svg: str, icon_text:str, text: str) -> None:
    with open(input_svg, "r") as d:
        x = d.read()

    x = base64.b64encode(x.encode("utf-8")).decode("utf-8")

    x = "data:image/svg+xml;base64," + x

    url = f"https://img.shields.io/badge/{icon_text}-{text}-%23555555?style=for-the-badge&logo={x}&labelColor=%23777777"

    if url + "\n" not in new_cache:
        new_cache.append(url + "\n")

    if url + "\n" in cache:
        return

    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urlopen(req) as response:
        data = response.read().decode("utf-8")

    with open(output_file, "w") as d:
        d.write(data)

def create_img(path: str, alt: str, link: str | None) -> str:
    if link is None:
        return f'<img src="{path}" alt="{alt}">'
    else:
        return f"[![{alt}]({path})]({link})"

DATA_DICT = {
    "C": {
        "SVG": "imgs/C/c.svg",
        "SVG_TEXT": "",
        "TEXT": "C",
        "FILE": "C.svg",
        "URL": None
    },
    "Docker": {
        "SVG": "imgs/Docker/docker-mark-ocean-blue.svg",
        "SVG_TEXT": "",
        "TEXT": "Docker",
        "FILE": "Docker.svg",
        "URL": None
    },
    "Docker-Me": {
        "SVG": "imgs/Docker/docker-mark-ocean-blue.svg",
        "SVG_TEXT": "Docker",
        "TEXT": "srisner",
        "FILE": "Docker-Me.svg",
        "URL": "https://hub.docker.com/repositories/srisner"
    },
    "Flask": {
        "SVG": "imgs/Flask/flask-icon.svg",
        "SVG_TEXT": "",
        "TEXT": "Flask",
        "FILE": "Flask.svg",
        "URL": None
    },
    "Itch.io-Me": {
        "SVG": "imgs/Itch/itchio-logo-textless-black.svg",
        "SVG_TEXT": "Itch.io",
        "TEXT": "Samuel%20Risner",
        "FILE": "Itch-Me.svg",
        "URL": "https://itch.io/profile/samuel-risner"
    },
    "Java": {
        "SVG": "imgs/Java/java.svg",
        "SVG_TEXT": "",
        "TEXT": "Java",
        "FILE": "Java.svg",
        "URL": None
    },
    "MicroPython": {
        "SVG": "imgs/MicroPython/micropython.svg",
        "SVG_TEXT": "",
        "TEXT": "MicroPython",
        "FILE": "MicroPython.svg",
        "URL": None
    },
    "Python": {
        "SVG": "imgs/Python/python.svg",
        "SVG_TEXT": "",
        "TEXT": "Python",
        "FILE": "Python.svg",
        "URL": None
    },
    "React": {
        "SVG": "imgs/React/react.svg",
        "SVG_TEXT": "",
        "TEXT": "React",
        "FILE": "React.svg",
        "URL": None
        },
    "TypeScript": {
        "SVG": "imgs/TypeScript/ts-logo-512.svg",
        "SVG_TEXT": "",
        "TEXT": "TypeScript",
        "FILE": "TypeScript.svg",
        "URL": None
    },
}

parts: list[str] = []

with open(README_INPUT_FILE, "r") as d:
    readme_input = d.read()

for part in readme_input.split("{{"):
    parts.extend(part.split("}}"))

for i in range(1, len(parts), 2):
    key: str = parts[i].strip()
    value = DATA_DICT.get(key)

    if value is not None:
        shield_path = os.path.join(SHIELDS_OUTPUT_FOLDER, value["FILE"])
        create_shield(shield_path, value["SVG"], value["SVG_TEXT"], value["TEXT"])
        parts[i] = create_img(f"{SHIELDS_OUTPUT_FOLDER}/{value["FILE"]}", value["TEXT"], value["URL"])
    else:
        print(f"ERR - key {key} not in REPLACE_DICT")

with open(README_OUTPUT_FILE, "w") as d:
    d.write("".join(parts))

with open(CACHE_FILE, "w") as d:
    d.writelines(new_cache)