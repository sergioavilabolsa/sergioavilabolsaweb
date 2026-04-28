"""
Generates a TradingView-style dark candlestick chart using yfinance + mplfinance.
Dark background #131722, green #26a69a, red #ef5350 — identical colour scheme
to the TradingView screenshot provided by the user.
"""

import os
import warnings
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Agg')  # headless rendering for GitHub Actions

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mplfinance as mpf
import yfinance as yf
import pandas as pd
import requests
import urllib3

warnings.filterwarnings('ignore')

# TradingView dark palette
TV_BG       = '#131722'
TV_PANEL    = '#1e222d'
TV_GRID     = '#2a2e39'
TV_TEXT     = '#b2b5be'
TV_SUBTEXT  = '#787b86'
TV_GREEN    = '#26a69a'
TV_RED      = '#ef5350'
TV_VOLUME   = '#363a45'
TV_VOL_UP   = '#26a69a'
TV_VOL_DN   = '#ef5350'


def _build_style() -> dict:
    mc = mpf.make_marketcolors(
        up=TV_GREEN, down=TV_RED,
        edge={'up': TV_GREEN, 'down': TV_RED},
        wick={'up': TV_GREEN, 'down': TV_RED},
        volume={'up': TV_VOL_UP, 'down': TV_VOL_DN},
        alpha=0.9,
    )
    return mpf.make_mpf_style(
        marketcolors=mc,
        facecolor=TV_BG,
        figcolor=TV_BG,
        gridcolor=TV_GRID,
        gridstyle='-',
        gridaxis='both',
        y_on_right=True,
        rc={
            'axes.labelcolor':    TV_TEXT,
            'axes.edgecolor':     TV_GRID,
            'xtick.color':        TV_SUBTEXT,
            'ytick.color':        TV_SUBTEXT,
            'xtick.labelsize':    9,
            'ytick.labelsize':    9,
            'font.family':        'DejaVu Sans',
            'font.size':          9,
            'figure.facecolor':   TV_BG,
            'axes.facecolor':     TV_BG,
            'savefig.facecolor':  TV_BG,
            'savefig.edgecolor':  TV_BG,
        },
    )


def _resolve_ticker(ticker: str) -> tuple[str, str]:
    """Return (yf_ticker, display_name). Normalise common formats."""
    ticker = ticker.strip().upper()
    # Map common Perplexity-returned names to Yahoo Finance tickers
    alias = {
        'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'GOLD': 'GC=F',
        'OIL': 'CL=F', 'WTI': 'CL=F', 'BRENT': 'BZ=F',
        'IBEX': '^IBEX', 'IBEX35': '^IBEX', 'SP500': '^GSPC',
        'SPX': '^GSPC', 'NDX': '^NDX', 'NASDAQ': '^NDX',
        'DJI': '^DJI', 'DAX': '^GDAXI', 'EURUSD': 'EURUSD=X',
    }
    yf_ticker = alias.get(ticker, ticker)
    return yf_ticker, ticker


def generate_chart(
    ticker: str,
    asset_name: str = '',
    days: int = 90,
    output_dir: str = '/tmp',
) -> str:
    """
    Download OHLCV data for `ticker` and save a TradingView-style PNG.
    Returns the path of the saved image.
    """
    yf_ticker, display = _resolve_ticker(ticker)

    end   = datetime.utcnow()
    start = end - timedelta(days=days)
    
    urllib3.disable_warnings()
    session = requests.Session()
    session.verify = False

    df = yf.download(
        yf_ticker,
        start=start.strftime('%Y-%m-%d'),
        end=(end + timedelta(days=1)).strftime('%Y-%m-%d'),
        interval='1d',
        progress=False,
        auto_adjust=True,
        session=session,
    )

    if df.empty:
        raise ValueError(f"No data returned for ticker '{yf_ticker}'")

    # Keep only OHLCV columns
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
    df.index = pd.to_datetime(df.index)

    style = _build_style()
    label = asset_name or display

    # Safe filename
    safe_ticker = yf_ticker.replace('/', '_').replace('^', '').replace('=', '_').replace('-', '_')
    out_path = os.path.join(output_dir, f'chart_{safe_ticker}.png')

    fig, axes = mpf.plot(
        df,
        type='candle',
        style=style,
        volume=True,
        figsize=(12, 6.75),    # 16:9 aspect ratio
        panel_ratios=(3, 1),
        tight_layout=True,
        returnfig=True,
        warn_too_much_data=9999,
    )

    # Title
    ax_main = axes[0]
    last_close = float(df['Close'].iloc[-1])
    prev_close = float(df['Close'].iloc[-2]) if len(df) > 1 else last_close
    pct_change = (last_close - prev_close) / prev_close * 100
    color = TV_GREEN if pct_change >= 0 else TV_RED
    sign  = '+' if pct_change >= 0 else ''

    ax_main.set_title(
        f'{label}   {last_close:.2f}   {sign}{pct_change:.2f}%',
        color=TV_TEXT,
        fontsize=11,
        fontweight='bold',
        loc='left',
        pad=8,
    )

    # Watermark — small, subtle, bottom-right
    fig.text(
        0.99, 0.01,
        'sergioavilabolsa.com',
        ha='right', va='bottom',
        fontsize=7, color=TV_SUBTEXT, alpha=0.6,
    )

    # Remove spines
    for ax in axes:
        for spine in ax.spines.values():
            spine.set_edgecolor(TV_GRID)

    fig.savefig(out_path, dpi=150, bbox_inches='tight',
                facecolor=TV_BG, edgecolor='none')
    plt.close(fig)

    return out_path
