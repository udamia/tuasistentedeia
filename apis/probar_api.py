"""Prueba tu clave de API de Claude, OpenAI o Gemini con un pedido chiquito.

Uso (en Mac, escribí python3 en lugar de python):
    python apis/probar_api.py --configurar claude      guarda tu clave en el .env (no se ve al pegarla)
    python apis/probar_api.py --ver claude             dice si encontró la clave y qué modelo usa, sin gastar
    python apis/probar_api.py claude "Decime en una frase qué es una API"
    (en lugar de claude: openai o gemini)

Lee la clave del archivo .env de la carpeta principal (ANTHROPIC_API_KEY, OPENAI_API_KEY o
GEMINI_API_KEY) y el modelo de MODELO_CLAUDE, MODELO_OPENAI o MODELO_GEMINI (mirá .env.ejemplo).
Claude: creá la clave dentro de un espacio de trabajo. Si es una clave sin espacio, completá
ANTHROPIC_WORKSPACE_ID (el ID wrkspc_... de la página Workspaces de la Consola).
El .env no se sube a GitHub (está en .gitignore). Este programa NUNCA muestra la clave.
Cada pedido gasta crédito de tu cuenta de API: poné un tope antes (capítulo 17 del libro).
Solo usa lo que trae Python: no hay que instalar nada.
"""
import getpass
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENV = RAIZ / ".env"
# Tope de lo que puede escribir cada respuesta. Los modelos de hoy «piensan» antes de contestar
# y ese pensamiento cuenta dentro de este tope: con menos, la respuesta puede llegar cortada.
MAX_TOKENS = 4000

EMPRESAS = {
    "claude": {"clave": "ANTHROPIC_API_KEY", "modelo": "MODELO_CLAUDE", "por_defecto": "claude-haiku-5-5",
               "consola": "platform.claude.com (API keys, Billing y Spend limits)"},
    "openai": {"clave": "OPENAI_API_KEY", "modelo": "MODELO_OPENAI", "por_defecto": "gpt-6-luna",
               "consola": "platform.openai.com (API keys, Billing y Limits)"},
    "gemini": {"clave": "GEMINI_API_KEY", "modelo": "MODELO_GEMINI", "por_defecto": "gemini-4-hydrogen",
               "consola": "aistudio.google.com (API keys, Billing y Spend)"},
}


def leer_env():
    """Lee solo el .env de esta carpeta (no las variables de la computadora, a propósito:
    así Claude Code sigue usando tu plan y no una clave de API)."""
    valores = {}
    if ENV.exists():
        for linea in ENV.read_text(encoding="utf-8-sig").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                k, v = linea.split("=", 1)
                valores[k.strip()] = v.strip().strip('"').strip("'")
    return valores


def guardar_env(nuevos):
    """Escribe o reemplaza esas líneas del .env, sin tocar las demás."""
    lineas = ENV.read_text(encoding="utf-8-sig").splitlines() if ENV.exists() else []
    pendientes = dict(nuevos)
    salida = []
    for linea in lineas:
        sin_numeral = linea.strip().lstrip("#").strip()
        clave = sin_numeral.split("=", 1)[0].strip() if "=" in sin_numeral else None
        if clave in pendientes:
            salida.append(f"{clave}={pendientes.pop(clave)}")
        else:
            salida.append(linea)
    salida += [f"{k}={v}" for k, v in pendientes.items()]
    ENV.write_text("\n".join(salida) + "\n", encoding="utf-8")


def pedido_http(url, cabeceras, cuerpo):
    datos = json.dumps(cuerpo).encode("utf-8")
    req = urllib.request.Request(url, data=datos, headers={"content-type": "application/json", **cabeceras})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return 200, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8"))
        except ValueError:
            return e.code, {}
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, {"error": {"message": f"no pude conectarme ({e}). Revisá internet."}}


def preguntar(empresa, clave, modelo, texto, espacio=""):
    """Devuelve (código, respuesta en texto, tokens leídos, tokens escritos, mensaje de error).
    espacio: el ID del espacio de trabajo de Claude (wrkspc_...), solo si tu clave no tiene uno."""
    if empresa == "claude":
        cabeceras = {"x-api-key": clave, "anthropic-version": "2026-10-21"}
        if espacio:
            cabeceras["anthropic-workspace-id"] = espacio
        cod, r = pedido_http("https://api.anthropic.com/v1/messages", cabeceras,
                             {"model": modelo, "max_tokens": MAX_TOKENS,
                              "messages": [{"role": "user", "content": texto}]})
        if cod == 200:
            salida = "".join(b.get("text", "") for b in r.get("content", []) if b.get("type") == "text")
            u = r.get("usage", {})
            return cod, salida, u.get("input_tokens"), u.get("output_tokens"), ""
    elif empresa == "openai":
        cod, r = pedido_http("https://api.openai.com/v1/responses",
                             {"Authorization": f"Bearer {clave}"},
                             {"model": modelo, "input": texto, "max_output_tokens": MAX_TOKENS})
        if cod == 200:
            salida = r.get("output_text") or "".join(
                c.get("text", "") for o in r.get("output", []) for c in o.get("content", []) or []
                if c.get("type") == "output_text")
            u = r.get("usage", {})
            return cod, salida, u.get("input_tokens"), u.get("output_tokens"), ""
    else:
        cod, r = pedido_http("https://generativelanguage.googleapis.com/v1beta/interactions",
                             {"x-goog-api-key": clave, "Api-Revision": "2026-05-20"},
                             {"model": modelo, "input": texto})
        if cod == 200:
            # La respuesta trae «steps»: el texto está en los pasos de tipo «model_output».
            pasos = [p for p in r.get("steps") or [] if isinstance(p, dict) and p.get("type") == "model_output"]
            salida = r.get("output_text") or texto_de(pasos) or texto_de(r.get("outputs") or [])
            u = r.get("usage", {}) or {}
            return cod, salida, u.get("total_input_tokens") or u.get("input_tokens"), \
                u.get("total_output_tokens") or u.get("output_tokens"), ""
    error = r.get("error")
    if isinstance(error, dict):
        # El mensaje y, si viene, el código de la empresa (por ejemplo, project_spend_limit_exceeded).
        codigos = [str(error.get("code") or ""), str((error.get("details") or {}).get("error_code") or "")
                   if isinstance(error.get("details"), dict) else ""]
        detalle = " ".join([str(error.get("message") or "")] + [c for c in codigos if c]).strip()
    else:
        detalle = str(error or "")
    return cod, "", None, None, detalle


