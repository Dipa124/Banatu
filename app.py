import streamlit as st

from utils import inicializar_session_state

from paginas.personas import pagina_personas
from paginas.gastos import pagina_gastos
from paginas.resumen import pagina_resumen
from paginas.avanzado import pagina_avanzado

st.markdown(
    """
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 18px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            padding: 0px 22px;
        }
        .stTabs [data-baseweb="tab"] p {
            font-size: 16px !important;
            font-weight: bold !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] p {
            color: #18ffff !important;
        }
        .stTabs [data-baseweb="tab"]:hover p {
            color: #00b4d8 !important;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #00bcd4 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    st.set_page_config(
        page_title="Banatu",
        page_icon="🧮",
        layout="wide",
    )

    inicializar_session_state()

    st.title("🧮 BANATU")
    st.subheader("Gestor de división de gastos en grupos.")

    tab_personas, tab_gastos, tab_resumen, tab_avanzado = st.tabs(
        [
            "👥 GESTIONAR PERSONAS",
            "💸 GESTIONAR GASTOS",
            "📊 RESUMEN DEUDAS",
            "⚙️ AVANZADO",
        ]
    )

    with tab_personas:
        pagina_personas()
    with tab_gastos:
        pagina_gastos()
    with tab_resumen:
        pagina_resumen()
    with tab_avanzado:
        pagina_avanzado()


if __name__ == "__main__":
    main()
