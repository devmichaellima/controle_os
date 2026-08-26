import pandas as pd 

# LEITURA DO ARQUIVO EXCEL
df = pd.read_excel("relatorio_jef.xlsx")

# ----------------------------------------------
# SEPARA O CREDENCIADO E A EMPRESA

df[['Empresa', 'Credenciado']] = df['Colaborador'].str.split(' - ', n=1, expand=True)

# ----------------------------------------------
# SELECIONA AS COLUNAS RELEVANTES

colunas_selecionadas = ['Identificador da OS', 'Empresa', 'Credenciado', 'Estado', 'Nome do cliente']

df = df[colunas_selecionadas]

# ----------------------------------------------
# FORMATA O TEXTO DAS COLUNAS

df['Estado'] = df['Estado'].replace({'São Paulo': 'SP'})
df['Empresa'] = df['Empresa'].astype(str).str.title()
df['Credenciado'] = df['Credenciado'].astype(str).str.title()
df['Nome do cliente'] = df['Nome do cliente'].astype(str).str.title()

# ----------------------------------------------
# CONTAGEM DE ORDENS POR CREDENCIADO

df_contagem = (
    df[['Empresa', 'Credenciado']]
    .value_counts()
    .reset_index(name='Quantidade_OS')
)

# ----------------------------------------------
# CONTAGEM DE ORDENS POR EMPRESA

df_empresa = df['Empresa'].value_counts()

