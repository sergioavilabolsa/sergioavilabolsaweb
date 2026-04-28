"""
Artículo 2 — Acciones USA (S&P 500 / Nasdaq 100) con más impacto HOY
Se publica a las 15:00h Madrid (lunes-viernes).
Ejecutado por GitHub Actions (.github/workflows/article_us_stocks.yml).
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from utils import extract_tag, format_date_spanish, today_str
from news_searcher import search_us_stocks_news
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
Hoy es {today}. Con las siguientes noticias de acciones americanas del S&P 500 y Nasdaq 100 \
publicadas HOY:

{news}

Redacta un artículo de blog profesional sobre las acciones americanas con más impacto en \
bolsa HOY. Sigue EXACTAMENTE este formato, usando las etiquetas XML indicadas:

<H1>Título entre 20 y 70 caracteres</H1>
<META_TITULO>Meta título entre 50 y 60 caracteres</META_TITULO>
<H2>Subtítulo único para todo el artículo, hasta 70 caracteres</H2>
<META_DESC>Meta descripción entre 140 y 160 caracteres optimizada para Google News</META_DESC>
<BULLETS>
- [bullet point 1 — dato o insight clave, muy profesional, sin emojis]
- [bullet point 2 — dato o insight clave, muy profesional, sin emojis]
- [bullet point 3 — dato o insight clave, muy profesional, sin emojis]
</BULLETS>
<PALABRAS_CLAVE>palabra1, palabra2, ... (mínimo 8 palabras clave separadas por comas)</PALABRAS_CLAVE>
<TICKER_PRINCIPAL>ticker Yahoo Finance del activo más relevante del artículo (ej: NVDA, AAPL)</TICKER_PRINCIPAL>

Luego, para CADA acción relevante de HOY, usa este bloque (repite N veces, entre 5 y 8 acciones):

<ACCION_NOMBRE>Nombre completo de la empresa</ACCION_NOMBRE>
<ACCION_TICKER>Ticker (ej: NVDA)</ACCION_TICKER>
<ACCION_NOTICIA>
Párrafo corto de máximo 50 palabras. Descripción objetiva e institucional de la noticia de hoy. Qué ha pasado exactamente. Sin copiar frases de fuentes publicadas.
</ACCION_NOTICIA>
<ACCION_ANALISIS>
Análisis original en dos párrafos cortos (estilo informe de IG, centrado en macro/fundamentales).
Párrafo 1: Impacto en el modelo de negocio, valoraciones o sentimiento del inversor.
Párrafo 2: Riesgos y perspectivas a corto plazo ante este evento.
</ACCION_ANALISIS>

<FIN_ACCIONES>

IMPORTANTE:
- H1, H2 y bullets optimizados para viralizarse en Google News y Google Discover.
- El H1 debe ser atractivo y mencionar 2-3 empresas clave.
- Cada texto debe ser 100% original, nunca copiar frases de internet.
- TICKER_PRINCIPAL: el de la acción con mayor impacto del día.
- Cierra siempre con la etiqueta <FIN_ACCIONES> tras el último bloque de acción.
"""


def parse_article(content: str) -> dict:
    base = {
        'h1':               extract_tag(content, 'H1'),
        'meta_titulo':      extract_tag(content, 'META_TITULO'),
        'h2':               extract_tag(content, 'H2'),
        'meta_desc':        extract_tag(content, 'META_DESC'),
        'bullets':          extract_tag(content, 'BULLETS'),
        'keywords':         extract_tag(content, 'PALABRAS_CLAVE'),
        'ticker_principal': extract_tag(content, 'TICKER_PRINCIPAL'),
    }

    # Parse repeating action blocks
    import re
    nombre_list   = re.findall(r'<ACCION_NOMBRE>(.*?)</ACCION_NOMBRE>',   content, re.DOTALL)
    ticker_list   = re.findall(r'<ACCION_TICKER>(.*?)</ACCION_TICKER>',   content, re.DOTALL)
    noticia_list  = re.findall(r'<ACCION_NOTICIA>(.*?)</ACCION_NOTICIA>', content, re.DOTALL)
    analisis_list = re.findall(r'<ACCION_ANALISIS>(.*?)</ACCION_ANALISIS>', content, re.DOTALL)

    acciones = []
    for i in range(len(nombre_list)):
        acciones.append({
            'nombre':   nombre_list[i].strip()   if i < len(nombre_list)   else '',
            'ticker':   ticker_list[i].strip()   if i < len(ticker_list)   else '',
            'noticia':  noticia_list[i].strip()  if i < len(noticia_list)  else '',
            'analisis': analisis_list[i].strip() if i < len(analisis_list) else '',
        })

    base['acciones'] = acciones
    return base


