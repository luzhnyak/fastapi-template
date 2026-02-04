import os
from app.core.config import settings

IMAGE_FOLDER = settings.app.IMAGE_FOLDER
BASE_URL = settings.app.BASE_URL


def get_list_photos(path: str, id: int, video: str):
    try:
        path_image = os.path.join(IMAGE_FOLDER, path, "resize", str(id))

        list_photo = []
        if os.path.exists(path_image):
            for i in os.listdir(path_image):
                list_photo.append(
                    {
                        "resize": f"/static/img/{path}/resize/{str(id)}/{i}",
                        "thumbnail": f"/static/img/{path}/thumbnail/{str(id)}/{i}",
                    }
                )
            if len(list_photo) > 0:
                return list_photo

        path_image_place = os.path.join(IMAGE_FOLDER, "placesmap", f"{str(id)}.png")

        if path == "places" and os.path.exists(path_image_place):
            list_photo.append(
                {
                    "resize": f"/static/img/placesmap/{str(id)}.png",
                    "thumbnail": f"/static/img/placesmap/{str(id)}.png",
                }
            )
            return list_photo

        if video:
            list_photo.append(
                {
                    "resize": f"https://i.ytimg.com/vi/{video}/maxresdefault.jpg",
                    "thumbnail": f"https://i.ytimg.com/vi/{video}/hqdefault.jpg",
                }
            )
            return list_photo

        list_photo.append(
            {
                "resize": f"/static/img/posts/resize/goldfishnet.jpg",
                "thumbnail": f"/static/img/posts/thumbnail/goldfishnet.jpg",
            }
        )
        return list_photo

    except Exception as e:
        print("Error in get_images places: " + str(e))
        return []


def get_list_photos_api(path: str, id: int, video: str):
    try:
        path_image = os.path.join(IMAGE_FOLDER, path, "resize", str(id))

        list_photo = []
        if os.path.exists(path_image):
            for i in os.listdir(path_image):
                list_photo.append(
                    {
                        "resize": f"{BASE_URL}/static/img/{path}/resize/{str(id)}/{i}",
                        "thumbnail": f"{BASE_URL}/static/img/{path}/thumbnail/{str(id)}/{i}",
                    }
                )
            if len(list_photo) > 0:
                return list_photo

        path_image_place = os.path.join(IMAGE_FOLDER, "placesmap", f"{str(id)}.png")

        if path == "places" and os.path.exists(path_image_place):
            list_photo.append(
                {
                    "resize": f"{BASE_URL}/static/img/placesmap/{str(id)}.png",
                    "thumbnail": f"{BASE_URL}/static/img/placesmap/{str(id)}.png",
                }
            )
            return list_photo

        if video:
            list_photo.append(
                {
                    "resize": f"https://i.ytimg.com/vi/{video}/maxresdefault.jpg",
                    "thumbnail": f"https://i.ytimg.com/vi/{video}/hqdefault.jpg",
                }
            )
            return list_photo

        list_photo.append(
            {
                "resize": f"{BASE_URL}/static/img/posts/resize/goldfishnet.jpg",
                "thumbnail": f"{BASE_URL}/static/img/posts/thumbnail/goldfishnet.jpg",
            }
        )
        return list_photo

    except Exception as e:
        # tg.sendMessage(
        #     "346777365", "GoldFishNet Error in get_images places: " + str(e), ""
        # )
        return []