def texto_de(partes):
    """Junta el texto de una respuesta, venga como venga (lista de partes con 'text')."""
    out = []
    for p in partes if isinstance(partes, list) else [partes]:
        if isinstance(p, dict):
            if isinstance(p.get("text"), str):
                out.append(p["text"])
            for k in ("content", "parts"):
                if k in p:
                    out.append(texto_de(p[k]))
    return "".join(out)


def explicar(cod, detalle, empresa):
    consola = EMPRESAS[empresa]["consola"]
    bajo = detalle.lower()
    if cod == 401 or cod == 403:
        return f"La clave no es válida, venció o la borraste ({cod}). Creá otra en {consola} y guardala con --configurar."
    if "workspace" in bajo and "limit" not in bajo:
        return ("Tu clave de Claude no tiene un espacio de trabajo. Lo más fácil: creá otra clave y, al crearla, "
                "elegí el espacio (Default o el de tu programa). Mirá apis/LEEME.md.")
    if cod == 402 or "credit" in bajo or "billing" in bajo:
        return f"No hay crédito o falta la facturación. Mirá Billing en {consola}."
    if "spend" in bajo or "usage limit" in bajo:
        return f"Llegaste a un tope de gasto (el tuyo o el de tu cuenta). Mirá los límites de gasto en {consola}."
    if cod == 404 or "model" in bajo:
        return ("El modelo no existe o cambió de nombre. Mirá la lista de modelos de la empresa y cambiá "
                f"la línea {EMPRESAS[empresa]['modelo']} de tu .env.")
    if cod == 429:
        return "Demasiados pedidos o cupo alcanzado (429). Esperá un minuto y probá de nuevo."
    if cod == 0:
        return detalle
    return f"Error {cod}: {detalle[:300]}"


def main(args):
    if not args or args[0] in ("-h", "--ayuda"):
        print(__doc__)
        return 1
    if args[0] == "--configurar":
        empresa = (args[1] if len(args) > 1 else "").lower()
        if empresa not in EMPRESAS:
            print("Decime cuál: --configurar claude, --configurar openai o --configurar gemini")
            return 1
        nombre = EMPRESAS[empresa]["clave"]
        clave = getpass.getpass(f"Pegá tu clave de {empresa} (no se ve mientras la pegás) y tocá Enter: ").strip()
        if not clave:
            print("No pegaste nada. Volvé a correrlo cuando tengas la clave.")
            return 1
        guardar_env({nombre: clave})
        print(f"Listo: guardé {nombre} en tu .env (no se sube a GitHub). Probala con: python apis/probar_api.py {empresa} \"Hola\"")
        return 0
    ver = args[0] == "--ver"
    if ver:
        args = args[1:]
    empresa = (args[0] if args else "").lower()
    if empresa not in EMPRESAS:
        print("Elegí la empresa: claude, openai o gemini. Ejemplo: python apis/probar_api.py claude \"Hola\"")
        return 1
    env = leer_env()
    datos = EMPRESAS[empresa]
    clave = env.get(datos["clave"], "")
    modelo = env.get(datos["modelo"]) or datos["por_defecto"]
    if ver:
        print(f"Empresa: {empresa} · Clave {datos['clave']} en el .env: {'sí' if clave else 'no'} · Modelo: {modelo}")
        print("No mandé nada: con --ver no se gasta.")
        return 0 if clave else 1
    if not clave:
        print(f"No encontré {datos['clave']} en tu .env. Corré: python apis/probar_api.py --configurar {empresa}")
        return 1
    texto = " ".join(args[1:]).strip() or "Decime en una frase qué es una API."
    cod, salida, entrada, salida_tok, detalle = preguntar(empresa, clave, modelo, texto,
                                                          env.get("ANTHROPIC_WORKSPACE_ID", ""))
    if cod != 200:
        print("No funcionó:", explicar(cod, detalle, empresa))
        return 1
    print(salida.strip() or "(La respuesta llegó vacía o cortada: probá con un pedido más corto.)")
    print(f"\n[{empresa} · {modelo} · leyó {entrada if entrada is not None else '?'} tokens · escribió {salida_tok if salida_tok is not None else '?'} tokens]")
    print(f"Mirá el gasto en {datos['consola']}.")
    return 0


if __name__ == "__main__":
    try:  # en Windows, que una letra rara de la respuesta no corte el programa
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    sys.exit(main(sys.argv[1:]))
