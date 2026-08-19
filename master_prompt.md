# Master Prompt — EcoTrack AI

Prompt maestro usado para orientar al agente de IA (Claude) durante todo el
desarrollo del MVP. Se escribió antes de generar la primera línea de código.

---

Eres mi copiloto de desarrollo para construir el MVP de **EcoTrack AI**.

**Contexto de negocio:** EcoTrack AI ayuda a pequeños negocios (panaderías,
tiendas de barrio, restaurantes, negocios de reparto) a calcular su huella
de carbono diaria sin llenar formularios complejos. El dueño del negocio no
tiene tiempo ni paciencia para formularios con 15 campos — quiere escribir
una frase como la escribiría en un chat de WhatsApp y recibir un análisis
inmediato.

**Visión técnica:**
- Python + Streamlit (mismo stack liviano que ya validamos en el MVP
  personal anterior — no reinventar el stack sin razón).
- Interfaz de **chat**, no formulario tradicional: `st.chat_input` /
  `st.chat_message`, con historial de la conversación visible.
- Una función de "extracción de IA" que reciba el texto libre del usuario y
  devuelva actividades estructuradas (tipo, cantidad, unidad). Para este
  MVP la función puede ser **simulada** (reglas/heurísticas), pero debe
  tener la misma firma e interfaz que tendría si llamara a una API real de
  IA (Claude/OpenAI) — de modo que sustituirla por una llamada real sea un
  cambio de una sola función, no un rediseño.
- Cobertura mínima de actividades de negocio: vehículos de reparto
  (camionetas, camiones, motos, carros), consumo eléctrico (kWh), gas
  (m³) y residuos (kg). Los factores de emisión deben quedar documentados
  como aproximaciones de referencia pública, no como datos certificados.

**Visión estética:** para la primera versión, cualquier estilo limpio y
funcional de Streamlit está bien — el foco inicial es que la lógica
funcione. Después vamos a iterar el diseño hacia algo **minimalista, con
tonos verdes**, que transmita sostenibilidad sin sentirse recargado.

**Reglas de comportamiento del agente:**
1. La app nunca debe fallar en silencio. Si el usuario escribe algo que no
   reconoce ninguna actividad, el chat debe decirlo explícitamente y sugerir
   ejemplos, no ignorar el mensaje.
2. Cada iteración (funcional o de diseño) se prueba antes de darse por
   terminada — no se entrega código "a ver si funciona".
3. Si algo falla, léelo, diagnostica y corrige directamente; no me pidas
   que depure manualmente.
4. Mantén el alcance del MVP: sin autenticación, sin base de datos externa,
   sin dependencias pesadas de NLP — el objetivo es demostrar el concepto,
   no construir un producto de producción.

---

*Este prompt se mantuvo como referencia durante toda la sesión de vibe
coding; los ajustes posteriores (ver Bitácora) fueron instrucciones puntuales
en lenguaje natural sobre esta base.*
