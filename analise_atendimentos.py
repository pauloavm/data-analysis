import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Análise de atendimentos.')

with st.container():
    st.subheader('Análise dos atendimentos.')
    st.write('Estudo dos atendimentos da Barbearia desde sua \
             abertura (Março de 2019) até Fevereiro de 2024')
    st.write('Informações dos atendimentos do salão:')

st.write('---')

with st.container():
    # Carregar dados
    df = pd.read_csv('agenda_servicos.csv')

    # Verificar e imprimir as colunas do DataFrame
    st.write("Colunas do DataFrame:", df.columns.tolist())

    # Distribuição dos Serviços por Dia da Semana
    st.header('Distribuição dos Serviços por Dia da Semana')
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='Dia_Semana', ax=ax)
    st.pyplot(fig)

    # Horários mais Comuns para os Serviços
    st.header('Horários mais Comuns para os Serviços')
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='Horarios', ax=ax)
    st.pyplot(fig)

    # Valores dos Serviços
    st.header('Distribuição dos Valores dos Serviços')
    fig, ax = plt.subplots()
    try:
        sns.boxplot(data=df, x='Valor', ax=ax)
        st.pyplot(fig)
    except ValueError as e:
        st.error(f"Erro: {e}")

    # Formas de Pagamento Utilizadas
    st.header('Formas de Pagamento Utilizadas')
    fig, ax = plt.subplots()
    df['Forma_Pgto'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

    # Status dos Serviços
    st.header('Status dos Serviços')
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='Status', ax=ax)
    st.pyplot(fig)

    # Agendamentos ao Longo do Tempo
    st.header('Agendamentos ao Longo do Tempo')
    df['Data_agendamento'] = pd.to_datetime(df['Data_agendamento'])
    fig, ax = plt.subplots()
    df.groupby(df['Data_agendamento'].dt.date).size().plot(kind='line', ax=ax)
    st.pyplot(fig)
