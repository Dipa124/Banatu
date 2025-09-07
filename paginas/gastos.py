import pandas as pd
import streamlit as st

from utils import Gasto
from utils import wait_notificaciones
from utils import nombres_personas, buscar_persona
from utils import descripcion_gastos, cuantia_gastos, pagador_gastos, deudores_gastos, indice_gasto_en_personas


def pagina_gastos():
    col_izq, col_dch = st.columns(2)
    with col_izq:
        st.subheader("📝 Añadir Gastos")
        # FORMULARIO SIMULADO (para poder actualizar la lista de deduores en función del pagador)
        if len(nombres_personas()) < 2:
            st.info("Debe haber al menos 2 personas para crear un gasto.")
        else:
            st.markdown("---")
            descripcion = st.text_input("Descripción:", placeholder="Ej: Cena Mexicano", max_chars=33).strip()
            cuantia = st.number_input("Importe total del gasto:", min_value=0.01, value=5.0)
            pagador = st.selectbox(
                "¿Quién pagó?", nombres_personas(), index=None, placeholder="Seleccionar una persona"
            )
            deudores = st.multiselect(
                "¿Quienes participaron?",
                nombres_personas(),
                placeholder="Elige participantes",
            )

            st.markdown("\n")
            submitted = st.button("Crear gasto", type="primary")
            if submitted:
                if descripcion == "" or not cuantia or not pagador or not deudores:
                    st.warning(f"Asegurate de completar todos los campos.", icon="⚠️")
                else:
                    añadir_gasto(descripcion, cuantia, pagador, deudores)

    with col_dch:
        # Mostrar tabla de gastos existentes
        st.subheader("🧾 Gastos registrados")

        if len(st.session_state.gastos) > 0:
            st.markdown("---")

            descripciones = descripcion_gastos()
            cuantias = cuantia_gastos()
            pagadores = pagador_gastos(solo_nombres=True)
            deudores = deudores_gastos(solo_nombres=True)
            st.dataframe(
                pd.DataFrame(
                    {
                        "Descripción": descripciones,
                        "Cuantía": cuantias,
                        "Pagador": pagadores,
                        "Deudores": deudores,
                    }
                )
            )
        else:
            st.info("Registra al menos un gasto para poder ver la lista.")

    st.subheader("🗑️ Eliminar Gastos")
    if len(st.session_state.gastos) == 0:
        st.info("No hay aún gastos registradas.")
    else:
        with st.form("eliminar_gasto"):
            descripcion = st.selectbox("Elige el gasto a eliminar:", descripcion_gastos())

            submitted = st.form_submit_button("Eliminar")
            if submitted:
                eliminar_gasto(descripcion)


def añadir_gasto(descripcion, cuantia, pagador, deudores):
    # Obtener Personas de participantes para poder pasarle el argumento correcto a gastos
    pagador = buscar_persona(pagador)
    deudores = [buscar_persona(deudor) for deudor in deudores]
    gasto_nuevo = Gasto(descripcion, cuantia, pagador, deudores)

    # Añadir el gasto si no existe uno con esa descripción ya
    if descripcion in descripcion_gastos():
        st.warning("Ya existe un gasto con esa descripción.", icon="⚠️")
        wait_notificaciones()
    else:
        st.session_state.gastos.append(gasto_nuevo)
        st.success(f"¡Gasto '{descripcion}' añadido correctamente!", icon="✅")
        wait_notificaciones()


def eliminar_gasto(descripcion):
    # Eliminar el gasto de todas las personas que participen
    for persona in st.session_state.personas:
        ind_gasto = indice_gasto_en_personas(descripcion, persona)
        if ind_gasto:
            persona.deudas.drop(ind_gasto, axis=0, inplace=True)

    # Eliminar el gasto del session_state
    indice = descripcion_gastos().index(descripcion)
    st.session_state.gastos.pop(indice)
    st.error(f"El gasto '{descripcion}' eliminado correctamente.", icon="❌")
    wait_notificaciones()
