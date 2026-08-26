import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import numpy as np
import json
import io
import os

# ══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Painel de Ordens de Serviço",
    page_icon="📊",
    layout="wide",
)

# ══════════════════════════════════════════════════════════════
# CSS CUSTOMIZADO — TEMA CLARO (BRANCO + CINZA)
# ══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* ---------- Fundo geral ---------- */
    .stApp {
        background: #f5f6fa !important;
    }

    /* ---------- Forçar textos escuros em TODO o app ---------- */
    .stApp, .stApp * {
        color: #1f2937;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li,
    .stText, div[data-testid="stText"],
    div[data-testid="stCaptionContainer"],
    div[data-testid="stCaptionContainer"] * {
        color: #4b5563 !important;
    }
    label, .stSelectbox label, .stMultiSelect label,
    .stFileUploader label, .stTextInput label,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #374151 !important;
    }
    span[data-testid="stHeaderActionElements"] *,
    .stFileUploader section small,
    .stFileUploader div, .stFileUploader span,
    div[data-testid="stFileUploaderDropzone"] *,
    div[data-testid="stFileUploaderDropzoneInstructions"] *,
    div[data-testid="stFileUploaderDropzoneInstructions"] span,
    div[data-testid="stFileUploaderDropzoneInstructions"] div,
    button[data-testid="stBaseButton-secondary"] {
        color: #4b5563 !important;
    }
    p, span, div {
        color: inherit;
    }

    /* ---------- Cards de indicadores — tamanho fixo ---------- */
    /* Força colunas-pai a mesma altura */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        display: flex;
        flex-direction: column;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e4ea;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden;
        box-sizing: border-box;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] > div {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 24px rgba(0,0,0,0.10);
    }
    div[data-testid="stMetric"] label {
        color: #6b7280 !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1f2937 !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        color: #4b5563 !important;
    }

    /* ---------- Títulos ---------- */
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        overflow-y: auto !important;
        padding: 1.5rem 1rem;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar {
        width: 6px;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"]::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    section[data-testid="stSidebar"] * {
        color: #1f2937;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1f2937 !important;
    }
    section[data-testid="stSidebar"] label {
        color: #374151 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #4b5563 !important;
    }

    /* ---------- Multiselect / inputs ---------- */
    div[data-baseweb="select"] *,
    div[data-baseweb="input"] * {
        color: #1f2937 !important;
    }
    div[data-baseweb="popover"] * {
        color: #1f2937 !important;
    }

    /* Cards / Tags de itens selecionados nos filtros */
    [data-baseweb="tag"],
    span[data-baseweb="tag"],
    div[data-baseweb="tag"] {
        background-color: #1e293b !important;
    }
    [data-baseweb="tag"] *,
    span[data-baseweb="tag"] *,
    div[data-baseweb="tag"] *,
    [data-baseweb="tag"] span,
    [data-baseweb="tag"] div,
    [data-baseweb="tag"] svg,
    [data-baseweb="tag"] svg path,
    div[data-testid="stMultiSelect"] [data-baseweb="tag"] *,
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }


    /* ---------- Tabelas ---------- */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }

    /* ---------- Botões de download ---------- */
    .stDownloadButton > button {
        background: #ffffff !important;
        color: #1f2937 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        background: #f3f4f6 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
        transform: translateY(-2px) !important;
    }

    /* ---------- Botão normal (limpar upload) ---------- */
    button[kind="secondary"],
    .stButton > button {
        color: #1f2937 !important;
        border-color: #d1d5db !important;
    }

    /* ---------- Upload ---------- */
    div[data-testid="stFileUploader"] {
        background: #f9fafb;
        border: 2px dashed #d1d5db;
        border-radius: 14px;
        padding: 10px;
    }
    div[data-testid="stFileUploader"] * {
        color: #4b5563 !important;
    }

    /* ---------- Divider ---------- */
    hr {
        border-color: #e5e7eb !important;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #f3f4f6;
        border-radius: 10px 10px 0 0;
        color: #6b7280 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #1f2937 !important;
        border-bottom: 2px solid #1f2937;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ══════════════════════════════════════════════════════════════

def processar_arquivo(uploaded_file) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Aplica o algoritmo do app.py sobre o arquivo enviado."""
    df = pd.read_excel(uploaded_file)

    # Separa Empresa e Credenciado
    df[['Empresa', 'Credenciado']] = (
        df['Colaborador'].str.split(' - ', n=1, expand=True)
    )

    # Seleciona colunas relevantes
    colunas = [
        'Identificador da OS', 'Empresa', 'Credenciado',
        'Estado', 'Nome do cliente',
    ]
    df = df[colunas]

    # Formata texto
    df['Estado'] = df['Estado'].replace({'São Paulo': 'SP'})
    df['Empresa'] = df['Empresa'].astype(str).str.title()
    df['Credenciado'] = df['Credenciado'].astype(str).str.title()
    df['Nome do cliente'] = df['Nome do cliente'].astype(str).str.title()

    # Contagem por credenciado + empresa
    df_contagem = (
        df[['Empresa', 'Credenciado']]
        .value_counts()
        .reset_index(name='Quantidade_OS')
    )

    return df, df_contagem


def gerar_excel(df: pd.DataFrame, sheet_name: str = 'Dados') -> bytes:
    """Converte DataFrame em bytes Excel para download."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        header_fmt = workbook.add_format({
            'bold': True,
            'bg_color': '#1f2937',
            'font_color': '#ffffff',
            'border': 1,
        })
        for col_num, value in enumerate(df.columns):
            worksheet.write(0, col_num, value, header_fmt)
            col_width = max(len(str(value)), df[value].astype(str).str.len().max()) + 2
            worksheet.set_column(col_num, col_num, min(col_width, 40))
    return buffer.getvalue()


