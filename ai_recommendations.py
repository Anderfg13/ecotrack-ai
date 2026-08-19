"""
Capa de recomendaciones personalizadas de EcoTrack AI.

A diferencia de `ai_extractor.py` (extracción, simulada por diseño), esta
función SÍ hace una llamada real a un LLM (Claude) cuando hay una API key
disponible, para cumplir con el pedido explícito del feedback del capstone:
"usa LLMs para generar recomendaciones personalizadas, no solo reglas
fijas".

Si no hay `ANTHROPIC_API_KEY` configurada (o la llamada falla por cualquier
motivo: red, cuota, timeout), cae automáticamente a un recomendador
simulado basado en reglas, para que el demo nunca se rompa en un entorno
sin la key configurada (ej. al calificar en Replit sin secrets).
"""

import os

MODEL = "claude-sonnet-4-5"

SYSTEM_PROMPT = (
    "Eres un asesor de sostenibilidad para pequeños negocios en Colombia. "
    "Con base en las actividades de un día que te comparten, da UNA "
    "recomendación breve (máximo 2 frases), concreta y accionable para "
    "reducir la huella de carbono del negocio. Sé específico según las "
    "actividades mencionadas, nunca genérico. No uses markdown."
)

# --- Recomendador simulado (respaldo, y comportamiento por defecto) -------

_TIPS_POR_CATEGORIA = {
    "🚚 Flota": (
        "Considera agrupar entregas por zona para reducir viajes, o evaluar "
        "motos/vehículos eléctricos para las rutas más cortas."
    ),
    "⚡ Electricidad": (
        "Revisa si puedes migrar a iluminación LED o instalar temporizadores "
        "en equipos que no necesitan estar encendidos todo el día."
    ),
    "🔥 Gas": (
        "Un mantenimiento periódico de calderas o estufas industriales suele "
        "reducir el consumo de gas entre un 5% y 10%."
    ),
    "🗑️ Residuos": (
        "Separar residuos orgánicos para compostaje puede reducir "
        "significativamente lo que termina en relleno sanitario."
    ),
}


def _recomendacion_simulada(actividades: list[dict]) -> str:
    """Elige el tip de la categoría con mayor CO2 detectada hoy."""
    if not actividades:
        return "Cuéntame tus actividades del día y te doy una recomendación personalizada."

    peor = max(actividades, key=lambda a: a["co2"])
    tip = _TIPS_POR_CATEGORIA.get(peor["tipo"], "Sigue registrando tus actividades para detectar patrones de consumo.")
    return f"[modo simulado] {tip}"


# --- Recomendador real (Claude) --------------------------------------------

def _resumen_actividades(actividades: list[dict], total: float) -> str:
    partes = [f"{a['detalle']} ({a['tipo']}): {a['co2']:.2f} kg CO2e" for a in actividades]
    return f"Actividades de hoy: {'; '.join(partes)}. Total: {total:.2f} kg CO2e."


def generar_recomendacion_ia(actividades: list[dict], total: float) -> str:
    """Devuelve una recomendación personalizada.

    Usa la API real de Claude si `ANTHROPIC_API_KEY` está configurada;
    si no, o si la llamada falla, usa el recomendador simulado.
    """
    if not actividades:
        return _recomendacion_simulada(actividades)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _recomendacion_simulada(actividades)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        respuesta = client.messages.create(
            model=MODEL,
            max_tokens=150,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _resumen_actividades(actividades, total)}],
            timeout=10.0,
        )
        texto = respuesta.content[0].text.strip()
        return f"🤖 {texto}"
    except Exception:
        # Cualquier fallo de red/cuota/API cae al modo simulado, sin romper el chat.
        return _recomendacion_simulada(actividades)
