# Agente 07 · Facturas por cobrar

Para oficios, consultores y empresas chicas · **Forma:** Despertador · **App y plan mínimo:** Claude de pago, con Drive y Gmail

## La ficha

| | |
|---|---|
| Qué mira | La planilla de facturas emitidas. |
| Nunca | envía ni toca el banco o la facturación electrónica. |
| Dónde te deja el resultado | Las vencidas, el total y los recordatorios. |
| Cuándo te pide el OK | Antes de enviar, publicar, crear o cambiar cualquier cosa |

## La orden (cambiá los [corchetes])

```
Cada jueves a las 9, abrí la planilla [Facturas emitidas] en Google Drive (columnas: cliente, correo, número, monto, vencimiento, estado). Buscá las facturas «por cobrar» vencidas hace al menos [7] días. Para cada una prepará un recordatorio de pago en borrador: saludo con su nombre, número, monto y vencimiento, una frase amable y mi contacto para dudas. Máximo 5 renglones, nunca en tono duro. No escribas datos bancarios: los agrego yo. No cambies la planilla y no envíes nada. Al final, decime el total.
```

## Dónde lo programás

Con horario. En Claude: tarea programada desde el chat (Programadas > Nueva tarea) o en Claude Code (Scheduled > New task). En ChatGPT: un chat nuevo con el horario escrito en la orden. En Gemini: programaciones o Tarea. Mirá `tareas-programadas/LEEME.md`.

**Primero, una prueba a mano:** pegá la orden en un chat y cambiá el horario por «ahora» (o «tomá el último correo»). Si el resultado te sirve una semana, recién ahí la programás.

Vas a recibir: las facturas vencidas, el total por cobrar y un recordatorio cordial para cada una. ¿Un cliente con varias? Sumá: «Prepará un solo recordatorio con la lista de todas.»
