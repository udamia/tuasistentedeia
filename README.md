# Tu Primer Asistente con IA · el repositorio

Este repositorio es **tu cerebro listo para usar**: una carpeta con todo armado para que Claude Code (o Codex) trabaje como tu asistente desde el primer día. Acompaña al libro «Tu Primer Asistente con IA».

No hace falta saber programar. Seguí los pasos en orden.

---

## Qué trae

| Carpeta o archivo | Qué es | Lo tocás… |
|---|---|---|
| `AGENTS.md` | **El manual de tu asistente.** Quién sos, cómo te habla, qué no hace nunca y dónde está cada cosa. Lo leen Codex y Claude Code | El primer día, para cambiar los [corchetes] |
| `CLAUDE.md` | Una sola línea que le dice a Claude Code «leé AGENTS.md», más lo propio de Claude | Casi nunca |
| `contexto/` | Tu información: quién sos, tu negocio, tus prioridades, cómo escribís | El primer día (con la entrevista) y una vez por mes |
| `referencias/` | Listas de precios, plantillas, documentos de consulta | Cuando cambian |
| `decisiones/registro.md` | Qué se decidió y por qué. Solo se agrega al final | Cada vez que decidís algo importante |
| `memoria/lecciones.md` | Las reglas que salieron de tus correcciones | Lo llena tu asistente, con tu OK |
| `trabajos/` | Lo que va produciendo tu asistente | Lo leés vos |
| `archivo/` | Lo viejo. Nada se borra: se mueve acá | Cuando ordenás |
| `asistentes/` | **20 asistentes** listos (correos, clientes, presupuestos, trámites, menú, viajes…) | Elegís uno y lo usás |
| `agentes/` | **15 agentes** listos, cada uno con su ficha y su orden | Elegís uno y lo programás |
| `tareas-programadas/` | Plantillas de tareas con horario, para Claude, ChatGPT, Gemini o Grok | Cuando querés que algo corra solo |
| `.claude/skills/` | **Skills** (métodos paso a paso) para Claude Code | Cuando sumás un método |
| `.agents/skills/` | Las mismas Skills, para Codex | Igual que la anterior: van juntas |
| `.claude/agents/` | **4 subagentes**: revisor de borradores, investigador, ordenador de facturas y revisor de reglas | Cuando sumás un especialista |
| `telegram/` | Cómo hablarle desde Telegram y un aviso al celular | Cuando llegás al capítulo de Telegram |
| `herramientas/revisar_repo.py` | Un control que revisa que todo esté bien armado y que no haya claves | Antes de cada «push» |
| `.gitignore` | La lista de lo que **nunca** se sube a GitHub (claves, datos de clientes) | Nunca lo borres |
| `.claude/settings.json` | Le prohíbe a Claude Code leer tus claves (el `.env` y la carpeta `secretos/`) | Nunca lo borres |

---

## Empezá acá: 5 pasos

### 1. Hacé tu copia privada

Si estás en GitHub, arriba de la lista de archivos tocá **Use this template > Create a new repository**. Elegí tu cuenta, ponele de nombre `mi-cerebro` y marcá **Private** (privado). Tocá **Create repository from template**.

> Tu copia es tuya: lo que cambies ahí no toca este repositorio.

### 2. Bajala a tu computadora

Con **GitHub Desktop**: **File > Clone Repository…**, elegí `mi-cerebro` y tocá **Clone**. Queda en `Documentos\GitHub\mi-cerebro`.

### 3. Abrila con tu asistente

- **Claude Code** (plan pago de Claude): abrí la app de Claude, pestaña **Code**, y elegí la carpeta `mi-cerebro`. O en la terminal: `cd` a la carpeta y `claude`.
- **Codex** (cuenta de ChatGPT, también la gratis con límites): abrí la app de ChatGPT en la computadora, elegí **Codex** en el menú y abrí la carpeta `mi-cerebro`. También anda con el Codex CLI o la extensión para tu editor.

### 4. Hacé la entrevista

Pegale esto:

```
Leé AGENTS.md y la carpeta contexto. Entrevistame de a una pregunta por vez para llenar los archivos de contexto y cambiar los [corchetes] de AGENTS.md. Mostrame cada archivo antes de guardarlo y esperá mi OK.
```

Lleva unos 30 minutos. Es lo que hace que piense como vos.

### 5. Guardá y probá

En GitHub Desktop: escribí un mensaje en **Summary** (por ejemplo, «Mi contexto»), tocá **Commit to main** y después **Push origin**.

Cerrá y volvé a abrir tu asistente. Preguntale: «¿Qué sabés de mí y de mi trabajo?». Si responde como vos, tu cerebro funciona.

---

## Cómo se usa cada cosa

- **Un asistente de la carpeta `asistentes/`:** «Usá asistentes/02-atencion-al-cliente.md y respondé este reclamo: […]». También podés copiar su texto en un Proyecto de ChatGPT, Claude o Grok, o en una Habilidad de Gemini.
- **Un agente de la carpeta `agentes/`:** abrí su archivo, completá los [corchetes] y seguí «Dónde lo programás». Primero probalo una vez, a mano.
- **Una Skill:** en Claude Code, escribí `/` y su nombre (`/resumen-semanal`). En Codex, pedila por su nombre («Usá la skill resumen-semanal») o buscala en **Skills**, en la barra de la izquierda; en la terminal, con `$resumen-semanal`. También podés pedir algo con tus palabras: la usa sola si encaja.
- **Un subagente:** «Usá el revisor-de-borradores con los correos de hoy».

---

## Las reglas que no se negocian (ya están en AGENTS.md)

1. Lo que envía, borra, publica o paga, lo aprobás vos.
2. Los correos a clientes quedan en borrador.
3. **Nunca** claves, contraseñas ni tokens en esta carpeta. Van en un archivo `.env` que **no se sube** (mirá `.env.ejemplo`).
4. Los datos reales de clientes van en `clientes-privado/`, que tampoco se sube.
5. Lo viejo no se borra: se mueve a `archivo/`.

---

## Antes de cada push

Pedile a tu asistente: «Corré herramientas/revisar_repo.py con Python y mostrame el resultado». Si preferís hacerlo vos, en la terminal, dentro de la carpeta:

```
python herramientas/revisar_repo.py
```

(En Mac, `python3`. Si te dice que no encuentra Python, instalalo desde python.org; en Windows, tildá «Add python.exe to PATH». O pedile a tu asistente que te guíe.)

Si dice **TODO BIEN**, subí. Si avisa algo, leelo: casi siempre es una clave pegada donde no va o un [corchete] sin completar.

---

## Si algo no funciona

| Si pasa… | Probá así |
|---|---|
| Claude Code no lee mis reglas | Abrilo **dentro** de la carpeta `mi-cerebro`, no en la de arriba |
| `/` no muestra mis Skills | Fijate que cada una esté en `.claude/skills/<nombre>/SKILL.md` y que `name` sea igual al nombre de la carpeta |
| Codex no ve las Skills | Tienen que estar también en `.agents/skills/` |
| GitHub Desktop quiere subir un `.env` | No lo subas. Revisá que `.gitignore` siga en la carpeta |
| Dice que no encuentra `python` | Instalá Python desde python.org (en Windows, tildá «Add python.exe to PATH»). En Mac, escribí `python3` |
| No sé qué hizo mi asistente | Preguntale: «Contame qué hiciste esta semana, en una tabla corta» |

Las apps cambian seguido: si un botón tiene otro nombre, buscá el parecido. Lo importante de esta carpeta (el manual, tu contexto, tus métodos) sirve igual.
