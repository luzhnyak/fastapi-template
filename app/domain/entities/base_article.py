from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from app.utils.strip_tags_and_trim import strip_tags_and_trim
from app.utils.photos import get_list_photos_api
from app.core.config import settings


@dataclass
class RelationshipArticle:
    id: int
    name: str
    slug: str


@dataclass(kw_only=True)
class BaseArticle:
    id: int
    name: str
    slug: str
    content: str
    created_at: datetime
    updated_at: datetime
    image: Optional[str] = None
    thumbnail: Optional[str] = None
    video: Optional[str] = None
    ena: Optional[str] = None
    is_gallery: Optional[bool] = False

    @property
    def maket(self) -> str:
        return "NONE"

    @property
    def icon(self) -> str:
        return "icon-file-alt"

    @property
    def icon_color(self) -> str:
        return "text-primary"

    @property
    def description(self) -> str:
        return strip_tags_and_trim(self.content)

    @property
    def main_image(self) -> str:
        if self.image:
            if self.image.startswith("http"):
                return self.image
            else:
                return f"{settings.app.BASE_URL}{self.image}"

        return get_list_photos_api(self.path, self.id, self.video)[0]["resize"]

    @property
    def images(self) -> List[dict]:
        return get_list_photos_api(self.path, self.id, self.video)
