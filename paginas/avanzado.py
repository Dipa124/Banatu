import streamlit as st

from utils import exportar_datos, importar_datos
from utils import limpiar_session_state, wait_notificaciones


def pagina_avanzado():
    st.subheader("🪙 Gestionar moneda:")
    monedas = {
        "USD": {"nombre": "Dólar estadounidense", "simbolo": "$"},
        "EUR": {"nombre": "Euro", "simbolo": "€"},
        "GBP": {"nombre": "Libra esterlina", "simbolo": "£"},
        "JPY": {"nombre": "Yen japonés", "simbolo": "¥"},
        "CNY": {"nombre": "Yuan chino", "simbolo": "¥"},
        "CHF": {"nombre": "Franco suizo", "simbolo": "CHF"},
        "KRW": {"nombre": "Won surcoreano", "simbolo": "₩"},
        "INR": {"nombre": "Rupia india", "simbolo": "₹"},
        "RUB": {"nombre": "Rublo ruso", "simbolo": "₽"},
        "TRY": {"nombre": "Lira turca", "simbolo": "₺"},
        "BRL": {"nombre": "Real brasileño", "simbolo": "R$"},
        "CAD": {"nombre": "Dólar canadiense", "simbolo": "C$"},
        "AUD": {"nombre": "Dólar australiano", "simbolo": "A$"},
        "NZD": {"nombre": "Dólar neozelandés", "simbolo": "NZ$"},
        "VND": {"nombre": "Dong vietnamita", "simbolo": "₫"},
        "ILS": {"nombre": "Shekel israelí", "simbolo": "₪"},
        "UAH": {"nombre": "Grivna ucraniana", "simbolo": "₴"},
        "NGN": {"nombre": "Naira nigeriana", "simbolo": "₦"},
        "THB": {"nombre": "Baht tailandés", "simbolo": "฿"},
        "PYG": {"nombre": "Guaraní paraguayo", "simbolo": "₲"},
        "GHS": {"nombre": "Cedi ghanés", "simbolo": "₵"},
        "MXN": {"nombre": "Peso mexicano", "simbolo": "$"},
        "CLP": {"nombre": "Peso chileno", "simbolo": "$"},
        "ARS": {"nombre": "Peso argentino", "simbolo": "$"},
        "COP": {"nombre": "Peso colombiano", "simbolo": "$"},
        "PEN": {"nombre": "Sol peruano", "simbolo": "S/"},
        "ZAR": {"nombre": "Rand sudafricano", "simbolo": "R"},
    }
    opciones = [f"{data['simbolo']} - {data['nombre']} ({codigo})" for codigo, data in monedas.items()]
    indice_moneda_actual = next(
        (i for i, opcion in enumerate(opciones) if f"({st.session_state.codigo_ISO})" in opcion), 0)
    selector_moneda = st.selectbox("Elige la unidad monetaria:", opciones, index=indice_moneda_actual,
                                   placeholder="Selecciona moneda")
    if selector_moneda:
        codigo_iso = selector_moneda.split("(")[-1].strip(")")
        simbolo_moneda = monedas[codigo_iso]["simbolo"]

        if codigo_iso != st.session_state.codigo_ISO:
            st.session_state.codigo_ISO = codigo_iso
            st.session_state.moneda = simbolo_moneda
            st.success(f"¡Moneda cambiada correctamente!", icon="✅")
            wait_notificaciones()

    st.subheader("🗃️ Gestionar datos:")
    # Descargar datos
    st.download_button("Descargar datos", data=exportar_datos(), file_name="datos.json", icon="📥")

    # Cargar datos
    with st.form("cargar_datos", clear_on_submit=True):
        archivo_datos = st.file_uploader("Elige el archivo de datos", type="json")
        submitted = st.form_submit_button(label="Cargar datos", icon="📤")

        if submitted:
            if not archivo_datos:
                st.warning("Asegurate de seleccionar un archivo de datos.", icon="⚠️")
                wait_notificaciones()
            else:
                importados = importar_datos(archivo_datos)
                if importados:
                    st.success(f"¡Datos cargados correctamente!", icon="✅")
                    wait_notificaciones()
                else:
                    st.error("No se ha podido cargar los datos.", icon="❌")
                    wait_notificaciones()

    boton_eliminar = st.button("🗑️ Limpiar todos los datos")
    if boton_eliminar:
        limpiar_session_state()
        st.error("Todos los datos han sido eliminados.", icon="❌")
        wait_notificaciones()
