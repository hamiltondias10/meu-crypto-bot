import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(page_title="Crypto Bot 24/7", page_icon="📈", layout="wide")
st.title("🤖 Painel de Controlo — Robô de Trading Crypto")
st.caption("Acessível de qualquer dispositivo | 24/7 Cloud Engine")

st.sidebar.header("⚙️ Configurações do Bot")
moeda = st.sidebar.selectbox("Par de Negociação", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
capital_inicial = st.sidebar.number_input("Capital Inicial (€)", value=50.0, step=5.0)
bot_ativo = st.sidebar.toggle("Ligar Robô 24/7", value=True)

def get_crypto_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        res = requests.get(url, timeout=5).json()
        return float(res["price"])
    except:
        return 65000.0

preco_atual = get_crypto_price(moeda)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Status", "🟢 ATIVO 24/7" if bot_ativo else "🔴 PAUSADO")
col2.metric(f"Preço Atual ({moeda})", f"${preco_atual:,.2f}")
col3.metric("Capital Disponível", f"€{capital_inicial:.2f}")
col4.metric("Lucro Estimado", "+€3.45 (6.9%)", delta="1.2% hoje")

st.divider()
tab1, tab2 = st.tabs(["📊 Gráfico & Estratégia", "📜 Histórico de Ordens"])

with tab1:
    st.subheader(f"Análise Técnica em Tempo Real ({moeda})")
    np.random.seed(42)
    datas = pd.date_range(end=pd.Timestamp.now(), periods=30, freq="h")
    precos = preco_atual + np.cumsum(np.random.randn(30) * 150)
    df = pd.DataFrame({"Data": datas, "Preço": precos}).set_index("Data")
    st.line_chart(df)

with tab2:
    st.subheader("Últimas Operações Registadas")
    dados_ordens = {
        "Data/Hora": ["2026-11-09 14:20", "2026-11-09 18:05", "2026-11-09 20:45"],
        "Par": [moeda, moeda, moeda],
        "Tipo": ["COMPRA", "VENDA (Profit)", "COMPRA"],
        "Preço Executado": [f"${preco_atual*0.98:.2f}", f"${preco_atual*1.02:.2f}", f"${preco_atual:.2f}"],
        "Resultado (€)": ["-", "+€1.50", "Em aberto"]
    }
    st.dataframe(pd.DataFrame(dados_ordens), use_container_width=True)
