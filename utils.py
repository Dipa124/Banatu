import pandas as pd
import streamlit as st
from time import sleep
from decimal import Decimal
from typing import ClassVar
from json import load, dumps
from dataclasses import dataclass, field


# FUNCIONAMIENTO INTERNO
@dataclass(slots=True)
class Persona:
    # Atributos de instancia:
    nombre: str
    deudas: pd.DataFrame = field(
        default_factory=lambda: pd.DataFrame(columns=["Cuantia", "Destinatario", "Descripcion"])
    )

    # Atributos de clase:
    registro: ClassVar[list["Persona"]] = []

    def __post_init__(self):
        # Añadir cada persona que se cree en un registro para poder acceder a todas desde este
        Persona.registro.append(self)

    def to_dict(self) -> dict:
        dict_persona = {
            "nombre": self.nombre,
            "deudas": self.deudas.to_dict("records")
        }
        return dict_persona

    def añadir_deuda(self, cantidad: float, destinatario: str, descripcion: str) -> None:
        self.deudas.loc[len(self.deudas)] = [cantidad, destinatario, descripcion]

    def deudas_simplificadas(self, destinatario_as_index=False) -> pd.DataFrame:
        return self.deudas.groupby("Destinatario", as_index=destinatario_as_index).sum()

    @staticmethod
    def matriz_deudas(personas: list["Persona"] = None) -> pd.DataFrame:
        if personas is None:
            personas: list[Persona] = Persona.registro
        nombres: list[str] = [persona.nombre for persona in personas]

        matriz_deudas: pd.DataFrame[float] = pd.DataFrame(float(0), index=nombres, columns=nombres)

        for persona in personas:
            if not persona.deudas.empty:
                deudas_redu: pd.DataFrame = persona.deudas_simplificadas(destinatario_as_index=True)
                for destinatario in deudas_redu.index.tolist():
                    matriz_deudas.loc[persona.nombre, destinatario] = deudas_redu.loc[destinatario]["Cuantia"]

        return matriz_deudas

    @staticmethod
    def matriz_deudas_simplificada(personas: list["Persona"] = None) -> pd.DataFrame:
        if personas is None:
            personas: list[Persona] = Persona.registro
        nombres: list = [persona.nombre for persona in personas]

        # Simplificar matriz de deudas para evitar intercambio de dinero duplicado:
        matriz_deudas_simplificada: pd.DataFrame[float] = Persona.matriz_deudas(personas)
        for persona in personas:
            if not persona.deudas.empty:
                persona1: str = persona.nombre
                # Se crea otra lista de nombres para no mirar deudas consigo mismo
                nombres2 = nombres.copy()
                nombres2.remove(persona1)
                for persona2 in nombres2:
                    deudas_mutuas: tuple[float, float] = (
                        matriz_deudas_simplificada.loc[persona1, persona2],
                        matriz_deudas_simplificada.loc[persona2, persona1],
                    )

                    if sum(deudas_mutuas) > 0:
                        # Si la deuda es igual --> Se anulan
                        if deudas_mutuas[0] == deudas_mutuas[1]:
                            matriz_deudas_simplificada.loc[persona1, persona2] = float(0)
                            matriz_deudas_simplificada.loc[persona2, persona1] = float(0)
                        # Si la deuda A es mayor que la B --> A = A-B y B = 0
                        elif deudas_mutuas[0] > deudas_mutuas[1]:
                            deuda_simplificada: float = redondear(deudas_mutuas[0] - deudas_mutuas[1])
                            matriz_deudas_simplificada.loc[persona1, persona2] = deuda_simplificada
                            matriz_deudas_simplificada.loc[persona2, persona1] = float(0)
                        # Si la deuda B es mayor que la A --> A = 0 y B = B-A
                        elif deudas_mutuas[1] > deudas_mutuas[0]:
                            deuda_simplificada: float = redondear(deudas_mutuas[1] - deudas_mutuas[0])
                            matriz_deudas_simplificada.loc[persona1, persona2] = float(0)
                            matriz_deudas_simplificada.loc[persona2, persona1] = deuda_simplificada

        return matriz_deudas_simplificada


