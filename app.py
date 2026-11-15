import streamlit as st
import pandas as pd
from binance.client import Client

st.set_page_config(page_title="Robô de Trading Total - 24/7", layout="wide")

# Ligação segura à Binance via Secrets
trys:
    api_key = st.secrets["binance"]["api_key"]
    api_secret = st.secrets["binance"]["api_secret"]
    client = Client(api_key, api_secret)
    status_conexao = True
except Exception as e:
    status_conexao = False

st.title("🤖 Painel de Controlo — Robô de Trading Autónomo")

# Sidebar
st.sidebar.header("⚙️ Configurações da Conta")

if status_conexao:
    st.sidebar.success("Conectado à API da Binance com sucesso!")
else:
    st.sidebar.error("⚠️ Chaves de API não detetadas nos Secrets do Streamlit.")

# Seleção de Moeda / Ativo
par_moeda = st.sidebar.selectbox("Selecionar Par de Negociação", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

# Obter Saldo Real se conectado
saldo_usdt = 0.0
if status_conexao:
    try:
        conta = client.get_account()
        for ativo in conta['balances']:
            if ativo['asset'] == 'USDT':
                saldo_usdt = float(ativo['free'])
                break
    except Exception:
        saldo_usdt = 0.0

# Painel Principal de Estado
col1, col2, col3 = st.columns(3)
col1.metric("Estado da Ligação", "ONLINE" if status_conexao else "OFFLINE")
col2.metric("Ativo Selecionado", par_moeda)
col3.metric("Saldo Real (USDT)", f"${saldo_usdt:,.2f}")

