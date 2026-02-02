import re
from app.core.config import settings

BASE_URL = settings.app.BASE_URL


def convert_relative_to_absolute(html: str) -> str:
    return re.sub(
        r'src="(/[^"]+)"',
        lambda match: f'src="{BASE_URL.rstrip("/")}{match.group(1)}"',
        html,
    )