@dataclass(slots=True)
class Gasto:
    descripcion: str
    cuantia: float
    pagador: Persona
    deudores: list[Persona]

    def __post_init__(self) -> None:
        # Automatizar reparto del gasto tras crear el gasto
        self.repartir_gasto()

    def to_dict(self):
        dict_gasto = {
            "descripcion": self.descripcion,
            "cuantia": self.cuantia,
            "pagador": self.pagador.nombre,
            "deudores": [deudor.nombre for deudor in self.deudores]
        }
        return dict_gasto

    def repartir_gasto(self) -> None:
        gasto_dividido: float = redondear(self.cuantia / (len(self.deudores)))
        for persona in self.deudores:
            persona.añadir_deuda(gasto_dividido, self.pagador.nombre, self.descripcion)


def redondear(num) -> float:
    d = Decimal.from_float(float(num))
    s = d * Decimal('100')
    frac = s - s.quantize(Decimal('1'), rounding="ROUND_DOWN")
    if frac <= Decimal('1e-10'):
        return float(s.quantize(Decimal('1'), rounding="ROUND_DOWN") / Decimal('100'))

    return float(d.quantize(Decimal('0.01'), rounding="ROUND_UP"))


# BACKEND DE STREAMLIT
def inicializar_session_state():
    if "personas" not in st.session_state:
        st.session_state.personas = []
    if "gastos" not in st.session_state:
        st.session_state.gastos = []
    if "codigo_ISO" not in st.session_state:
        st.session_state.codigo_ISO = "EUR"
    if "moneda" not in st.session_state:
        st.session_state.moneda = "€"


def limpiar_session_state():
    st.session_state.personas = []
    st.session_state.gastos = []


def exportar_datos():
    datos = {
        "personas": [persona.to_dict() for persona in st.session_state.personas],
        "gastos": [gasto.to_dict() for gasto in st.session_state.gastos],
        "codigo_ISO": st.session_state.codigo_ISO,
        "moneda": st.session_state.moneda
    }
    json_datos = dumps(datos)
    return json_datos


def importar_datos(json_datos):
    try:
        limpiar_session_state()
        Persona.registro = []

        if type(json_datos) != dict:
            datos = load(json_datos)
        else:
            datos = json_datos

        for persona in datos["personas"]:
            persona = Persona(persona["nombre"])
            st.session_state.personas.append(persona)

        for gasto in datos["gastos"]:
            descripcion = gasto["descripcion"]
            cuantia = gasto["cuantia"]
            pagador = buscar_persona(gasto["pagador"])
            deudores = [buscar_persona(deudor) for deudor in gasto["deudores"]]
            gasto = Gasto(descripcion, cuantia, pagador, deudores)
            st.session_state.gastos.append(gasto)

        st.session_state.codigo_ISO = datos["codigo_ISO"]
        st.session_state.moneda = datos["moneda"]

        return True
    except Exception as e:
        print(e)
        return False


def wait_notificaciones():
    sleep(1.5)
    st.rerun()


# PARA PERSONAS
def nombres_personas():
    return [persona.nombre for persona in st.session_state.personas]


def buscar_persona(nombre):
    return st.session_state.personas[nombres_personas().index(nombre)]


# PARA GASTOS
def descripcion_gastos():
    return [gasto.descripcion for gasto in st.session_state.gastos]


def cuantia_gastos():
    return [gasto.cuantia for gasto in st.session_state.gastos]


def pagador_gastos(solo_nombres: bool = False):
    lista_pagador_gastos = [gasto.pagador for gasto in st.session_state.gastos]
    if solo_nombres:
        return [pagador.nombre for pagador in lista_pagador_gastos]
    else:
        return lista_pagador_gastos


def deudores_gastos(solo_nombres: bool = False):
    lista_deudores_gastos = [gasto.deudores for gasto in st.session_state.gastos]
    if solo_nombres:
        return [[deudor.nombre for deudor in deudores] for deudores in lista_deudores_gastos]
    else:
        return lista_deudores_gastos


def indice_gasto_en_personas(descripcion_gasto, persona):
    if not persona.deudas.empty:
        for indice_deuda in range(len(persona.deudas)):
            if persona.deudas.loc[indice_deuda].Descripcion == descripcion_gasto:
                return indice_deuda
    return None
