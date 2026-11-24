"""Manda un aviso corto a tu Telegram. Lo usan tus tareas programadas al terminar.

Uso (en Mac, escribí python3 en lugar de python):
    python telegram/avisar.py --configurar     la primera vez: guarda el token y tu chat en el .env
    python telegram/avisar.py "Resumen del lunes listo: está en trabajos/lunes.md"
    python telegram/avisar.py --ver "texto"    muestra lo que mandaría, sin mandar nada
    python telegram/avisar.py --mi-chat        muestra el número de tu chat (escribile antes al bot)

Lee TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID de las variables de tu computadora o del archivo
.env de la carpeta principal. El .env no se sube a GitHub (está en .gitignore).
Usá un bot solo para avisos, distinto del bot del canal de Claude Code: si los dos usan el
mismo bot, Telegram no deja leer los mensajes a la vez.
Nunca escribas el token en este archivo. Nunca mandes claves ni datos de clientes.
Solo usa lo que trae Python: no hay que instalar nada.
"""
import getpass
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENV = RAIZ / ".env"
LARGO_MAXIMO = 1000


def leer_env():
    valores = {}
    if ENV.exists():
        # utf-8-sig: el Bloc de notas a veces guarda con una marca invisible al principio.
        for linea in ENV.read_text(encoding="utf-8-sig").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                clave, valor = linea.split("=", 1)
                valores[clave.strip()] = valor.strip().strip('"').strip("'")
    for clave in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        if os.environ.get(clave):
            valores[clave] = os.environ[clave]
    return valores


def guardar_env(nuevos):
    """Escribe o reemplaza las líneas de nuevos en el .env, sin tocar las demás."""
    lineas = ENV.read_text(encoding="utf-8-sig").splitlines() if ENV.exists() else []
    pendientes = dict(nuevos)
    salida = []
    for linea in lineas:
        clave = linea.split("=", 1)[0].strip() if "=" in linea and not linea.strip().startswith("#") else None
        if clave in pendientes:
            salida.append(f"{clave}={pendientes.pop(clave)}")
        else:
            salida.append(linea)
    salida += [f"{k}={v}" for k, v in pendientes.items()]
    ENV.write_text("\n".join(salida) + "\n", encoding="utf-8")


def llamar(token, metodo, datos=None):
    url = f"https://api.telegram.org/bot{token}/{metodo}"
    cuerpo = urllib.parse.urlencode(datos).encode() if datos else None
    try:
        with urllib.request.urlopen(url, data=cuerpo, timeout=20) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            detalle = json.loads(e.read().decode()).get("description", "")
        except ValueError:
            detalle = ""
        if e.code == 401:
            return {"ok": False, "description": "el token no es válido. Pedí uno nuevo a @BotFather con /token."}
        if e.code == 409:
            return {"ok": False, "description": "ese bot ya lo está leyendo otro programa (¿el canal de Claude Code?). Usá un bot solo para avisos."}
        return {"ok": False, "description": detalle or f"error {e.code}"}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"ok": False, "description": f"no pude conectarme a Telegram ({e}). Revisá internet."}


def buscar_chats(token):
    respuesta = llamar(token, "getUpdates")
    if not respuesta.get("ok"):
        print("Telegram no respondió bien:", respuesta.get("description"))
        return None
    return {u["message"]["chat"]["id"] for u in respuesta.get("result", []) if "message" in u}


def configurar():
    print("Configuración del aviso. El token no se muestra mientras lo pegás y queda solo en tu .env.")
    token = getpass.getpass("Pegá el token de tu bot de avisos (te lo dio @BotFather) y tocá Enter: ").strip()
    if not token:
        print("No pegaste nada. Volvé a correrlo cuando tengas el token.")
        return 1
    input("Ahora escribile «hola» a ese bot desde Telegram y tocá Enter acá... ")
    chats = buscar_chats(token)
    if chats is None:
        return 1
    if len(chats) != 1:
        print("No encontré un solo chat. Escribile «hola» al bot (solo vos) y volvé a correrlo.")
        return 1
    guardar_env({"TELEGRAM_BOT_TOKEN": token, "TELEGRAM_CHAT_ID": str(chats.pop())})
    print("Listo: guardé el token y tu chat en el .env. Probalo con: python telegram/avisar.py \"Hola\"")
    return 0


def main(args):
    if not args:
        print(__doc__)
        return 1
    if args[0] == "--configurar":
        return configurar()
    ver = args[0] == "--ver"
    if ver:
        args = args[1:]
        if not args:
            print("Escribí el aviso entre comillas después de --ver.")
            return 1
    env = leer_env()
    token = env.get("TELEGRAM_BOT_TOKEN", "")
    if args[0] == "--mi-chat":
        if not token:
            print("Falta TELEGRAM_BOT_TOKEN en tu .env. Corré: python telegram/avisar.py --configurar")
            return 1
        chats = buscar_chats(token)
        if chats is None:
            return 1
        if not chats:
            print("No encontré mensajes. Escribile «hola» a tu bot y volvé a correrlo.")
            return 1
        print("Tu número de chat:", ", ".join(str(c) for c in chats))
        return 0
    texto = " ".join(args).strip()[:LARGO_MAXIMO]
    if not texto:
        print("Escribí el aviso entre comillas.")
        return 1
    if ver:
        print("Mandaría:", texto)
        print("Token cargado:", "sí" if token else "no", "· Chat cargado:", "sí" if env.get("TELEGRAM_CHAT_ID") else "no")
        return 0
    chat = env.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat:
        print("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en tu .env. Corré: python telegram/avisar.py --configurar")
        return 1
    respuesta = llamar(token, "sendMessage", {"chat_id": chat, "text": texto})
    print("Aviso enviado." if respuesta.get("ok") else f"Telegram no lo aceptó: {respuesta.get('description')}")
    return 0 if respuesta.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
