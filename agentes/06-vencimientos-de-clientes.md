# Agente 06 · Vencimientos de clientes

Para contadores, consultores y agencias con clientes fijos · **Forma:** Despertador · **App y plan mínimo:** Claude de pago, con Drive y Gmail

## La ficha

| | |
|---|---|
| Qué mira | La planilla de vencimientos. |
| Nunca | cambia la planilla ni envía. |
| Dónde te deja el resultado | La lista de la semana y los recordatorios. |
| Cuándo te pide el OK | Antes de enviar, publicar, crear o cambiar cualquier cosa |

## La orden (cambiá los [corchetes])

```
Cada viernes a las 10, abrí la planilla [Vencimientos de clientes] en Google Drive (columnas: cliente, correo, qué vence, fecha). Haceme la lista, por fecha, de los vencimientos de la semana que viene. Para cada cliente prepará un recordatorio en borrador: saludo con su nombre, qué vence y cuándo, qué necesito y [para cuándo], y un agradecimiento. Máximo 5 renglones. Si una fecha no está clara, avisame y salteá ese recordatorio. No cambies la planilla y no envíes nada.
```

## Dónde lo programás

Con horario. En Claude: tarea programada desde el chat (Programadas > Nueva tarea) o en Claude Code (Scheduled > New task). En ChatGPT: un chat nuevo con el horario escrito en la orden. En Gemini: programaciones o Tarea. Mirá `tareas-programadas/LEEME.md`.

**Primero, una prueba a mano:** pegá la orden en un chat y cambiá el horario por «ahora» (o «tomá el último correo»). Si el resultado te sirve una semana, recién ahí la programás.

Vas a recibir: el viernes, la semana siguiente de un vistazo y los recordatorios listos. No reemplaza tu agenda de vencimientos: la acompaña.
