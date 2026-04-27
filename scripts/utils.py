import re
from datetime import datetime
import pytz

MADRID_TZ = pytz.timezone('Europe/Madrid')

MONTH_NAMES_ES = {
    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
}

WEEKDAY_NAMES_ES = {
    0: 'lunes', 1: 'martes', 2: 'miércoles', 3: 'jueves',
    4: 'viernes', 5: 'sábado', 6: 'domingo'
}


def now_madrid() -> datetime:
    return datetime.now(MADRID_TZ)


def format_date_spanish(date: datetime = None) -> str:
    if date is None:
        date = now_madrid()
    day = date.day
    weekday = WEEKDAY_NAMES_ES[date.weekday()]
    month = MONTH_NAMES_ES[date.month]
    year = date.year
    return f"{weekday}, {day} de {month} de {year}"


def today_str() -> str:
    return now_madrid().strftime('%Y-%m-%d')


def extract_tag(content: str, tag: str) -> str:
    """Extract content between XML-style tags."""
    pattern = rf'<{re.escape(tag)}>(.*?)</{re.escape(tag)}>'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ''


def clean_text(text: str) -> str:
    """Remove extra whitespace and normalize line breaks."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def slug_from_title(title: str) -> str:
    """Generate URL slug from a title."""
    import unicodedata
    title = unicodedata.normalize('NFKD', title)
    title = title.encode('ascii', 'ignore').decode('ascii')
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    title = re.sub(r'[\s_]+', '-', title)
    title = re.sub(r'-+', '-', title)
    return title.strip('-')
