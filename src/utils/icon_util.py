from typing import Dict
from PIL import Image
from io import BytesIO
from base64 import b64decode


class IconUtil:
    _icon_dict: Dict[str, bytes] = {
        "clear_light": b"iVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAJ1BMVEUAAABhYW1gYGpgZmZdY2hgYGZeYmhfY2hfZGhfY2hfYmhfY2j////n6LN1AAAAC3RSTlMAFRgoLC29v9LT10/SkkUAAAABYktHRAyBs1FjAAAAUElEQVQY02NgoBwwF4FIsQAwh22nAAMD4+wEMIexexEDg8QuBYg6IAMsAJOCSzAwSO6cPRFuHmM3QgKVg6wMxQBko1EsRXEOSyLYoQ5U8DMAE8gYtYkhyDMAAAAASUVORK5CYII=",
        "clear_dark": b"iVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAJ1BMVEUAAACenqqVn6qZn6acoqiZn6SaoaaaoKaaoKaZoKaaoKaaoKb///90Cst2AAAAC3RSTlMAFRgoLC29v9LT10/SkkUAAAABYktHRAyBs1FjAAAAUElEQVQY02NgoBwwF4FIsQAwh22nAAMD4+wEMIexexEDg8QuBYg6IAMsAJOCSzAwSO6cPRFuHmM3QgKVg6wMxQBko1EsRXEOSyLYoQ5U8DMAE8gYtYkhyDMAAAAASUVORK5CYII=",
    }

    @staticmethod
    def has_icon_name(name: str) -> bool:
        return name in IconUtil._icon_dict

    @staticmethod
    def get_icon(name: str) -> Image:
        if name not in IconUtil._icon_dict:
            raise KeyError(f"icon name '{name}' not found in icon_dict")

        icon_base64: bytes = IconUtil._icon_dict[name]
        return Image.open(BytesIO(b64decode(icon_base64)))
