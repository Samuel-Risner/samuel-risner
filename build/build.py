import os, base64
from urllib.request import urlopen, Request

README_INPUT_FILE = os.path.join("build", "README_src.md")
README_OUTPUT_FILE = os.path.join("README.md")

SHIELDS_OUTPUT_FOLDER = "shields"

def create_shield(output_file: str, input_svg: str, text: str) -> None:
    with open(input_svg, "r") as d:
        x = d.read()

    x = base64.b64encode(x.encode("utf-8")).decode("utf-8")

    x = "data:image/svg+xml;base64," + x

    url = f"https://img.shields.io/badge/{text}-%23555555?style=for-the-badge&logo={x}&labelColor=%23777777"

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

def create_img(path: str, text: str) -> str:
    return f'<img title="{text}" alt="{text}" src="{path}">'

DATA_DICT = {
    "Docker": {
        "SVG": "imgs/Docker/docker-mark-ocean-blue.svg",
        "TEXT": "Docker"
    },
    "TypeScript": {
        "SVG": "imgs/TypeScript/ts-logo-512.svg",
        "TEXT": "TypeScript"
    },
    "Python": {
        "SVG": "imgs/Python/python.svg",
        "TEXT": "Python"
    },
    "Java": {
        "SVG": "imgs/Java/java.svg",
        "TEXT": "Java"
    },
    "React": {
        "SVG": "imgs/React/react.svg",
        "TEXT": "React"
        },
    "Flask": {
        "SVG": "imgs/Flask/flask-icon.svg",
        "TEXT": "Flask"
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
        shield_path = os.path.join(SHIELDS_OUTPUT_FOLDER, f"{value["TEXT"]}.svg")
        create_shield(shield_path, value["SVG"], value["TEXT"])
        parts[i] = create_img(shield_path, value["TEXT"])
    else:
        print(f"ERR - key {key} not in REPLACE_DICT")

with open(README_OUTPUT_FILE, "w") as d:
    d.write("".join(parts))