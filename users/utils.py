import os
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

def generate_avatar(email, save_path):
    """
    Генерирует аватарку с первой буквой email на черном фоне.
    :param email: Email пользователя
    :param save_path: Путь, куда сохранить файл (относительно MEDIA_ROOT)
    :return: Полный путь к сохраненному файлу
    """
    initial = email[0].upper() if email else '?'
    size = (200, 200)
    image = Image.new('RGB', size, color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    try:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 100)
                break        
        if not font:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), initial, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) / 2 - bbox[0]
    y = (size[1] - text_height) / 2 - bbox[1]
    draw.text((x, y), initial, fill=(255, 255, 255), font=font)
    full_path = os.path.join(settings.MEDIA_ROOT, save_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    image.save(full_path)
    return save_path
