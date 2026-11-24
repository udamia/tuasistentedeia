"""Revisa que tu cerebro esté bien armado y que no haya claves antes de subirlo a GitHub.

Uso: python herramientas/revisar_repo.py   (en Mac: python3)
Solo lee: no cambia nada. Al final dice TODO BIEN o la lista de lo que hay que mirar.

Revisa:
- Que estén AGENTS.md, CLAUDE.md (con @AGENTS.md) y .gitignore (con .env y clientes-privado/).
- Cada Skill: carpeta con SKILL.md, encabezado con name y description, y name igual a la carpeta.
- Que las Skills de .claude/skills (Claude Code) y .agents/skills (Codex) sean las mismas.
- Cada subagente de .claude/agents: encabezado con name y description.
- Que .claude/settings.json sea un JSON válido.
- Que ningún archivo tenga algo con forma de clave o token.
- Que no haya un .env fuera del .gitignore.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALTEAR = {".git", "__pycache__", "clientes-privado", "secretos"}
CLAVES = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"), "clave de Anthropic"),
    (re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{32,}"), "clave de OpenAI"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "clave de Google"),
    (re.compile(r"\b\d{8,10}:[A-Za-z0-9_\-]{35}\b"), "token de Telegram"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "token de GitHub"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "clave privada"),
]


def encabezado(texto):
    m = re.match(r"^---\n(.*?)\n---\n", texto.replace("\r\n", "\n"), flags=re.S)
    if not m:
        return None
    campos = {}
    for linea in m.group(1).splitlines():
        if ":" in linea:
            k, v = linea.split(":", 1)
            campos[k.strip()] = v.strip()
    return campos


def archivos():
    for p in RAIZ.rglob("*"):
        if p.is_file() and not (set(p.relative_to(RAIZ).parts) & SALTEAR):
            yield p


def main():
    avisos = []
    rel = lambda p: p.relative_to(RAIZ).as_posix()

    for nombre in ("AGENTS.md", "CLAUDE.md", ".gitignore", "README.md"):
        if not (RAIZ / nombre).exists():
            avisos.append(f"Falta {nombre}")
    if (RAIZ / "CLAUDE.md").exists() and "@AGENTS.md" not in (RAIZ / "CLAUDE.md").read_text(encoding="utf-8-sig"):
        avisos.append("CLAUDE.md no importa @AGENTS.md: Claude Code no va a leer tu manual")
    gi = (RAIZ / ".gitignore").read_text(encoding="utf-8-sig").splitlines() if (RAIZ / ".gitignore").exists() else []
    for debe in (".env", "clientes-privado/", "CLAUDE.local.md"):
        if debe not in gi:
            avisos.append(f".gitignore no tiene «{debe}»")

    skills = {}
    for carpeta in (".claude/skills", ".agents/skills"):
        base = RAIZ / carpeta
        skills[carpeta] = {}
        if not base.exists():
            avisos.append(f"Falta la carpeta {carpeta}")
            continue
        for d in sorted(x for x in base.iterdir() if x.is_dir()):
            sk = d / "SKILL.md"
            if not sk.exists():
                avisos.append(f"{rel(d)}: falta SKILL.md")
                continue
            texto = sk.read_text(encoding="utf-8-sig")
            cab = encabezado(texto)
            if cab is None:
                avisos.append(f"{rel(sk)}: falta el encabezado entre las dos líneas de guiones")
                continue
            if cab.get("name") != d.name:
                avisos.append(f"{rel(sk)}: name «{cab.get('name')}» no es igual a la carpeta «{d.name}»")
            if not cab.get("description"):
                avisos.append(f"{rel(sk)}: falta description (es lo que le dice cuándo usarla)")
            cuerpo = texto.split("---", 2)[-1].strip()
            skills[carpeta][d.name] = cuerpo
    a, b = skills.get(".claude/skills", {}), skills.get(".agents/skills", {})
    for nombre in sorted(set(a) ^ set(b)):
        avisos.append(f"La Skill «{nombre}» está solo en una de las dos carpetas (.claude/skills y .agents/skills)")
    for nombre in sorted(set(a) & set(b)):
        if a[nombre] != b[nombre]:
            avisos.append(f"La Skill «{nombre}» dice distinto en .claude/skills y en .agents/skills")

    base = RAIZ / ".claude/agents"
    for f in sorted(base.glob("*.md")) if base.exists() else []:
        cab = encabezado(f.read_text(encoding="utf-8-sig"))
        if not cab or not cab.get("name") or not cab.get("description"):
            avisos.append(f"{rel(f)}: el subagente necesita name y description en el encabezado")
        elif cab["name"] != f.stem:
            avisos.append(f"{rel(f)}: name «{cab['name']}» no es igual al nombre del archivo")

    ajustes = RAIZ / ".claude/settings.json"
    if ajustes.exists():
        try:
            json.loads(ajustes.read_text(encoding="utf-8-sig"))
        except ValueError as e:
            avisos.append(f".claude/settings.json no es un JSON válido: {e}")

    for p in archivos():
        if p.name == ".env" or (p.name.startswith(".env.") and p.name != ".env.ejemplo"):
            # El .env tiene tus claves a propósito: está bien en tu compu si .gitignore lo deja afuera.
            if ".env" not in gi:
                avisos.append(f"Hay un {rel(p)} y .gitignore no lo deja afuera: se subiría a GitHub")
            continue
        if p.suffix.lower() not in {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".csv", ".env", ""} and not p.name.startswith(".env"):
            continue
        try:
            texto = p.read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, OSError):
            continue
        for patron, que in CLAVES:
            if patron.search(texto):
                avisos.append(f"{rel(p)}: parece tener una {que}. Sacala y guardala en .env")

    total = sum(1 for _ in archivos())
    print(f"Revisé {total} archivos · Skills: {len(a)} (Claude Code) y {len(b)} (Codex) · Subagentes: {len(list(base.glob('*.md'))) if base.exists() else 0}")
    if avisos:
        print(f"\nPara mirar ({len(avisos)}):")
        for x in avisos:
            print(" -", x)
        return 1
    print("TODO BIEN: no hay claves y todo está bien armado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
