# CLAUDE.md — Reglas del agente para EcoTrack AI

> Cumple el mismo rol que `.cursorrules` en Cursor. Ver también
> `master_prompt.md` para la visión completa del producto.

## Visión del producto

EcoTrack AI ayuda a pequeños negocios a calcular su huella de carbono
diaria describiendo sus actividades en lenguaje natural, vía una interfaz
de chat (no un formulario).

## Stack y convenciones técnicas

- Python 3 + Streamlit, interfaz de chat (`st.chat_input`/`st.chat_message`).
- La función de extracción de actividades (`ai_extractor.py`) debe mantener
  siempre el mismo contrato de entrada/salida que tendría una llamada real
  a un LLM, aunque su implementación actual sea simulada (regex/heurística).
- Dependencias mínimas: nada de librerías de NLP pesadas para el MVP.
- Factores de emisión documentados como aproximaciones públicas, no datos
  certificados.
- Todo cambio de diseño se aplica vía `.streamlit/config.toml` (tema) y CSS
  inyectado en `app.py`, no reescribiendo componentes desde cero.

## Cómo debe comportarse el agente

1. Priorizar la intención sobre la sintaxis: recibir descripciones de alto
   nivel ("hazlo más minimalista", "agrega detección de gas") y decidir la
   implementación.
2. Nunca fallar en silencio: si el chat no detecta actividades, debe
   decirlo y sugerir ejemplos.
3. Diagnosticar y corregir errores directamente (leer el traceback/reproducir
   el caso en aislado), sin pedir depuración manual al desarrollador.
4. Probar cada cambio (funcional o visual) con una ejecución real antes de
   darlo por terminado — no entregar código sin verificar.
5. Preguntar antes de expandir el alcance cuando una instrucción sea
   ambigua.

## Fuera de alcance (por ahora)

- Autenticación, persistencia externa, integraciones con proveedores reales
  de electricidad/gas.
- Llamadas reales a una API de IA (queda documentado cómo se conectaría,
  pero no se activa en este MVP para no depender de API keys en el
  despliegue de evaluación).
