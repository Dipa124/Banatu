import pandas as pd
import streamlit as st
from itertools import chain

from utils import Persona
from utils import wait_notificaciones
from utils import nombres_personas, buscar_persona
from utils import pagador_gastos, deudores_gastos


def pagina_personas():
    col_izq, col_dch = st.columns(2)
    with col_izq:
        st.subheader("➕ Añadir Personas")

        with st.form("añadir_persona", clear_on_submit=True):
            nombre = st.text_input("Nombre:", placeholder="Ej: El Nano", max_chars=15).strip()

            submitted = st.form_submit_button("Añadir", type="primary")
            if submitted:
                añadir_persona(nombre)

    with col_dch:
        st.subheader("🗑️ Eliminar Personas")

        if len(st.session_state.personas) == 0:
            st.info("No hay aún personas registradas.")
        else:
            with st.form("eliminar_persona"):
                nombre = st.selectbox("Elige la persona a eliminar:", nombres_personas())

                submitted = st.form_submit_button("Eliminar")
                if submitted:
                    eliminar_persona(nombre)

    st.subheader("📝 Personas registradas")
    if len(st.session_state.personas) == 0:
        st.info("No hay aún personas registradas.")
    else:
        st.dataframe(pd.DataFrame(nombres_personas(), columns=["Nombre"]), hide_index=False)


def añadir_persona(nombre):
    nombres_existentes = nombres_personas()
    if nombre == "":
        st.warning(f"Asegurate de completar el campo.", icon="⚠️")
    elif nombre not in nombres_existentes:
        persona_nueva = Persona(nombre)
        st.session_state.personas.append(persona_nueva)
        st.success(f"¡'{nombre}' añadido correctamente!", icon="✅")
        wait_notificaciones()
    else:
        st.warning(f"La persona '{nombre}' ya existe.", icon="⚠️")
        wait_notificaciones()


def eliminar_persona(nombre):
    pagadores = pagador_gastos(solo_nombres=True)
    deudores = list(set(chain.from_iterable(deudores_gastos(solo_nombres=True))))
    if nombre not in pagadores and nombre not in deudores:
        Persona.registro.remove(buscar_persona(nombre))
        st.session_state.personas.remove(buscar_persona(nombre))
        st.error(f"La persona '{nombre}' ha sido eliminada.", icon="❌")
        wait_notificaciones()
    else:
        st.warning(f"La persona '{nombre}' no puede eliminarse, ya que participa en un gasto.", icon="⚠️")
        wait_notificaciones()
