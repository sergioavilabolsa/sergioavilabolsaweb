"""
Artículo 1 — Los 3 activos que dominan el mercado HOY
Se publica a las 9:00h Madrid (lunes-viernes).
Ejecutado por GitHub Actions (.github/workflows/article_markets.yml).
"""

import os
import sys
from pathlib import Path

# Allow imports from scripts/ when run directly
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from utils import extract_tag, format_date_spanish, today_str
from news_searcher import search_top_market_assets
from chart_generator import generate_chart
from wordpress_publisher import WordPressPublisher


SYSTEM_PROMPT = """\
Eres Sergio Ávila, inversor experimentado y analista bursátil con más de 20 años en los \
mercados financieros (analista Senior en IG España, "Mejor cartera de inversión en Expansión 2020"). \
Escribes en español para audiencia hispana (España y Latinoamérica). \
Tu objetivo es empoderar al inversor con ideas accionables y gestión del riesgo. \
Tu estilo es institucional, claro, basado en datos objetivos, y centrado en el contexto macroeconómico, \
la liquidez y la psicología colectiva detrás de los precios. Estructuras los análisis en párrafos cortos y directos. \
Nunca copias frases ni párrafos de fuentes publicadas en internet. Siempre redactas con tu propia voz.\
"""

ARTICLE_PROMPT_TEMPLATE = """\
Hoy es {today}. Con las siguientes noticias y movimientos de mercado de HOY:

{news}

Redacta un artículo de blog profesional sobre los 3 activos que dominan la narrativa \
del mercado HOY. Sigue EXACTAMENTE este formato de respuesta, usando las etiquetas XML indicadas:

<H1>Título entre 20 y 70 caracteres</H1>
<META_TITULO>Meta título entre 50 y 60 caracteres</META_TITULO>
<H2>Subtítulo único para todo el artículo, hasta 70 caracteres</H2>
<META_DESC>Meta descripción entre 140 y 160 caracteres optimizada para Google News</META_DESC>
<BULLETS>
- [bullet point 1 — dato o insight clave, muy profesional, sin emojis]
- [bullet point 2 — dato o insight clave, muy profesional, sin emojis]
- [bullet point 3 — dato o insight clave, muy profesional, sin emojis]
</BULLETS>
<PALABRAS_CLAVE>palabra1, palabra2, palabra3, ... (mínimo 8 palabras clave separadas por comas)</PALABRAS_CLAVE>
<TICKER_PRINCIPAL>ticker Yahoo Finance del activo más relevante (ej: AAPL, ^IBEX, BTC-USD)</TICKER_PRINCIPAL>
<ACTIVO1_NOMBRE>Nombre completo del activo 1</ACTIVO1_NOMBRE>
<ACTIVO1_TICKER>Ticker Yahoo Finance del activo 1</ACTIVO1_TICKER>
<ACTIVO1_ANALISIS>
Análisis original de unos 3 párrafos cortos. Emula el estilo analítico, formal y macroeconómico de los informes institucionales (ej: IG). 
Estructura obligatoria:
Párrafo 1: Situación actual (qué ha pasado hoy, sin relleno).
Párrafo 2: Impacto macro o fundamental (por qué importa al ecosistema).
Párrafo 3: Perspectiva y riesgos (visión a corto plazo).
Sin copiar ninguna frase de fuentes publicadas.
</ACTIVO1_ANALISIS>
<ACTIVO2_NOMBRE>Nombre completo del activo 2</ACTIVO2_NOMBRE>
<ACTIVO2_TICKER>Ticker Yahoo Finance del activo 2</ACTIVO2_TICKER>
<ACTIVO2_ANALISIS>
Análisis original de unos 3 párrafos cortos. Mismo estilo y estructura que el activo 1.
</ACTIVO2_ANALISIS>
<ACTIVO3_NOMBRE>Nombre completo del activo 3</ACTIVO3_NOMBRE>
<ACTIVO3_TICKER>Ticker Yahoo Finance del activo 3</ACTIVO3_TICKER>
<ACTIVO3_ANALISIS>
Análisis original de unos 3 párrafos cortos. Mismo estilo y estructura que el activo 1.
</ACTIVO3_ANALISIS>

IMPORTANTE:
- El H1, H2 y bullets deben estar optimizados para viralizarse en Google News y Google Discover.
- Cada análisis debe ser 100% original, nunca copiar frases de internet.
- El TICKER_PRINCIPAL debe ser exactamente el formato Yahoo Finance (ej: ^GSPC, BTC-USD, NVDA).
"""


