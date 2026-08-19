# EcoTrack AI — Capstone Vibe Coding

MVP de chat para que pequeños negocios calculen su huella de carbono
diaria describiendo sus actividades en lenguaje natural (ej. *"Hoy usamos
5 camionetas de reparto y gastamos 200kWh de luz"*).

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Desplegado en Replit

Importa este repositorio en Replit — `.replit` ya define el comando de
arranque. Funciona sin ninguna API key (la extracción de actividades está
simulada). Si quieres activar las recomendaciones generadas por Claude en
vez del recomendador simulado, agrega tu propia key como Secret en Replit:

```
ANTHROPIC_API_KEY = sk-ant-...
```

Sin esa key, o si la llamada falla por cualquier motivo, la app cae
automáticamente al recomendador simulado — el chat nunca se rompe.

## Documentación del proceso (vibe coding)

- [`master_prompt.md`](./master_prompt.md) — prompt maestro con la visión
  técnica y estética del proyecto.
- [`bitacora.md`](./bitacora.md) — bitácora completa: prompts usados por
  componente, iteración de diseño, funcionalidad de IA (extracción
  simulada + recomendaciones reales con Claude) y un bug real encontrado y
  corregido.
- [`.cursorrules`](./.cursorrules) / [`CLAUDE.md`](./CLAUDE.md) — reglas del
  agente de IA para este proyecto.

## Archivos clave

- `app.py` — interfaz de chat (Streamlit) + tema minimalista verde.
- `ai_extractor.py` — capa de "extracción de IA" simulada (misma interfaz
  que tendría una llamada real a un LLM) para detectar actividades.
- `ai_recommendations.py` — recomendaciones personalizadas: llamada real a
  la API de Claude si hay `ANTHROPIC_API_KEY`, con respaldo simulado si no.
- `screenshots/` — capturas del proceso de iteración citadas en la bitácora.
