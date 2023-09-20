from typing import Dict
from os import listdir, remove
from base64 import b64decode, b64encode
from PIL import Image, ImageTk
from io import BytesIO

# from cairosvg import svg2png

if __name__ == "__main__":
    # im = Image.open(
    #     BytesIO(
    #         b64decode(
    #             b"iVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAJ1BMVEUAAABhYW1gYGpgZmZdY2hgYGZeYmhfY2hfZGhfY2hfYmhfY2j////n6LN1AAAAC3RSTlMAFRgoLC29v9LT10/SkkUAAAABYktHRAyBs1FjAAAAUElEQVQY02NgoBwwF4FIsQAwh22nAAMD4+wEMIexexEDg8QuBYg6IAMsAJOCSzAwSO6cPRFuHmM3QgKVg6wMxQBko1EsRXEOSyLYoQ5U8DMAE8gYtYkhyDMAAAAASUVORK5CYII="
    #         )
    #     )
    # )

    icons_dir: str = "assets/icons/png"

    save_icon_dict_file_path: str = "assets/icons/icon_dict.py"

    icon_dict: Dict[str, bytes] = {}
    for icon_file_name in listdir(icons_dir):
        icon_file_path: str = f"{icons_dir}/{icon_file_name}"
        with open(icon_file_path, mode="rb") as icon_file:
            icon_name = icon_file_name.replace(".png", "")

            icon_dict[icon_name] = b64encode(icon_file.read())

    with open(save_icon_dict_file_path, mode="w") as icon_dict_file:
        content: str = f"_icon_dict:Dict[str,bytes] = {str(icon_dict)}"
        icon_dict_file.write(content)
