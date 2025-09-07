import pandas as pd
import streamlit as st

from utils import Persona
from utils import redondear


def pagina_resumen():
    col_izq, col_dch = st.columns(2)

    # Matriz deudas - Originales/Simplificadas
    with col_izq:
        personas = st.session_state.personas
        matriz_deudas = Persona.matriz_deudas(personas)
        matriz_deudas_simplificada = Persona.matriz_deudas_simplificada(personas)

        st.subheader("💠 Matriz Deudas")
        if len(st.session_state.gastos) > 0:
            st.dataframe(matriz_deudas)
        else:
            st.info("Añade al menos un gasto para visualizar la matriz.")

        st.subheader("⚖️ Matriz Deudas Simplificada")
        if len(st.session_state.gastos) > 0:
            st.dataframe(matriz_deudas_simplificada)
        else:
            st.info("Añade al menos un gasto para visualizar la matriz.")

    # Deudas por persona
    with col_dch:
        st.subheader("📊 Deudas por persona")
        if len(st.session_state.gastos) > 0:
            for persona in st.session_state.personas:
                resumen_personal(persona, matriz_deudas_simplificada)
        else:
            st.info("No hay aún personas con gastos.")


def resumen_personal(persona, matriz_deudas_simplificada):
    nombre = persona.nombre
    with st.expander(nombre):
        st.text("📉 Debe:")
        deudas = matriz_deudas_simplificada.loc[nombre]
        deudas_filtradas = deudas[deudas.index != nombre]
        tot_deudas_filtradas = redondear(sum(deudas_filtradas))
        if tot_deudas_filtradas > 0:
            col_izq, col_dch = st.columns([3, 1], gap="Large")
            with col_izq:
                df_deudas = pd.DataFrame(columns=["Destinatario", "Cuantía"])
                for destinatario in deudas_filtradas.index.tolist():
                    cuantia = redondear(deudas_filtradas.loc[destinatario])
                    if cuantia > 0:
                        df_deudas.loc[len(df_deudas)] = [destinatario, cuantia]
                st.dataframe(df_deudas, hide_index=True)
            with col_dch:
                if len(df_deudas.Destinatario) > 1:
                    with st.container():
                        st.markdown(
                            '<div style="display: flex; justify-content: center;">',
                            unsafe_allow_html=True,
                        )
                        st.metric("Deuda total:", f"{tot_deudas_filtradas} {st.session_state.moneda}")
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.metric("Deuda total:", f"{tot_deudas_filtradas} {st.session_state.moneda}")
        else:
            st.info("No le debe nada a nadie.")

        st.text("📈 Le deben:")
        creditos = matriz_deudas_simplificada[nombre]
        creditos_filtrados = creditos[creditos.index != nombre]
        tot_creditos_filtradados = redondear(sum(creditos_filtrados))
        if tot_creditos_filtradados > 0:
            col_izq, col_dch = st.columns([3, 1], gap="Large")
            with col_izq:
                df_creditos = pd.DataFrame(columns=["Deudor", "Cuantía"])
                for deudor in creditos_filtrados.index.tolist():
                    cuantia = redondear(creditos_filtrados.loc[deudor])
                    if cuantia > 0:
                        df_creditos.loc[len(df_creditos)] = [deudor, cuantia]
                st.dataframe(df_creditos, hide_index=True)

            with col_dch:
                if len(df_creditos.Deudor) > 1:
                    with st.container():
                        st.markdown(
                            '<div style="display: flex; justify-content: center;">',
                            unsafe_allow_html=True,
                        )
                        st.metric("Crédito total:", f"{tot_creditos_filtradados} {st.session_state.moneda}")
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.metric("Crédito total:", f"{tot_creditos_filtradados} {st.session_state.moneda}")
        else:
            st.info("Nadie le debe nada.")
