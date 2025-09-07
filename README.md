# 🧮 Banatu

## Acerca de

Banatu es una aplicación web desarrollada con **Streamlit** para **gestionar y dividir gastos de forma sencilla entre 
miembros de un grupo**. 

El objetivo principal es simplificar el proceso de liquidación: en lugar de mostrar todas las deudas brutas entre 
miembros, la aplicación calcula el balance neto. Por ejemplo, si *A* debe 6€ a *B* y, a su vez, *B* debe 2€ a *A*, en 
vez de que ambos tengan que intercambiar dinero en ambas direcciones, la app propone una liquidación optimizada: *A* 
solo tendría que pagar 4€ a *B*, evitando transferencias innecesarias.

---

## Estructura del repositorio

Estructura relevante (archivos y carpetas principales):

```
Banatu/
├─ .streamlit/
│    └─ config.toml         # Configuración del tema y opciones de Streamlit
│
├─ paginas/                 # Páginas de la interfaz web
│    ├─ personas.py         # Gestión de miembros
│    ├─ gastos.py           # Registro de gastos
│    ├─ resumen.py          # Resumen y balances
│    └─ avanzado.py         # Funcionalidades extra (ej. guardar/cargar datos, cambio de divisa)
│
├─ datos/  
│    └─ datos_ejemplo.json  # Datos sintéticos para probar la app
│
├─ app.py                   # Gestor principal de la web
├─ utils.py                 # Lógica interna y funciones auxiliares
│
├─ pyproject.toml           # Dependencias y requisitos de Python
├─ uv.lock                  # Bloqueo de versiones para entornos reproducibles (para usar "uv sync")
│
├─ LICENSE                  # Licencia del proyecto
└─ README.md                # Estás aquí
```

---

## Requisitos

La aplicación se ha probado únicamente con las versiones indicadas en el archivo `pyproject.toml`:

- **Python**: >= 3.13  
- **pandas**: >= 2.3.2  
- **streamlit**: >= 1.49.1  

> No se garantiza compatibilidad con versiones anteriores de Python o de las librerías.

---

## Setup (usar `uv`)

Se asume que tienes `uv` instalado globalmente. Si no lo tienes, instálalo primero con `pip` u otra forma que prefieras.

1. Clona el repositorio y sitúate en la carpeta del proyecto:

```bash
git clone https://github.com/Dipa124/Banatu.git
cd Banatu
```

2. Regenerar / sincronizar el entorno virtual con `uv`:

```bash
uv sync
```

`uv sync` leerá `pyproject.toml` y creará un `.venv` reproducible

3. (Opcional) Verificar el ejecutable de Python dentro del `.venv` generado:

```bash
uv run python -c "import sys; print(sys.executable)"
```

---

## Ejecutar la app (local)

Con `uv` (recomendado):

```bash
uv run streamlit run app.py
```

Esto ejecuta Streamlit dentro del `.venv` gestionado por `uv`.

Si prefieres no usar `uv` y ya tienes un entorno virtual activo o Streamlit instalado globalmente, puedes usar:

```bash
python -m streamlit run app.py
# o
streamlit run app.py
```

---

## Uso (flujo típico de la app)

La app está diseñada para un uso directo e intuitivo. Flujo general:

1. **Añadir integrantes** — registra a los miembros del grupo (por ejemplo: *Pepe*, *Pepa*, etc.).  
2. **Registrar gastos** — introduce para cada gasto su descripción, importe, la persona que lo pagó y los participantes que lo comparten.  
3. **Matrices de gastos** — consulta una matriz inicial con las deudas brutas y otra optimizada, donde las deudas se simplifican para reducir transferencias innecesarias.  
4. **Ver el resumen** — la aplicación calcula el balance neto y muestra claramente cuánto debe cada miembro y cuánto se le debe.  
