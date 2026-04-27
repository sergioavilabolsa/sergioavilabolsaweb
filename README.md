# sergioavilabolsa.com — Automatización de artículos con IA

Sistema de publicación automática de dos artículos diarios en WordPress usando
GitHub Actions + OpenAI GPT-4o + Perplexity Sonar Pro.

---

## Artículos generados

| Artículo | Hora Madrid (verano) | Hora Madrid (invierno) | Contenido |
|---|---|---|---|
| Mercados | 09:00 | 08:00 | Los 3 activos que dominan la sesión hoy |
| Acciones USA | 15:00 | 14:00 | Noticias de S&P 500 / Nasdaq 100 con más impacto hoy |

---

## Requisitos previos

### 1. WordPress

- WordPress 5.6 o superior
- Plugin SEO instalado: **Yoast SEO** (recomendado), Rank Math o All in One SEO
- REST API habilitada (está activa por defecto)

### 2. Contraseña de aplicación WordPress

1. Entra en WordPress Admin → **Usuarios → Tu perfil**
2. Baja hasta **Contraseñas de aplicación**
3. Escribe un nombre (ej: `GitHub Actions`) y haz clic en **Añadir contraseña**
4. Copia la contraseña generada (formato: `xxxx xxxx xxxx xxxx xxxx xxxx`)

### 3. API Keys necesarias

| Clave | Dónde conseguirla | Coste estimado |
|---|---|---|
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com/api-keys) | ~$0.01–0.05 por artículo |
| `PERPLEXITY_API_KEY` | [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api) | ~$0.005 por búsqueda |

> El coste total estimado es **menos de $0.10 por día** (dos artículos).

---

## Configuración de GitHub Secrets

Ve a tu repositorio en GitHub → **Settings → Secrets and variables → Actions → New repository secret**

Crea estos secrets:

| Secret | Valor de ejemplo |
|---|---|
| `OPENAI_API_KEY` | `sk-proj-...` |
| `PERPLEXITY_API_KEY` | `pplx-...` |
| `WP_URL` | `https://sergioavilabolsa.com` |
| `WP_USERNAME` | `sergio` |
| `WP_APP_PASSWORD` | `xxxx xxxx xxxx xxxx xxxx xxxx` |
| `WP_SEO_PLUGIN` | `yoast` (o `rankmath` o `aioseo`) |
| `WP_CATEGORY_MARKETS` | `Análisis de Mercados` |
| `WP_CATEGORY_US` | `Acciones USA` |

---

## Estructura del repositorio

```
.github/
  workflows/
    article_markets.yml      # Cron 07:00 UTC (09:00 CEST)
    article_us_stocks.yml    # Cron 13:00 UTC (15:00 CEST)
scripts/
  article_markets.py         # Artículo 1: top 3 activos del día
  article_us_stocks.py       # Artículo 2: acciones USA con más impacto
  chart_generator.py         # Gráfico estilo TradingView (dark theme)
  news_searcher.py            # Búsqueda de noticias con Perplexity
  wordpress_publisher.py     # Cliente WordPress REST API
  utils.py                   # Utilidades compartidas
requirements.txt
.env.example                 # Copia a .env para pruebas locales
```

---

## Prueba local

```bash
# Clona el repositorio
git clone https://github.com/sergioavilabolsa/sergioavilabolsaweb.git
cd sergioavilabolsaweb

# Instala dependencias
pip install -r requirements.txt

# Copia y rellena las variables de entorno
cp .env.example .env
# Edita .env con tus claves reales

# Prueba el artículo de mercados
python scripts/article_markets.py

# Prueba el artículo de acciones USA
python scripts/article_us_stocks.py
```

---

## Lanzamiento manual desde GitHub

Puedes lanzar cualquiera de los dos workflows manualmente:

1. Ve a **Actions** en tu repositorio de GitHub
2. Selecciona el workflow que quieras ejecutar
3. Haz clic en **Run workflow → Run workflow**

---

## Formato de los artículos generados

### Artículo 1 — Mercados (09:00h)

- **Intro** con la fecha del día
- **3 bullet points** con emojis (optimizados para Google Discover)
- **H2** descriptivo
- **3 análisis** de 120-180 palabras cada uno (un activo por sección)
- **Aviso legal** de carácter informativo
- **Imagen de portada**: gráfico dark-mode del activo más relevante
- **SEO**: H1, meta título, meta descripción, palabras clave

### Artículo 2 — Acciones USA (15:00h)

- **Intro** con la fecha del día
- **3 bullet points** con emojis
- **H2** descriptivo
- **5 a 8 acciones** con:
  - Noticia de hoy (máx. 50 palabras)
  - Análisis de impacto en cotización (máx. 100 palabras)
- **Aviso legal**
- **Imagen de portada**: gráfico dark-mode de la acción más relevante
- **SEO**: completo igual que artículo 1

---

## Notas sobre horario

GitHub Actions usa UTC. Los workflows están configurados así:

- `0 7 * * 1-5` → 09:00 CEST (verano) / 08:00 CET (invierno)
- `0 13 * * 1-5` → 15:00 CEST (verano) / 14:00 CET (invierno)

España cambia al horario de invierno el último domingo de octubre y vuelve al
de verano el último domingo de marzo. Durante esos ~5 meses los artículos se
publicarán 1 hora antes de lo indicado.

---

## Solución de problemas

**El workflow falla con "No data returned for ticker"**  
El modelo devolvió un ticker incorrecto. El script tiene un fallback automático
a `SPY` (artículo 1) o `QQQ` (artículo 2). Puedes ver el log en
Actions → el workflow → el paso "Publish article".

**El post se crea pero sin meta SEO**  
Verifica que el plugin Yoast/Rank Math esté activo y que el secret
`WP_SEO_PLUGIN` esté correctamente configurado (`yoast`, `rankmath` o `aioseo`).

**Error 401 en WordPress**  
La contraseña de aplicación es incorrecta o el usuario no tiene permisos de
autor/editor. Regenera la contraseña desde tu perfil de WordPress.

**Error de Perplexity API**  
Comprueba que `PERPLEXITY_API_KEY` sea válida y que tengas saldo en tu cuenta
de Perplexity ([perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)).
