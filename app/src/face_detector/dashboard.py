import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Conexão com o banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="controle_acesso_dee"
    )

# Últimos logs
def buscar_logs(limit=20):
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT log_acesso.id, usuarios.nome, usuarios.tipo, log_acesso.autorizado, log_acesso.timestamp
        FROM log_acesso
        LEFT JOIN usuarios ON log_acesso.usuario_id = usuarios.id
        ORDER BY log_acesso.timestamp DESC
        LIMIT %s
    """, (limit,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(resultados)

# Pessoas atualmente no DEE
def usuarios_presentes():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.id, u.nome, u.tipo, MAX(l.timestamp) as ultima_entrada
        FROM usuarios u
        JOIN log_acesso l ON u.id = l.usuario_id
        WHERE l.autorizado = TRUE
        GROUP BY u.id
        HAVING ultima_entrada >= (
            SELECT MAX(l2.timestamp)
            FROM log_acesso l2
            WHERE l2.usuario_id = u.id AND l2.autorizado = FALSE
        ) OR NOT EXISTS (
            SELECT 1
            FROM log_acesso l2
            WHERE l2.usuario_id = u.id AND l2.autorizado = FALSE
        )
        ORDER BY ultima_entrada DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(resultados)

# Frequência mensal por usuário
def frequencia_mensal():
    conn = conectar_banco()
    query = """
        SELECT u.nome, COUNT(*) as total_acessos,
               DATE_FORMAT(l.timestamp, '%Y-%m') as mes
        FROM log_acesso l
        JOIN usuarios u ON l.usuario_id = u.id
        WHERE l.autorizado = TRUE
        GROUP BY u.nome, mes
        ORDER BY mes DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Horário de pico de acesso
def horarios_pico():
    conn = conectar_banco()
    query = """
        SELECT HOUR(timestamp) as hora, COUNT(*) as acessos
        FROM log_acesso
        WHERE autorizado = TRUE
        GROUP BY hora
        ORDER BY hora
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Cadastros próximos a vencer
def cadastros_vencendo():
    conn = conectar_banco()
    query = """
        SELECT nome, tipo, cadastro_valido_ate
        FROM usuarios
        WHERE cadastro_valido_ate <= CURDATE() + INTERVAL 30 DAY
        ORDER BY cadastro_valido_ate ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Comportamento por tipo
def acessos_por_tipo():
    conn = conectar_banco()
    query = """
        SELECT u.tipo, COUNT(*) as acessos
        FROM log_acesso l
        JOIN usuarios u ON l.usuario_id = u.id
        WHERE l.autorizado = TRUE
        GROUP BY u.tipo
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Interface
st.set_page_config(page_title="Painel de Acesso - DEE", layout="wide")
st.title("🔐 Painel de Acesso - DEE/UFPE")
st.markdown("Este painel mostra os acessos mais recentes e as pessoas atualmente no local.")

aba = st.sidebar.radio("Navegação", ["Dashboard Principal", "Frequência Mensal", "Horários de Pico", "Cadastros a Vencer", "Acessos por Tipo"])

if aba == "Dashboard Principal":
    st.subheader("📋 Últimos registros de acesso")
    logs_df = buscar_logs()
    if not logs_df.empty:
        logs_df['timestamp'] = logs_df['timestamp'].apply(lambda x: x.strftime('%d/%m/%Y %H:%M:%S'))
        logs_df['autorizado'] = logs_df['autorizado'].map({1: '✅ Autorizado', 0: '❌ Negado'})
        st.dataframe(logs_df.rename(columns={
            'nome': 'Nome', 'tipo': 'Tipo', 'autorizado': 'Status', 'timestamp': 'Data/Hora'
        }), use_container_width=True)
    else:
        st.info("Nenhum acesso registrado ainda.")

    st.subheader("🏢 Pessoas atualmente no DEE")
    presentes_df = usuarios_presentes()
    if not presentes_df.empty:
        presentes_df['ultima_entrada'] = presentes_df['ultima_entrada'].apply(lambda x: x.strftime('%d/%m/%Y %H:%M:%S'))
        st.dataframe(presentes_df.rename(columns={
            'nome': 'Nome', 'tipo': 'Tipo', 'ultima_entrada': 'Última Entrada'
        }), use_container_width=True)
    else:
        st.success("Nenhuma pessoa no local no momento.")

elif aba == "Frequência Mensal":
    st.subheader("📅 Frequência por usuário por mês")
    df = frequencia_mensal()
    st.dataframe(df, use_container_width=True)

elif aba == "Horários de Pico":
    st.subheader("⏰ Horário de pico de acessos")
    df = horarios_pico()
    st.bar_chart(df.set_index('hora'))

elif aba == "Cadastros a Vencer":
    st.subheader("📆 Cadastros vencendo em até 30 dias")
    df = cadastros_vencendo()
    st.dataframe(df.rename(columns={
        'nome': 'Nome', 'tipo': 'Tipo', 'cadastro_valido_ate': 'Validade'
    }), use_container_width=True)

elif aba == "Acessos por Tipo":
    st.subheader("📈 Comportamento de acesso por tipo de usuário")
    df = acessos_por_tipo()
    st.bar_chart(df.set_index('tipo'))

st.markdown("---")
st.caption("Desenvolvido como projeto interdisciplinar para as disciplinas de Banco de Dados e Inteligência Artificial – UFPE")
