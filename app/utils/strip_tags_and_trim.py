import re
import html as html_lib


def strip_tags_and_trim(html: str, max_length: int = 150) -> str:
    # Декодуємо HTML-ентіті (&nbsp;, &mdash;, &amp; тощо)
    html = html_lib.unescape(html or "")

    # Видаляємо всі HTML-теги
    clean_text = re.sub(r"<[^>]+>", "", html)

    # Замінюємо багато пробілів на один і обрізаємо
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    # Обрізаємо текст і додаємо "..." якщо потрібно
    return (
        clean_text[:max_length] + "..." if len(clean_text) > max_length else clean_text
    )