def build_html_content(parsed: dict) -> str:
    today = format_date_spanish()

    bullets_raw = parsed['bullets']
    bullets_lines = [l.strip() for l in bullets_raw.split('\n') if l.strip()]
    bullets_html = '\n'.join(f'<li>{b}</li>' for b in bullets_lines)

    acciones_html = ''
    for acc in parsed['acciones']:
        noticia  = acc['noticia'].replace('\n', ' ').strip()
        analisis = acc['analisis'].replace('\n', ' ').strip()
        acciones_html += f"""\

<!-- wp:heading {{"level":3}} -->
<h3>{acc['nombre']} ({acc['ticker']})</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Noticia:</strong> {noticia}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Análisis:</strong> {analisis}</p>
<!-- /wp:paragraph -->
"""

    return f"""\
<!-- wp:paragraph -->
<p><em>Análisis de bolsa americana — {today}</em></p>
<!-- /wp:paragraph -->

<!-- wp:list {{"ordered":false}} -->
<ul>
{bullets_html}
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>{parsed['h2']}</h2>
<!-- /wp:heading -->
{acciones_html}
<!-- wp:paragraph -->
<p><em>Este análisis tiene carácter informativo y no constituye asesoramiento de inversión. \
Invertir en bolsa conlleva riesgos. Consulta siempre con un asesor financiero antes de tomar \
decisiones de inversión.</em></p>
<!-- /wp:paragraph -->
"""


def run():
    today = format_date_spanish()
    print(f"[us_stocks] Generando artículo de acciones USA para {today}")

    # 1. Buscar noticias en tiempo real
    print("[us_stocks] Buscando noticias de acciones USA con Perplexity...")
    news_content = search_us_stocks_news()
    print(f"[us_stocks] Noticias obtenidas ({len(news_content)} chars)")

    # 2. Generar artículo con GPT-4o
    print("[us_stocks] Generando artículo con GPT-4o...")
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user',   'content': ARTICLE_PROMPT_TEMPLATE.format(
                today=today, news=news_content
            )},
        ],
        temperature=0.7,
        max_tokens=4000,
    )
    article_raw = response.choices[0].message.content
    print(f"[us_stocks] Artículo generado ({len(article_raw)} chars)")

    # 3. Parsear respuesta
    parsed = parse_article(article_raw)

    if not parsed['acciones']:
        raise ValueError("No se encontraron bloques <ACCION_*> en la respuesta del modelo.")

    ticker = parsed['ticker_principal'] or parsed['acciones'][0]['ticker'] or 'SPY'
    asset_name = parsed['acciones'][0]['nombre'] or ticker

    # 4. Generar gráfico
    print(f"[us_stocks] Generando gráfico para {ticker}...")
    try:
        chart_path = generate_chart(ticker=ticker, asset_name=asset_name)
        print(f"[us_stocks] Gráfico guardado en {chart_path}")
    except Exception as e:
        print(f"[us_stocks] Error generando gráfico para {ticker}: {e}. Usando QQQ...")
        chart_path = generate_chart(ticker='QQQ', asset_name='Nasdaq 100 ETF')

    # 5. Publicar en WordPress
    print("[us_stocks] Publicando en WordPress...")
    publisher = WordPressPublisher()

    image_id = publisher.upload_image(
        file_path=chart_path,
        title=f'{asset_name} — análisis técnico {today_str()}',
        alt_text=f'Gráfico análisis técnico {asset_name} {today_str()}',
    )

    keywords = parsed['keywords']
    tag_names = [k.strip() for k in keywords.split(',')[:5] if k.strip()]

    post_id = publisher.create_post(
        title=parsed['h1'],
        content=build_html_content(parsed),
        featured_image_id=image_id,
        meta_title=parsed['meta_titulo'],
        meta_desc=parsed['meta_desc'],
        keywords=keywords,
        category_name=os.environ.get('WP_CATEGORY_US', 'Acciones USA'),
        tag_names=tag_names,
    )
    print(f"[us_stocks] Artículo publicado correctamente. Post ID: {post_id}")


if __name__ == '__main__':
    run()
