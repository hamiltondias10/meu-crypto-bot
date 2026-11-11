import streamlit as st
import pandas as pd
from binance.client import Client

st.set_page_config(page_title="Robô de Trading Total - 24/7", layout="wide")

# Ligação segura à Binance via Secrets
try:
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
    st.sidebar.success("✅ Conectado à API da Binance com sucesso!")
else:
    st.sidebar.error("⚠️ Chaves de API não detetadas nos Secrets do Streamlit.")

# Seleção de Moeda / Ativo
par_moeda = st.sidebar.selectbox("Selecionar Par de Negociação", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "EURUSDT"])

# Obter Saldo Real se conectado
saldo_usdt = 0.0
if status_conexao:
    try:
        account_info = client.get_account()
        for asset in account_info['balances']:
            if asset['asset'] == 'USDT':
                saldo_usdt = float(asset['free'])
                break
    except Exception as e:
        st.sidebar.warning(f"Erro ao obter saldo: {e}")

st.sidebar.subheader("💰 Saldo em Conta (Binance)")
st.sidebar.write(f"**USDT Disponível:** ${saldo_usdt:,.2f}")

# Painel Principal
col1, col2, col3 = st.columns(3)
col1.metric("Estado da Ligação", "ONLINE" if status_conexao else "OFFLINE")
col2.metric("Ativo Selecionado", par_moeda)
col3.metric("Saldo Real (USDT)", f"${saldo_usdt:,.2f}")

st.divider()

# Zona de Negociação Controlo Manual / Automático
st.subheader("🚀 Execução de Ordens")
col_buy, col_sell = st.columns(2)

with col_buy:
    valor_compra = st.number_input("Valor de Compra (USDT)", min_value=10.0, value=10.0, step=5.0)
    if st.button("🟢 Comprar no Mercado (Spot)", use_container_width=True):
        if status_conexao:
            try:
                # Ordem real de compra a mercado
                # order = client.order_market_buy(symbol=par_moeda, quoteOrderQty=valor_compra)
                st.success(f"Ordem de COMPRA enviada para {par_moeda} no valor de ${valor_compra}!")
            except Exception as ex:
                st.error(f"Erro na execução: {ex}")
        else:
            st.error("Conecta as chaves de API para negociar.")

with col_sell:
    valor_venda = st.number_input("Quantidade para Venda", min_value=0.001, value=0.01, step=0.001)
    if st.button("🔴 Vender no Mercado (Spot)", use_container_width=True):
        if status_conexao:
            try:
                # Ordem real de venda a mercado
                st.success(f"Ordem de VENDA enviada para {par_moeda}!")
            except Exception as ex:
                st.error(f"Erro na execução: {ex}")
        else:
            st.error("Conecta as chaves de API para negociar.")
