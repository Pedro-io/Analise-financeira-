import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar dados de um arquivo CSV
def load_data(filename):
  try:
    df = pd.read_csv(filename)
    return df
  except FileNotFoundError:
    return pd.DataFrame(columns=['Data', 'Descrição', 'Valor', 'Tipo'])

# Função para salvar dados em um arquivo CSV
def save_data(df, filename):
  df.to_csv(filename, index=False)

# Carrega dados existentes ou inicia um novo DataFrame
df = load_data('financas.csv')

# Título da página
st.title('Gerenciador Financeiro Pessoal')

# Formulário para adicionar novas entradas
with st.form('add_entry'):
  data = st.date_input('Data')
  descricao = st.text_input('Descrição')
  valor = st.number_input('Valor', value=0.00, format="%.2f")
  tipo = st.selectbox('Tipo', ['Entrada', 'Saída'])
  submitted = st.form_submit_button('Adicionar')
  if submitted:
    new_entry = pd.DataFrame([[data, descricao, valor, tipo]], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df, 'financas.csv')

# Visualização dos dados
st.header('Transações:')
st.dataframe(df)

# Análise de dados
st.header('Análise de Gastos:')
if not df.empty:
  df['Valor'] = df['Valor'].astype(float)
  df['Tipo'] = df['Tipo'].astype('category')
  gastos_por_tipo = df.groupby('Tipo')['Valor'].sum()
  st.bar_chart(gastos_por_tipo)
  st.pyplot(plt.figure(figsize=(10, 5)))
  plt.title('Total de Entradas e Saídas')
  plt.bar(['Entradas', 'Saídas'], [gastos_por_tipo['Entrada'], gastos_por_tipo['Saída']])
  plt.show()