import os

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont


def generate_avatar(text, save_path_relative):
    if not text:
        initial = 'U'
    else:
        initial = text.strip()[0].upper()
        if not initial.isalnum():
            initial = 'U'

    size = (200, 200)
    hash_val = sum(ord(c) for c in text) if text else 100
    bg_color = (
        (hash_val * 53) % 200 + 55, 
        (hash_val * 71) % 200 + 55, 
        (hash_val * 97) % 200 + 55
    )    
    image = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    x = 90
    y = 90
    draw.text((x, y), initial, fill=(255, 255, 255), font=font)
    full_path = os.path.join(settings.MEDIA_ROOT, save_path_relative)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    image.save(full_path)