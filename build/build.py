import os, re

README_INPUT_FILE = os.path.join("build", "README_src.md")
README_OUTPUT_FILE = os.path.join("README.md")

TEXT_SVG_OUTPUT_FOLDER = "text imgs"

SVG_H = 20

TEXT_SVG_W = 100
TEXT_SVG_X = 5
TEXT_SVG_Y = 12

def create_text_svg(text: str, output_svg_path: str):
    new_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{TEXT_SVG_W}" height="{SVG_H}">
        <text
            x="{TEXT_SVG_X}"
            y="{TEXT_SVG_Y}"
            font-family="Arial"
            font-size="16"
            dominant-baseline="middle">
            {text}
        </text>
    </svg>
    """

    with open(output_svg_path, "w") as d:
        d.write(new_svg)

def create_img(icon_svg_path: str, text_svg_path: str | None, text: str, icon_bg: str | None) -> str:
    icon_bg_str = "" if icon_bg is None else f"background-color: {icon_bg};"

    icon_svg= f'<img title="{text} Icon" alt="{text} Icon" src="{icon_svg_path}" style="height: {SVG_H}px; {icon_bg_str}">'

    if text_svg_path is None:
        return icon_svg
    
    text_svg = f'<img title="{text}" alt="{text}" src="{text_svg_path}">'

    return icon_svg + text_svg

DATA_DICT = {
    "Docker_Text": {
        "SVG": "imgs/Docker/docker-mark-ocean-blue.svg",
        "TEXT": "Docker",
        "ICON": False
    },
    "TypeScript_Text": {
        "SVG": "imgs/TypeScript/ts-logo-512.svg",
        "TEXT": "TypeScript",
        "ICON": False
    },
    "Python_Text": {
        "SVG": "imgs/Python/python.svg",
        "TEXT": "Python",
        "ICON": False
    },
    "Java_Text": {
        "SVG": "imgs/Java/java.svg",
        "TEXT": "Java",
        "ICON": False,
        "ICON_BG": "white"
    },
    "React_Text": {
        "SVG": "imgs/React/react.svg",
        "TEXT": "React",
        "ICON": False
        },
    "Flask_Text": {
        "SVG": "imgs/Flask/flask-icon.svg",
        "TEXT": "Flask",
        "ICON": False
    },

    "Docker_Icon": {
        "SVG": "imgs/Docker/docker-mark-ocean-blue.svg",
        "TEXT": "Docker",
        "ICON": True
    },
    "TypeScript_Icon": {
        "SVG": "imgs/TypeScript/ts-logo-512.svg",
        "TEXT": "TypeScript",
        "ICON": True
    },
    "Python_Icon": {
        "SVG": "imgs/Python/python.svg",
        "TEXT": "Python",
        "ICON": True
    },
    "Java_Icon": {
        "SVG": "imgs/Java/java.svg",
        "TEXT": "Java",
        "ICON": True,
        "ICON_BG": "white"
    },
    "React_Icon": {
        "SVG": "imgs/React/react.svg",
        "TEXT": "React",
        "ICON": True
        },
    "Flask_Icon": {
        "SVG": "imgs/Flask/flask-icon.svg",
        "TEXT": "Flask",
        "ICON": True
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
        text_svg_output_path = None if value["ICON"] else os.path.join(TEXT_SVG_OUTPUT_FOLDER, f"{value["TEXT"]}.svg")
        if text_svg_output_path is not None:
            create_text_svg(value["TEXT"], text_svg_output_path)
        parts[i] = create_img(value["SVG"], text_svg_output_path, value["TEXT"], value.get("ICON_BG"))
    else:
        print(f"ERR - key {key} not in REPLACE_DICT")

with open(README_OUTPUT_FILE, "w") as d:
    d.write("".join(parts))