def build_html_content(parsed: dict) -> str:
    today = format_date_spanish()
    bullets_raw = parsed['bullets']
    bullets_lines = [
        line.strip()
        for line in bullets_raw.split('\n')
        if line.strip()
    ]
    bullets_html = '\n'.join(f'<li>{b}</li>' for b in bullets_lines)

    a1 = parsed['activo1_analisis'].replace('\n', ' ').strip()
    a2 = parsed['activo2_analisis'].replace('\n', ' ').strip()
    a3 = parsed['activo3_analisis'].replace('\n', ' ').strip()

    return f"""\
<!-- wp:paragraph -->
<p><em>Análisis de mercados — {today}</em></p>
<!-- /wp:paragraph -->

<!-- wp:list {{\"ordered\":false}} -->
<ul>
{bullets_html}
</ul>
<!-- /wp:list -->

<!-- wp:heading {{\"level\":2}} -->
<h2>{parsed['h2']}</h2>
<!-- /wp:heading -->

<!-- wp:heading {{\"level\":3}} -->
<h3>{parsed['activo1_nombre']}</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{a1}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{\"level\":3}} -->
<h3>{parsed['activo2_nombre']}</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{a2}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{\"level\":3}} -->
<h3>{parsed['activo3_nombre']}</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{a3}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><em>Este análisis tiene carácter informativo y no constituye asesoramiento de inversión. \
Invertir en bolsa conlleva riesgos. Consulta siempre con un asesor financiero antes de tomar \
decisiones de inversión.</em></p>
<!-- /wp:paragraph -->
"""


def parse_article(content: str) -> dict:
    return {
        'h1':               extract_tag(content, 'H1'),
        'meta_titulo':      extract_tag(content, 'META_TITULO'),
        'h2':               extract_tag(content, 'H2'),
        'meta_desc':        extract_tag(content, 'META_DESC'),
        'bullets':          extract_tag(content, 'BULLETS'),
        'keywords':         extract_tag(content, 'PALABRAS_CLAVE'),
        'ticker_principal': extract_tag(content, 'TICKER_PRINCIPAL'),
        'activo1_nombre':   extract_tag(content, 'ACTIVO1_NOMBRE'),
        'activo1_ticker':   extract_tag(content, 'ACTIVO1_TICKER'),
        'activo1_analisis': extract_tag(content, 'ACTIVO1_ANALISIS'),
        'activo2_nombre':   extract_tag(content, 'ACTIVO2_NOMBRE'),
        'activo2_ticker':   extract_tag(content, 'ACTIVO2_TICKER'),
        'activo2_analisis': extract_tag(content, 'ACTIVO2_ANALISIS'),
        'activo3_nombre':   extract_tag(content, 'ACTIVO3_NOMBRE'),
        'activo3_ticker':   extract_tag(content, 'ACTIVO3_TICKER'),
        'activo3_analisis': extract_tag(content, 'ACTIVO3_ANALISIS'),
    }


def run():
    today = format_date_spanish()
    print(f"[markets] Generando artículo de mercados para {today}")

    # 1. Buscar noticias en tiempo real
    print("[markets] Buscando activos relevantes con Perplexity...")
    news_content = search_top_market_assets()
    print(f"[markets] Noticias obtenidas ({len(news_content)} chars)")

    # 2. Generar artículo con GPT-4o
    print("[markets] Generando artículo con GPT-4o...")
    import httpx
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        http_client=httpx.Client(verify=False)
    )
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user',   'content': ARTICLE_PROMPT_TEMPLATE.format(
                today=today, news=news_content
            )},
        ],
        temperature=0.7,
        max_tokens=3500,
    )
    article_raw = response.choices[0].message.content
    print(f"[markets] Artículo generado ({len(article_raw)} chars)")

    # 3. Parsear respuesta
    parsed = parse_article(article_raw)

    # Validations
    missing = [k for k, v in parsed.items() if not v]
    if missing:
        print(f"[markets] ADVERTENCIA: campos vacíos: {missing}")

    ticker = parsed['ticker_principal'] or parsed['activo1_ticker'] or 'SPY'
    asset_name = parsed['activo1_nombre'] or ticker

    # 4. Generar gráfico
    print(f"[markets] Generando gráfico para {ticker}...")
    try:
        chart_path = generate_chart(ticker=ticker, asset_name=asset_name)
        print(f"[markets] Gráfico guardado en {chart_path}")
    except Exception as e:
        print(f"[markets] Error generando gráfico para {ticker}: {e}. Intentando SPY...")
        try:
            chart_path = generate_chart(ticker='SPY', asset_name='S&P 500 ETF')
        except Exception as e2:
            print(f"[markets] Error generando gráfico de SPY: {e2}. Se publicará sin gráfico.")
            chart_path = None

    # 5. Publicar en WordPress
    print("[markets] Publicando en WordPress...")
    publisher = WordPressPublisher()

    image_id = 0
    if chart_path:
        try:
            image_id = publisher.upload_image(
                file_path=chart_path,
                title=f'{asset_name} — análisis técnico {today_str()}',
                alt_text=f'Gráfico análisis técnico {asset_name} {today_str()}',
            )
        except Exception as e:
            print(f"Error subiendo imagen a WP: {e}")

    keywords = parsed['keywords']
    tag_names = [k.strip() for k in keywords.split(',')[:5] if k.strip()]

    post_id = publisher.create_post(
        title=parsed['h1'],
        content=build_html_content(parsed),
        featured_image_id=image_id,
        meta_title=parsed['meta_titulo'],
        meta_desc=parsed['meta_desc'],
        keywords=keywords,
        category_name=os.environ.get('WP_CATEGORY_MARKETS', 'Análisis de Mercados'),
        tag_names=tag_names,
    )
    print(f"[markets] Artículo publicado correctamente. Post ID: {post_id}")


if __name__ == '__main__':
    run()
