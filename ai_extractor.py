"""
Capa de "extracción de IA" para EcoTrack AI.

IMPORTANTE (ver Bitácora): esta función está SIMULADA a propósito para
este MVP (heurísticas + regex), pero se diseñó con la misma firma e
interfaz de entrada/salida que tendría una llamada real a un modelo de
lenguaje. Sustituirla por una API real (Claude, OpenAI, etc.) es un
cambio contenido a esta función: recibiría el mismo `texto` y debería
devolver la misma lista de diccionarios `{tipo, detalle, cantidad,
unidad, co2}`.

Ejemplo de cómo se vería la versión real (no usada en este MVP):

    def extraer_actividades_ia(texto: str) -> list[dict]:
        respuesta = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": PROMPT_EXTRACCION.format(texto=texto),
            }],
        )
        return json.loads(respuesta.content[0].text)  # el modelo devuelve JSON
"""

import re

# ---------------------------------------------------------------------------
# Factores de emisión (kg CO2e). Aproximaciones de referencia pública para
# un MVP educativo (no para reporting oficial de sostenibilidad).
# ---------------------------------------------------------------------------

# kg CO2e por uso/día de vehículo (recorrido urbano típico de reparto local).
VEHICLE_FACTORS_KG_CO2E_PER_USO = {
    "camion": 12.0,
    "camión": 12.0,
    "camiones": 12.0,
    "camioneta": 8.0,
    "camionetas": 8.0,
    "furgon": 10.0,
    "furgón": 10.0,
    "furgones": 10.0,
    "carro": 5.0,
    "carros": 5.0,
    "auto": 5.0,
    "autos": 5.0,
    "moto": 2.0,
    "motos": 2.0,
    "motocicleta": 2.0,
    "motocicletas": 2.0,
}

ELECTRICITY_KG_CO2E_PER_KWH = 0.164  # factor de red eléctrica de Colombia (aprox.)
GAS_KG_CO2E_PER_M3 = 2.03            # combustión de gas natural (aprox.)
WASTE_KG_CO2E_PER_KG = 0.5           # residuos a relleno sanitario (aprox.)

VEHICLE_PATTERN = re.compile(
    r"(\d+)\s*(" + "|".join(sorted(VEHICLE_FACTORS_KG_CO2E_PER_USO, key=len, reverse=True)) + r")\b"
)
ELECTRICITY_PATTERN = re.compile(r"(\d+(?:[.,]\d+)?)\s*kwh", re.IGNORECASE)
GAS_PATTERN = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:m3|m³|metros?\s+c[uú]bicos?)\s*(?:de\s+)?gas", re.IGNORECASE)
WASTE_PATTERN = re.compile(r"(\d+(?:[.,]\d+)?)\s*kg\s*(?:de\s+)?(?:basura|residuos)", re.IGNORECASE)


def _to_float(raw: str) -> float:
    return float(raw.replace(",", "."))


def _sanitizar(texto: str) -> str:
    """Quita ruido de formato (markdown, comillas) que rompe los patrones.

    Bug real encontrado en pruebas: un mensaje como
    "*Además* gastamos __15m3__ de gas" no detectaba el gas porque los
    guiones bajos de énfasis quedaban pegados al número/unidad y el regex
    esperaba solo espacios entre "15m3" y "de gas". La solución es
    normalizar el texto antes de aplicar cualquier patrón, no parchar cada
    regex por separado.
    """
    return re.sub(r"[*_`]", " ", texto)


def extraer_actividades_ia(texto: str) -> list[dict]:
    """Extrae actividades de negocio y su CO2 estimado a partir de texto libre.

    Simula lo que devolvería un servicio de IA de extracción de información:
    una lista de actividades estructuradas, cada una con su tipo, detalle,
    cantidad, unidad y emisiones estimadas en kg CO2e.
    """
    texto_low = _sanitizar(texto.lower())
    actividades = []

    for match in VEHICLE_PATTERN.finditer(texto_low):
        cantidad = int(match.group(1))
        vehiculo = match.group(2)
        factor = VEHICLE_FACTORS_KG_CO2E_PER_USO[vehiculo]
        co2 = cantidad * factor
        actividades.append({
            "tipo": "🚚 Flota",
            "detalle": f"{cantidad} {vehiculo}",
            "cantidad": cantidad,
            "unidad": "uso/día",
            "co2": co2,
        })

    match = ELECTRICITY_PATTERN.search(texto_low)
    if match:
        kwh = _to_float(match.group(1))
        co2 = kwh * ELECTRICITY_KG_CO2E_PER_KWH
        actividades.append({
            "tipo": "⚡ Electricidad",
            "detalle": f"{kwh:g} kWh",
            "cantidad": kwh,
            "unidad": "kWh",
            "co2": co2,
        })

    match = GAS_PATTERN.search(texto_low)
    if match:
        m3 = _to_float(match.group(1))
        co2 = m3 * GAS_KG_CO2E_PER_M3
        actividades.append({
            "tipo": "🔥 Gas",
            "detalle": f"{m3:g} m³",
            "cantidad": m3,
            "unidad": "m³",
            "co2": co2,
        })

    match = WASTE_PATTERN.search(texto_low)
    if match:
        kg = _to_float(match.group(1))
        co2 = kg * WASTE_KG_CO2E_PER_KG
        actividades.append({
            "tipo": "🗑️ Residuos",
            "detalle": f"{kg:g} kg",
            "cantidad": kg,
            "unidad": "kg",
            "co2": co2,
        })

    return actividades
