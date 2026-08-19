"""
EcoTrack AI — MVP de chat para que pequeños negocios calculen su huella de
carbono diaria describiendo sus actividades en lenguaje natural.

Ej: "Hoy usamos 5 camionetas de reparto y gastamos 200kWh de luz"
"""

from datetime import datetime

import streamlit as st

from ai_extractor import extraer_actividades_ia
from ai_recommendations import generar_recomendacion_ia


def _escapar_markdown(texto: str) -> str:
    """Evita que asteriscos/guiones bajos del usuario se rendericen como
    formato markdown (bug encontrado: "*Además*" se mostraba en cursiva)."""
    import re

    return re.sub(r"([*_`])", r"\\\1", texto)

st.set_page_config(page_title="EcoTrack AI", page_icon="🌿", layout="centered")

# --- Iteración de diseño (prompt: "hazlo más minimalista y con tonos verdes") ---
st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 2.5rem; max-width: 760px;}
    h1 {font-weight: 700; letter-spacing: -0.02em; color: #1B4332;}
    [data-testid="stMetric"] {
        background: #E8F5E9;
        border: 1px solid #C8E6C9;
        border-radius: 12px;
        padding: 0.75rem 1rem;
    }
    [data-testid="stMetricValue"] {color: #2E7D32;}
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        border: 1px solid #E0E0E0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant",
            "content": (
                "Hola 👋 Soy el asistente de **EcoTrack AI**. Cuéntame qué "
                "hizo tu negocio hoy (vehículos de reparto, electricidad, gas, "
                "residuos...) y te doy un estimado de tu huella de carbono.\n\n"
                "Ej: *\"Hoy usamos 5 camionetas de reparto y gastamos 200kWh de luz\"*"
            ),
        }
    ]
if "total_dia" not in st.session_state:
    st.session_state.total_dia = 0.0

st.title("🌿 EcoTrack AI")
st.caption("Huella de carbono para pequeños negocios, en lenguaje natural.")

st.metric("Huella acumulada hoy", f"{st.session_state.total_dia:.2f} kg CO2e")

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Describe las actividades de hoy...")

if prompt:
    st.session_state.mensajes.append({"role": "user", "content": _escapar_markdown(prompt)})
    with st.chat_message("user"):
        st.markdown(_escapar_markdown(prompt))

    actividades = extraer_actividades_ia(prompt)

    if not actividades:
        respuesta = (
            "No detecté actividades que pueda medir en ese mensaje 🤔. "
            "Prueba mencionando vehículos (ej. *3 camionetas*), electricidad "
            "(ej. *200kWh*), gas (ej. *15m3 de gas*) o residuos "
            "(ej. *8kg de basura*)."
        )
    else:
        total = sum(a["co2"] for a in actividades)
        st.session_state.total_dia += total
        lineas = [f"He detectado **{len(actividades)} actividad(es)**:\n"]
        for a in actividades:
            lineas.append(f"- {a['tipo']} — {a['detalle']}: **{a['co2']:.2f} kg CO2e**")
        lineas.append(f"\n**Total de este mensaje: {total:.2f} kg CO2e**")
        recomendacion = generar_recomendacion_ia(actividades, total)
        lineas.append(f"\n💡 **Recomendación:** {recomendacion}")
        respuesta = "\n".join(lineas)

    st.session_state.mensajes.append({
        "role": "assistant",
        "content": respuesta,
        "hora": datetime.now().strftime("%H:%M"),
    })
    st.rerun()
