import os

README_INPUT_FILE = os.path.join("build", "README_src.md")
README_OUTPUT_FILE = os.path.join("README.md")

BADGE_OUTPUT_FOLDER = "badges"

def create_badge(
        icon_path: str,
        text: str, text_w: int,
        output_file: str,
        font_family: str="Arial", font_size: int=16, text_padding_left: int=2, badge_h: int=25, icon_h: int=20
    ) -> None:

    badge_w = badge_h + text_w

    icon_y = (badge_h-icon_h)/2
    icon_x = icon_y

    text_x = badge_h + text_padding_left
    text_y = badge_h/2

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{badge_w}" height="{badge_h}">
    
        <rect x="0" y="0" width="100%" height="100%" fill="#555555"></rect>
        <rect x="0" y="0" width="{badge_h}" height="{badge_h}" fill="#333333"></rect>

        <image href="{icon_path}" height="{icon_h}" x="{icon_x}" y="{icon_y}"></image>

        <text
            x="{text_x}"
            y="{text_y}"
            font-family="{font_family}"
            font-size="{font_size}"
            dominant-baseline="middle"
            fill="#111">
            {text}
        </text>
    </svg>"""

    with open(output_file, "w") as d:
        d.write(svg)

def create_img(path: str, text: str) -> str:
    return f'<img title="{text}" alt="{text}" src="{path}">'

DATA_DICT = {
    "Docker": {
        "SVG": "imgs/Docker/docker-mark-ocean-blue.svg",
        "TEXT": "Docker",
        "TEXT_W": 80
    },
    "TypeScript": {
        "SVG": "imgs/TypeScript/ts-logo-512.svg",
        "TEXT": "TypeScript",
        "TEXT_W": 80
    },
    "Python": {
        "SVG": "imgs/Python/python.svg",
        "TEXT": "Python",
        "TEXT_W": 80
    },
    "Java": {
        "SVG": "imgs/Java/java.svg",
        "TEXT": "Java",
        "TEXT_W": 80
    },
    "React": {
        "SVG": "imgs/React/react.svg",
        "TEXT": "React",
        "TEXT_W": 80
        },
    "Flask": {
        "SVG": "imgs/Flask/flask-icon.svg",
        "TEXT": "Flask",
        "TEXT_W": 80
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
        badge_path = os.path.join(BADGE_OUTPUT_FOLDER, value["TEXT"])
        create_badge(value["SVG"], value["TEXT"], value["TEXT_W"], badge_path)

        parts[i] = create_img(badge_path, value["TEXT"])
    else:
        print(f"ERR - key {key} not in REPLACE_DICT")

with open(README_OUTPUT_FILE, "w") as d:
    d.write("".join(parts))