GEOJSON_URL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

@st.cache_data(ttl=3600)
def carregar_geojson(url: str):
    """Baixa e cacheia o GeoJSON dos estados do Brasil."""
    import urllib.request
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read().decode())


# ══════════════════════════════════════════════════════════════
# CABEÇALHO COM LOGO
# ══════════════════════════════════════════════════════════════

LOGO_PATH = os.path.join(os.path.dirname(__file__), "Technogym_Logo.svg.webp")

col_logo, col_title = st.columns([2, 6], vertical_alignment="center")
with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=240)
with col_title:
    st.markdown("## Painel de Ordens de Serviço")
    st.caption("Faça upload do relatório Excel para visualizar indicadores, tabelas e gráficos.")

st.divider()

# ══════════════════════════════════════════════════════════════
# SIDEBAR — UPLOAD DE ARQUIVO
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 📁 Upload")
    uploaded_file = st.file_uploader(
        "Envie o relatório (.xlsx)",
        type=["xlsx"],
        key="file_uploader",
    )
    if st.button("🗑️ Limpar Upload", use_container_width=True):
        if "file_uploader" in st.session_state:
            del st.session_state["file_uploader"]
        st.rerun()
    st.divider()

# ══════════════════════════════════════════════════════════════
# PROCESSAMENTO E EXIBIÇÃO
# ══════════════════════════════════════════════════════════════

