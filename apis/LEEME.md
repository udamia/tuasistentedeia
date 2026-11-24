# APIs: tu asistente usando Claude, ChatGPT o Gemini desde un programa

Esta carpeta es para cuando **un programa tuyo** necesita a la IA sin que estés en el chat (capítulo 17 del libro). Para chatear, usar Claude Code o programar tareas, **no hace falta**: alcanza con tu plan.

## Qué trae

| Archivo | Qué hace |
|---|---|
| `probar_api.py` | Guarda tu clave en el `.env` sin que se vea y la prueba con un pedido chiquito. Sirve para Claude, OpenAI y Gemini |
| `resumir_y_avisar.py` | El ejercicio de punta a punta: resume un archivo de `trabajos/` con Claude por API y te lo manda a Telegram |

Los dos usan solo lo que trae Python: no hay que instalar nada. En Mac, escribí `python3` en lugar de `python`.

## El paso a paso corto

1. **Elegí una sola empresa,** la que ya usás.
2. **Creá la clave** con un nombre que diga para qué es y con vencimiento:
   - Claude: **platform.claude.com > API keys > Create key**, y elegí un **espacio de trabajo** (Workspace) para la clave: el de tu programa o **Default**. Una clave sin espacio no anda sola (si ya la tenés así, completá `ANTHROPIC_WORKSPACE_ID` en el `.env`).
   - OpenAI: **platform.openai.com > API keys > Create new secret key** (permisos **Restricted** si sabés qué usa).
   - Gemini: **aistudio.google.com > API keys > Create API key**, y después **Add restrictions > Restrict to Gemini API only**.
   Se muestra **una sola vez**: copiala en el momento.
3. **Ponele tope antes de usarla:**
   - Claude: **Spend limits > Monthly spend limit > Set limit** (mejor, un **Workspace** propio con su tope, y la clave creada en ese espacio).
   - OpenAI: **Limits > Spend > Edit spend limit** y prendé **Enforce a hard limit**. En la primera compra, apagá **Use auto-reload**.
   - Gemini: **Spend > Monthly spend cap > Edit spend cap**.
   Cargá el crédito mínimo y dejá la recarga automática apagada al principio.
4. **Guardala** desde la carpeta principal:
   ```
   python apis/probar_api.py --configurar claude
   ```
   (o `openai`, o `gemini`). Te la pide sin mostrarla y la guarda en el `.env`.
5. **Probala:**
   ```
   python apis/probar_api.py --ver claude
   python apis/probar_api.py claude "Decime en una frase qué es una API"
   ```
6. **Mirá el gasto** en la página **Usage** de la consola de esa empresa.
7. **El ejercicio de punta a punta** (necesita también el bot de avisos: `python telegram/avisar.py --configurar`):
   ```
   python apis/resumir_y_avisar.py --ver trabajos/lunes.md
   python apis/resumir_y_avisar.py trabajos/lunes.md
   ```
8. **Antes de cada push:** `python herramientas/revisar_repo.py` tiene que decir TODO BIEN.

## Las reglas de una clave

- **Nunca** en un chat (tampoco el de Claude Code), en GitHub, en AGENTS.md, CLAUDE.md ni en un mensaje.
- **Solo en el `.env`** de esta carpeta, que no se sube. No como variable de toda la computadora: así Claude Code sigue usando tu plan.
- **Una clave por uso,** con tope de gasto y vencimiento.
- **Rotala** cada 3 meses: creá la nueva, cambiala en el `.env`, probala y recién ahí borrá la vieja.

## Si se filtró una clave

1. Apagala o borrala ya desde la consola (Claude: **Disable** o **Delete**; OpenAI: el tachito; Google: desactivarla en la consola de Google Cloud).
2. Creá otra y guardala con `--configurar`.
3. Mirá el gasto de los últimos días.
4. Buscá dónde quedó. Si estuvo en GitHub, borrar el archivo no alcanza: queda en el historial. Primero la clave.
5. Anotalo en `decisiones/registro.md`.

## Conectar una API nueva

Pedíselo a tu asistente así:

```
Quiero conectar mi cerebro con la API de [nombre de la app] para [qué querés que haga]. Primero leé la documentación oficial y explicame en palabras simples qué permisos necesita, cuánto cuesta, qué límites tiene y cómo se apaga. Después proponeme el plan y esperá mi OK. Reglas: el programa va en apis/, la clave la lee del .env con el nombre que me digas (no me la pidas ni leas el .env), solo lectura si alcanza, con una opción --ver que muestre lo que haría sin hacerlo, y nada se envía, borra ni paga sin mi OK. Antes del commit, corré herramientas/revisar_repo.py.
```

**Google (Gmail, Calendar, Drive):** casi siempre conviene el **conector** de tu IA. Si un programa propio necesita la API de Google, los archivos `credentials.json` y `token.json` son llaves: el `.gitignore` ya los deja fuera de GitHub.
