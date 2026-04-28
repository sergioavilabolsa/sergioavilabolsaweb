import os
import requests
import urllib3
urllib3.disable_warnings()
from utils import format_date_spanish, now_madrid


def _perplexity_search(system_prompt: str, user_query: str, recency: str = 'day') -> str:
    """
    Call Perplexity sonar-pro to search real-time web content.
    recency: 'hour', 'day', 'week', 'month', 'year'
    """
    api_key = os.environ['PERPLEXITY_API_KEY']

    payload = {
        'model': 'sonar-pro',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user',   'content': user_query},
        ],
        'search_recency_filter': recency,
        'return_citations': False,
        'temperature': 0.2,
    }

    resp = requests.post(
        'https://api.perplexity.ai/chat/completions',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        json=payload,
        timeout=60,
        verify=False,
    )
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']


def search_top_market_assets() -> str:
    """
    Find the 3 most relevant financial assets dominating market narrative TODAY.
    Returns raw research text for use in GPT-4 article generation.
    """
    today = format_date_spanish()

    system_prompt = (
        "Eres un analista financiero experto con acceso a noticias en tiempo real. "
        "Solo reportas noticias y movimientos de mercado de HOY. "
        "Ignora completamente cualquier noticia o movimiento de días anteriores. "
        "Citas fuentes verificadas: Bloomberg, Reuters, Financial Times, Expansión, Cinco Días, El Economista, Investing.com."
    )

    user_query = (
        f"Hoy es {today}. "
        "Identifica los 3 activos financieros (acciones, índices, materias primas, criptomonedas o divisas) "
        "que están dominando HOY la narrativa de los mercados financieros a nivel global y en España. "
        "Deben ser los activos que más están moviendo la prensa financiera, los foros de inversión y las redes sociales DE HOY. "
        "Para cada activo indica: "
        "1) Nombre completo y ticker bursátil (formato Yahoo Finance). "
        "2) Las noticias o situaciones concretas de HOY que están moviendo ese activo. "
        "3) Movimiento de precio de HOY (subida/bajada y porcentaje si está disponible). "
        "4) Por qué está generando tanto interés hoy entre inversores y prensa. "
        "Sé muy específico y concreto. Incluye datos de hoy solamente."
    )

    return _perplexity_search(system_prompt, user_query, recency='day')


def search_us_stocks_news() -> str:
    """
    Find US stocks (S&P 500 / Nasdaq 100) with most market-moving news TODAY.
    Returns raw research text for use in GPT-4 article generation.
    """
    today = format_date_spanish()

    system_prompt = (
        "Eres un analista financiero experto especializado en bolsa americana. "
        "Solo reportas noticias publicadas HOY. Ignora cualquier noticia de días anteriores. "
        "Citas fuentes verificadas nacionales e internacionales: Bloomberg, Reuters, CNBC, MarketWatch, "
        "WSJ, Financial Times, Barron's, Expansión, Cinco Días, El Economista."
    )

    user_query = (
        f"Hoy es {today}. "
        "Búscame las noticias publicadas HOY sobre acciones del S&P 500 o Nasdaq 100 que más impacto "
        "están teniendo en bolsa. Solo noticias de hoy, no de días anteriores. "
        "Para cada acción relevante: "
        "1) Nombre de la empresa y ticker (ej: AAPL, NVDA, TSLA). "
        "2) Descripción breve de la noticia de hoy (qué pasó exactamente). "
        "3) Movimiento de precio de hoy (porcentaje de subida/bajada). "
        "4) Fuente verificada donde se publicó la noticia. "
        "Incluye entre 5 y 8 acciones con noticias relevantes de hoy. "
        "Prioriza las que tengan mayor movimiento de precio o más cobertura mediática de hoy."
    )

    return _perplexity_search(system_prompt, user_query, recency='day')
