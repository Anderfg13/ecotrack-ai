# Bitácora — EcoTrack AI (Capstone Vibe Coding)

## 1. El "vibe" y el prompt maestro

Antes de escribir código, se definió el prompt maestro con la visión técnica
y estética completa del proyecto (stack, interfaz de chat, alcance de la
función de IA, reglas de comportamiento del agente). Ver
[`master_prompt.md`](./master_prompt.md) para el texto completo.

Decisiones clave que salieron de ese prompt:

- Interfaz de **chat** (`st.chat_input` / `st.chat_message`) en vez de un
  formulario, porque el enunciado explícitamente pide algo que un dueño de
  negocio pueda usar como si le escribiera a alguien por WhatsApp.
- Una función `extraer_actividades_ia()` con la misma forma que tendría una
  llamada real a un LLM (mismo contrato de entrada/salida), aunque para este
  MVP se implementó **simulada** (heurísticas + regex) — decisión tomada
  explícitamente para no depender de una API key en el despliegue de
  evaluación, sin sacrificar la posibilidad de conectar una API real después.

## 2. Desarrollo iterativo

### v1 — Funcionalidad primero

Se construyó `app.py` + `ai_extractor.py` con el estilo por defecto de
Streamlit, para validar la lógica antes de invertir en diseño.

Prueba con la frase exacta del enunciado
*("Hoy usamos 5 camionetas de reparto y gastamos 200kWh de luz")*:

![v1 chat](./screenshots/v1_chat.png)

Resultado: 5 camionetas (40.00 kg CO2e) + 200 kWh (32.80 kg CO2e) =
**72.80 kg CO2e**, calculado correctamente.

### Iteración de diseño — "Hazlo más minimalista y usa tonos verdes"

Instrucción dada en lenguaje natural al agente, tal como sugiere el
enunciado. El agente respondió con dos cambios concretos:

1. `.streamlit/config.toml` — tema nativo de Streamlit con paleta verde
   (`primaryColor = "#2E7D32"`, fondo `#FBFEFB`, fondo secundario `#E8F5E9`).
2. CSS inyectado en `app.py` — oculta el menú/footer por defecto, redondea
   las tarjetas del chat, y resalta el métrico de huella acumulada con un
   recuadro verde suave.

Antes / después:

| Antes (v1) | Después (v2, minimalista + verde) |
|---|---|
| ![antes](./screenshots/v1_inicial.png) | ![después](./screenshots/v2_minimalista.png) |

## 3. Funcionalidad de IA implementada

`ai_extractor.extraer_actividades_ia(texto)` recibe el mensaje libre del
usuario y devuelve una lista estructurada de actividades detectadas (tipo,
detalle, cantidad, unidad, CO2 estimado), cubriendo cuatro categorías de
consumo de negocio: flota de vehículos, electricidad (kWh), gas (m³) y
residuos (kg).

Es una **simulación documentada** de una capa de extracción por IA: en vez
de una llamada a un modelo de lenguaje, usa palabras clave + expresiones
regulares. Se decidió así (ver conversación con el usuario) para que el
MVP funcione sin necesidad de configurar una API key en el entorno de
despliegue de evaluación. El módulo incluye, en su docstring, el fragmento
de código que se usaría para reemplazarla por una llamada real a la API de
Claude sin cambiar el resto de la aplicación — la función ya expone el
contrato (mismo texto de entrada, misma lista de actividades de salida) que
tendría esa versión real.

## 4. Debugging con IA

**Problema encontrado:** al probar una segunda actividad en la conversación
con formato de énfasis (`*Además* gastamos __15m3__ de gas...`), la app no
detectaba el gas, y el mensaje del usuario se renderizaba con cursiva/negrita
en vez de mostrar el texto tal cual se escribió.

Antes del fix:

![bug antes](./screenshots/bug_antes_1.png)

**Diagnóstico:** se le pidió al agente reproducir el caso en aislado
(`extraer_actividades_ia()` directamente, sin la interfaz) para confirmar
que el problema estaba en el parser y no en Streamlit. Causa raíz: los
guiones bajos de markdown (`__15m3__`) quedaban pegados al número y a la
unidad, y el regex de gas esperaba solo espacios entre `"15m3"` y `"de gas"`,
así que no matcheaba. Un segundo síntoma relacionado: `st.markdown()`
interpretaba los asteriscos/guiones bajos del usuario como formato en vez de
texto literal.

**Solución (propuesta y aplicada por el agente, sin depurar línea a línea
manualmente):**

1. `_sanitizar()` en `ai_extractor.py` — quita `*`, `_` y `` ` `` del texto
   antes de aplicar cualquier patrón, en vez de parchar cada regex por
   separado.
2. `_escapar_markdown()` en `app.py` — escapa esos mismos caracteres antes de
   mostrar el mensaje del usuario, para que se vea tal como lo escribió.

Después del fix (misma frase, detecta gas y residuos, y el texto se muestra
literal):

![bug después](./screenshots/bug_despues_1.png)

## 5. Vibe Coding vs. desarrollo tradicional

Construir este MVP tomó una sesión continua de orquestación: describir la
visión completa una vez (prompt maestro), dejar que el agente generara la
primera versión funcional, y luego dirigir dos iteraciones puntuales en
lenguaje natural (diseño y un bug real) sin escribir ni depurar código a
mano. La diferencia frente a un flujo tradicional no es solo velocidad: es
que el tiempo humano se concentró en decidir *qué* debía hacer la app y
*cómo* debía sentirse, mientras que la traducción a sintaxis, la detección
de la causa raíz del bug y la implementación del fix quedaron delegadas —
verificadas en cada paso con pruebas reales (regex en aislado, capturas de
pantalla del navegador) antes de darlas por buenas.
