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
arranque. No requiere ninguna API key: la extracción de actividades está
simulada (ver `ai_extractor.py` y la Bitácora).

## Documentación del proceso (vibe coding)

- [`master_prompt.md`](./master_prompt.md) — prompt maestro con la visión
  técnica y estética del proyecto.
- [`bitacora.md`](./bitacora.md) — bitácora completa: iteración de diseño,
  funcionalidad de IA implementada, y un bug real encontrado y corregido.
- [`.cursorrules`](./.cursorrules) / [`CLAUDE.md`](./CLAUDE.md) — reglas del
  agente de IA para este proyecto.

## Archivos clave

- `app.py` — interfaz de chat (Streamlit) + tema minimalista verde.
- `ai_extractor.py` — capa de "extracción de IA" (simulada, con la misma
  interfaz que tendría una llamada real a un LLM).
- `screenshots/` — capturas del proceso de iteración citadas en la bitácora.