if uploaded_file is not None:
    df, df_contagem = processar_arquivo(uploaded_file)

    # ----------------------------------------------------------
    # SIDEBAR — FILTROS
    # ----------------------------------------------------------
    with st.sidebar:
        st.markdown("### 🔎 Filtros")
        st.divider()

        # Filtro por Credenciado
        credenciados = sorted(df['Credenciado'].dropna().unique())
        filtro_credenciado = st.multiselect(
            "Credenciado",
            options=credenciados,
            default=[],
            placeholder="Todos os credenciados",
            key="filtro_credenciado",
        )

        # Filtro por Empresa
        empresas = sorted(df['Empresa'].dropna().unique())
        filtro_empresa = st.multiselect(
            "Empresa",
            options=empresas,
            default=[],
            placeholder="Todas as empresas",
            key="filtro_empresa",
        )

        # Filtro por Estado
        estados = sorted(df['Estado'].dropna().unique())
        filtro_estado = st.multiselect(
            "Estado",
            options=estados,
            default=[],
            placeholder="Todos os estados",
            key="filtro_estado",
        )

        st.divider()

        def _limpar_filtros():
            st.session_state["filtro_credenciado"] = []
            st.session_state["filtro_empresa"] = []
            st.session_state["filtro_estado"] = []

        st.button("🧹 Limpar Filtros", use_container_width=True, on_click=_limpar_filtros)

    # Aplica filtros
    df_filtrado = df.copy()
    df_contagem_filtrada = df_contagem.copy()

    if filtro_credenciado:
        df_filtrado = df_filtrado[df_filtrado['Credenciado'].isin(filtro_credenciado)]
        df_contagem_filtrada = df_contagem_filtrada[
            df_contagem_filtrada['Credenciado'].isin(filtro_credenciado)
        ]

    if filtro_empresa:
        df_filtrado = df_filtrado[df_filtrado['Empresa'].isin(filtro_empresa)]
        df_contagem_filtrada = df_contagem_filtrada[
            df_contagem_filtrada['Empresa'].isin(filtro_empresa)
        ]

    if filtro_estado:
        df_filtrado = df_filtrado[df_filtrado['Estado'].isin(filtro_estado)]
        df_contagem_filtrada = df_contagem_filtrada[
            df_contagem_filtrada['Credenciado'].isin(
                df_filtrado['Credenciado'].unique()
            )
        ]

    # ----------------------------------------------------------
    # INDICADORES
    # ----------------------------------------------------------
    total_os = len(df_filtrado)

    cred_mais_ordens = (
        df_filtrado['Credenciado']
        .value_counts()
        .idxmax() if total_os > 0 else "—"
    )
    qtd_cred_top = (
        df_filtrado['Credenciado']
        .value_counts()
        .max() if total_os > 0 else 0
    )

    empresa_mais_ordens = (
        df_filtrado['Empresa']
        .value_counts()
        .idxmax() if total_os > 0 else "—"
    )
    qtd_empresa_top = (
        df_filtrado['Empresa']
        .value_counts()
        .max() if total_os > 0 else 0
    )

    n_credenciados = df_filtrado['Credenciado'].nunique()
    media_os = round(total_os / n_credenciados, 1) if n_credenciados > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📋 OS Agendadas", f"{total_os:,}".replace(",", "."))
    k2.metric("🏆 Credenciado Top", cred_mais_ordens, delta=f"{qtd_cred_top} OS")
    k3.metric("🏢 Empresa Top", empresa_mais_ordens, delta=f"{qtd_empresa_top} OS")
    k4.metric("📈 Média OS / Credenciado", media_os)

    st.divider()

    # ----------------------------------------------------------
    # TABELAS EM ABAS
    # ----------------------------------------------------------
    tab1, tab2 = st.tabs(["📄 Tabela de Ordens", "📊 Contagem por Credenciado"])

    with tab1:
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            height=450,
            hide_index=True,
        )

        # Exportação do df principal
        excel_bytes = gerar_excel(df_filtrado, sheet_name='Ordens')
        st.download_button(
            label="⬇️ Exportar Ordens para Excel",
            data=excel_bytes,
            file_name="ordens_de_servico.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with tab2:
        st.dataframe(
            df_contagem_filtrada,
            use_container_width=True,
            height=450,
            hide_index=True,
            column_config={
                "Quantidade_OS": st.column_config.NumberColumn(
                    "Quantidade_OS",
                    alignment="left",
                ),
            },
        )

        # Exportação do df_contagem
        excel_contagem = gerar_excel(df_contagem_filtrada, sheet_name='Contagem')
        st.download_button(
            label="⬇️ Exportar Contagem para Excel",
            data=excel_contagem,
            file_name="contagem_credenciados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    st.divider()

    # ----------------------------------------------------------
    # GRÁFICOS LADO A LADO
    # ----------------------------------------------------------
    col_rank, col_mapa = st.columns(2)

    # ========== COLUNA ESQUERDA: RANKING ==========
    with col_rank:
        st.markdown("### Ranking de Credenciados")

        rank = (
            df_filtrado['Credenciado']
            .value_counts()
            .reset_index()
        )
        rank.columns = ['Credenciado', 'Quantidade_OS']
        rank = rank.sort_values('Quantidade_OS', ascending=True)

        # Gradiente azul: mais claro (menos OS) → mais escuro (mais OS)
        n = len(rank)
        from matplotlib.colors import LinearSegmentedColormap
        blue_cmap = LinearSegmentedColormap.from_list(
            'blue_grad', ['#93c5fd', '#3b82f6', '#1e3a5f']
        )
        if n > 0:
            norm_vals = rank['Quantidade_OS'].values / rank['Quantidade_OS'].max()
            cores = [blue_cmap(v) for v in norm_vals]
        else:
            cores = []

        CHART_H = 3.6  # ~350px
        fig, ax = plt.subplots(figsize=(7, max(CHART_H, n * 0.25)))
        fig.patch.set_facecolor('#f5f6fa')
        ax.set_facecolor('#f5f6fa')

        bars = ax.barh(
            rank['Credenciado'],
            rank['Quantidade_OS'],
            color=cores,
            edgecolor='#ffffff',
            linewidth=0.8,
            height=0.65,
        )

        max_val = rank['Quantidade_OS'].max() if n > 0 else 1
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + max_val * 0.015,
                bar.get_y() + bar.get_height() / 2,
                f'{int(width)}',
                va='center',
                ha='left',
                fontsize=10,
                fontweight='bold',
                color='#374151',
            )

        ax.set_xlabel('Quantidade de OS', fontsize=11, color='#4b5563')
        ax.set_title('')
        ax.tick_params(axis='y', labelsize=9, colors='#1f2937')
        ax.tick_params(axis='x', labelsize=9, colors='#6b7280')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#d1d5db')
        ax.spines['bottom'].set_color('#d1d5db')
        ax.set_xlim(0, max_val * 1.12)

        plt.tight_layout()
        st.pyplot(fig)

    # ========== COLUNA DIREITA: MAPA DO BRASIL ==========
    with col_mapa:
        st.markdown("### Ordens por Estado")

        # Mapeamento de nomes/abreviações para código UF (ISO 3166-2:BR)
        ESTADOS_BR = {
            'AC': 'AC', 'Acre': 'AC',
            'AL': 'AL', 'Alagoas': 'AL',
            'AP': 'AP', 'Amapá': 'AP',
            'AM': 'AM', 'Amazonas': 'AM',
            'BA': 'BA', 'Bahia': 'BA',
            'CE': 'CE', 'Ceará': 'CE',
            'DF': 'DF', 'Distrito Federal': 'DF',
            'ES': 'ES', 'Espírito Santo': 'ES',
            'GO': 'GO', 'Goiás': 'GO',
            'MA': 'MA', 'Maranhão': 'MA',
            'MT': 'MT', 'Mato Grosso': 'MT',
            'MS': 'MS', 'Mato Grosso Do Sul': 'MS', 'Mato Grosso do Sul': 'MS',
            'MG': 'MG', 'Minas Gerais': 'MG',
            'PA': 'PA', 'Pará': 'PA',
            'PB': 'PB', 'Paraíba': 'PB',
            'PR': 'PR', 'Paraná': 'PR',
            'PE': 'PE', 'Pernambuco': 'PE',
            'PI': 'PI', 'Piauí': 'PI',
            'RJ': 'RJ', 'Rio De Janeiro': 'RJ', 'Rio de Janeiro': 'RJ',
            'RN': 'RN', 'Rio Grande Do Norte': 'RN', 'Rio Grande do Norte': 'RN',
            'RS': 'RS', 'Rio Grande Do Sul': 'RS', 'Rio Grande do Sul': 'RS',
            'RO': 'RO', 'Rondônia': 'RO',
            'RR': 'RR', 'Roraima': 'RR',
            'SC': 'SC', 'Santa Catarina': 'SC',
            'SP': 'SP', 'São Paulo': 'SP',
            'SE': 'SE', 'Sergipe': 'SE',
            'TO': 'TO', 'Tocantins': 'TO',
        }

        # Contagem por estado
        df_estado = df_filtrado['Estado'].value_counts().reset_index()
        df_estado.columns = ['Estado', 'Quantidade_OS']
        df_estado['UF'] = df_estado['Estado'].map(ESTADOS_BR)
        df_estado = df_estado.dropna(subset=['UF'])

        try:
            geojson_br = carregar_geojson(GEOJSON_URL)

            # Coordenadas centrais de cada estado (para rótulos)
            CENTROIDS = {
                'AC': (-8.77, -70.55), 'AL': (-9.57, -36.78),
                'AP': (1.41, -51.77), 'AM': (-3.07, -63.00),
                'BA': (-12.96, -41.68), 'CE': (-5.20, -39.53),
                'DF': (-15.83, -47.86), 'ES': (-19.19, -40.34),
                'GO': (-15.98, -49.86), 'MA': (-4.96, -45.27),
                'MT': (-12.64, -55.42), 'MS': (-20.51, -54.54),
                'MG': (-18.10, -44.38), 'PA': (-3.79, -52.48),
                'PB': (-7.06, -36.72), 'PR': (-24.89, -51.55),
                'PE': (-8.38, -37.86), 'PI': (-7.72, -42.73),
                'RJ': (-22.25, -42.66), 'RN': (-5.81, -36.59),
                'RS': (-29.75, -53.25), 'RO': (-10.83, -63.34),
                'RR': (1.99, -61.33), 'SC': (-27.45, -50.95),
                'SP': (-22.19, -48.79), 'SE': (-10.57, -37.45),
                'TO': (-10.25, -48.25),
            }

            import plotly.graph_objects as go

            fig_mapa = go.Figure()

            # 1) Camada base: TODOS os estados com contorno cinza e sem preenchimento
            for feat in geojson_br['features']:
                sigla = feat['properties']['sigla']
                fig_mapa.add_trace(go.Choropleth(
                    geojson={'type': 'FeatureCollection', 'features': [feat]},
                    locations=[sigla],
                    featureidkey='properties.sigla',
                    z=[0],
                    colorscale=[[0, '#f0f0f0'], [1, '#f0f0f0']],
                    showscale=False,
                    hoverinfo='skip',
                    marker_line_color='#9ca3af',
                    marker_line_width=1,
                ))

            # 2) Camada com dados: apenas estados que têm ordens
            if len(df_estado) > 0:
                fig_mapa.add_trace(go.Choropleth(
                    geojson=geojson_br,
                    locations=df_estado['UF'],
                    featureidkey='properties.sigla',
                    z=df_estado['Quantidade_OS'],
                    colorscale=[
                        [0.0, '#93c5fd'],
                        [0.3, '#60a5fa'],
                        [0.6, '#3b82f6'],
                        [1.0, '#1e3a5f'],
                    ],
                    showscale=True,
                    colorbar=dict(
                        title=dict(text='OS', font=dict(color='#4b5563')),
                        thickness=14,
                        len=0.6,
                        tickfont=dict(color='#4b5563'),
                    ),
                    marker_line_color='#6b7280',
                    marker_line_width=1.2,
                    hovertemplate='<b>%{location}</b><br>Ordens: %{z}<extra></extra>',
                ))

            # 3) Siglas de todos os estados
            todos_ufs = list(CENTROIDS.keys())
            lats = [CENTROIDS[uf][0] for uf in todos_ufs]
            lons = [CENTROIDS[uf][1] for uf in todos_ufs]

            fig_mapa.add_trace(go.Scattergeo(
                lat=lats,
                lon=lons,
                text=todos_ufs,
                mode='text',
                textfont=dict(size=8, color='#374151', family='Arial'),
                showlegend=False,
                hoverinfo='skip',
            ))

            fig_mapa.update_geos(
                visible=False,
                bgcolor='rgba(0,0,0,0)',
                center=dict(lat=-14.0, lon=-53.0),
                projection_scale=4.7,
            )

            fig_mapa.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='#f5f6fa',
                geo_bgcolor='#f5f6fa',
                font=dict(color='#1f2937'),
                height=350,
            )

            st.plotly_chart(fig_mapa, use_container_width=True, config={'staticPlot': True})

        except Exception as e:
            st.error(f"Erro ao carregar o mapa: {e}")

else:
    # Tela de boas-vindas quando não há upload
    st.markdown("""
    <div style="
        text-align: center;
        padding: 80px 20px;
        color: #6b7280;
    ">
        <div style="font-size: 4rem; margin-bottom: 16px;">📂</div>
        <h3 style="color: #374151; margin-bottom: 8px;">Nenhum arquivo carregado</h3>
        <p style="font-size: 1.05rem; color: #6b7280;">
            Envie um relatório <code style="color: #374151;">.xlsx</code> na barra lateral para começar a análise.
        </p>
    </div>
    """, unsafe_allow_html=True)
