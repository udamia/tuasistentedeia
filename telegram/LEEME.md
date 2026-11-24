# Telegram: hablale a tu cerebro desde el celular

Hay dos formas. Empezá por la primera.

| | Para qué | Qué necesita |
|---|---|---|
| **1 · El canal de Claude Code** | Le escribís al bot y te contesta tu cerebro, con tus archivos y tus reglas | Plan pago de Claude, Claude Code abierto con el canal y la computadora prendida |
| **2 · El aviso** (`avisar.py`) | Una tarea programada te manda un mensaje al terminar: «Resumen listo» | Python en tu computadora y **otro bot**, solo para avisos, con su token en tu `.env` |

---

## 1 · El canal de Claude Code (en prueba)

**Paso 1 · Creá el bot.** En Telegram, buscá **@BotFather** (con el tilde azul), escribí `/newbot`, elegí un nombre y un usuario que termine en `bot`. Te da un **token**: cualquiera que lo tenga controla tu bot. No lo pegues en ningún chat ni en este repositorio.

**Paso 2 · Instalá el canal.** Necesitás Bun instalado (pedíselo a Claude Code: «Instalá Bun en mi computadora y explicame qué es»). Después, dentro de Claude Code:

```
/plugin install telegram@claude-plugins-official
```

Si te dice «Run /reload-plugins to apply», escribí `/reload-plugins`.

**Paso 3 · Dale el token.**

```
/telegram:configure <tu-token>
```

El token queda guardado en tu computadora, fuera de esta carpeta.

**Paso 4 · Abrí Claude Code con el canal.** Salí con `/exit` y, en la terminal, dentro de tu carpeta:

```
claude --channels plugin:telegram@claude-plugins-official
```

**Paso 5 · Emparejá tu Telegram.** Escribile cualquier cosa a tu bot. Te responde un código. En Claude Code:

```
/telegram:access pair <código>
```

**Paso 6 · Cerrá la puerta.** Que solo te conteste a vos:

```
/telegram:access policy allowlist
```

**Para tener en cuenta:**

- Los mensajes llegan **solo mientras esa sesión está abierta** y la computadora prendida.
- Quien esté en la lista de permitidos puede aprobar o negar permisos: solo vos (o alguien de mucha confianza).
- Si el bot no contesta, te faltó abrir con `--channels`.
- Si el token se filtró: en @BotFather, `/token` te da uno nuevo y el viejo deja de andar.

---

## 2 · El aviso al celular (`avisar.py`)

Sirve para que una tarea que corre en tu computadora te avise cuando termina.

1. **Creá un bot nuevo solo para avisos** con @BotFather (como en el paso 1 de arriba). Si usás el mismo bot del canal, Telegram no deja que los dos lo lean a la vez.
2. **Abrí la terminal vos** (no se lo pidas a Claude Code: así el token no pasa por ningún chat), entrá a tu carpeta con `cd` y escribí:

```
python telegram/avisar.py --configurar
```

   (En Mac, `python3`.) Pegá el token cuando te lo pida (no se ve mientras lo pegás), escribile «hola» al bot nuevo desde Telegram y tocá Enter. El programa guarda el token y tu número de chat en el archivo `.env`, que no se sube a GitHub.
3. Probalo sin mandar nada: `python telegram/avisar.py --ver "Hola, soy tu cerebro"`.
4. Mandalo de verdad: `python telegram/avisar.py "Hola, soy tu cerebro"`.

Si te dice que no encuentra Python, instalalo desde python.org (en Windows, tildá «Add python.exe to PATH»).

En una tarea programada, sumá al final de la orden: «Cuando termines, corré `python telegram/avisar.py "<resumen en una línea>"`».

**Lo que nunca va por Telegram:** claves, contraseñas, datos de clientes. El aviso dice «listo, está en trabajos/», no el contenido.
