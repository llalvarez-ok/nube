# Dashboard en Excel con IA: el error de cada inicio de mes (ronda 2)

- **Pilar:** P1 · Excel + IA. La ficha (`canales/atajos-ia/ficha.md`, "Temas de RPM alto") incluye "dashboards e informes de gestión"; no hay una cifra de RPM con fuente para este tema y no la invento. · **Formato:** estructura **A (tutorial con cronómetro)** de `youtube/04` §5 (`04` solo define A, B y C). Los "pasos 1–3" son las 4 preguntas del dashboard. El "paso secreto" es la Prueba sobre el dato "contra el mes anterior" (≈ 65 %). El resultado final es el dashboard rehaciéndose al pegar los pedidos nuevos. · **Duración objetivo:** 9,5 min (rango 9–11), con un corte de anuncios en 5:00, entre la pregunta 2 y la 3.
- **Palabra clave principal:** `dashboard en excel con ia`. Va al principio de todos los títulos, menos el A/B 3 condicional.
- **Búsquedas relacionadas (no salen de `investigar.py sugerencias`, que volvió a dar 403 el 26/10/2026):**
  - Consultas medidas con la API: `dashboard en excel` (oportunidad 79) y `tabla dinamica con ia` (62; devuelve sobre todo dashboards con IA).
  - Términos que se repiten en los títulos del top: `dashboard automático`, `dashboard con claude`, `dashboard interactivo en excel`, `plantilla dashboard excel gratis`.
  - Para capítulos y descripción (RPM): `informe de ventas en excel`, `reporte de ventas`, `cuentas por cobrar`, `Power BI` (en Límites).
  - Pendiente, sin bloquear: reintentar `investigar.py sugerencias` o Google Trends cuando el proxy lo permita.
- **Evidencia de demanda (API de YouTube, 26/10/2026, región MX, últimos 365 días; `sistema/investigacion/2026-10-26-video03.md` y `-datos.json`):**
  - `dashboard en excel` → **oportunidad 79**; `dashboard en excel con ia` → **oportunidad 65**. Ojo: el puntaje sale de 25 resultados, en su mayoría en inglés o hindi.
  - **Top en español sobre el tema: mediana de unas 137 mil vistas (n = 10), con 10 o más videos de 30 mil vistas o más en 12 meses.** Pasa con holgura el umbral acordado en video02.
  - Outliers: en español, el mejor es [Raymon Acuña, "¡Adiós a las horas en Excel! Dashboards automáticos con Gemini"](https://youtu.be/V1O-Z0dl5o0) (142 mil, **2,2x**). En inglés, [Vedakarna, "…Dashboard with ONE Prompt using Claude AI"](https://youtu.be/NsZg0sgUFzU) (515 mil, **8,2x**), [Easy Click Learning](https://youtu.be/MEfKQFYvCHw) (310 mil, **9,9x**) y [Marg Analytics](https://youtu.be/fhVXfSjLb6I) (233 mil, **45,7x**).
  - **Lectura honesta:**
    - En español, los videos del tema hacen **entre 500 y 1.600 vistas por día**: El Inge Francisco [1.613/día](https://youtu.be/f1pifDNhSzk), El Tío Tech [1.336](https://youtu.be/VVE2BfJ2cdg), EXCELeINFO [882](https://youtu.be/YtGfOEePKRU), Raymon Acuña [680](https://youtu.be/V1O-Z0dl5o0) y El Tío Tech con VBA [515](https://youtu.be/cjvQzxuaGlI).
    - Su ratio es de **0,0x a 0,5x**, salvo Raymon Acuña (2,2x), y **ninguno tiene menos de 60 días**.
    - La demanda existe, pero se la llevan canales de 188 mil a 2 millones de suscriptores.
    - **Expectativa:** por búsqueda, poco en las primeras semanas. El video depende del **CTR en sugeridos** (por eso el empaque principal es el giro, que no se parece a ninguna miniatura del top) y del **tráfico de video02** (tarjeta y pantalla final).
- **Por qué ahora:**
  1. Todos los videos del tema venden velocidad: "1 minuto", "al instante", "adiós a las horas". Ninguno habla de que el número más grande del tablero puede estar mal.
  2. Se publica el **martes 03/11/2026, día 3 del mes**: es exactamente la situación del giro. Igual, la voz nunca dice "hoy": dice "el día 3 de cada mes", y el giro funciona en cualquier fecha de publicación.
  3. Continuidad: video02 (26/10) dejó la planilla de Distribuidora Sur limpia y con la cobranza corregida. video03 es el paso siguiente: "los datos ya están limpios; ahora, el tablero del lunes".
- **Línea 1 de la descripción:** "Dashboard en Excel con IA: pegas los pedidos y se rehace solo, pero ojo con el error de cada inicio de mes que te muestra caídas de ventas que no existen. Gratis, en Excel para la web, sin macros ni tablas dinámicas."

## Ángulo propio: qué no tiene el top 5 en español

El top en español sobre dashboards con IA, ya revisado por el investigador con las descripciones de los videos:
- [El Tío Tech, "Dashboard en 1 minuto con Claude AI | 1 Clic + VBA"](https://youtu.be/cjvQzxuaGlI): VBA.
- [Raymon Acuña](https://youtu.be/V1O-Z0dl5o0): Gemini Canvas.
- [EXCELeINFO, "Claude ya puede crear dashboards que se actualizan solos"](https://youtu.be/YtGfOEePKRU): trabaja en Google Sheets.
- [Mundo Virtual Pro](https://youtu.be/Iz-44S4tHfU): Gemini y un conversor de pago.
- [El Inge Francisco, "el mejor prompt… ¿Claude SIRVE?"](https://youtu.be/1pJqarOwgbA): **falta revisarlo**. Es la condición del investigador: si en ese video se revisa la exactitud de un KPI por mes incompleto, el giro pierde exclusividad y el empaque principal se reevalúa.

Diferenciadores reales (solo dos, y el empaque vende el primero):
1. **El error de cada inicio de mes (el giro).** Con los datos al 03/11, el dato "ventas de este mes contra el anterior" da **−90,4 %**. Comparado con el mismo tramo de días da **+7,6 %**, y el último mes cerrado, **+8,6 %**. Ningún video del top revisa si el número del tablero es cierto. Es la firma 3 del canal (veredicto honesto) llevada al título.
2. **Un dashboard de Excel de verdad, que abre gratis y se rehace al pegar.** Usa fórmulas (SUMAR.SI.CONJUNTO, CONTAR.SI.CONJUNTO, FILTRAR) sobre una **Tabla de Excel**, 2 gráficos de barras y una **lista desplegable** como filtro, en **Excel para la web gratis**. Nada de VBA, Gemini Canvas, Google Sheets, conversores ni complementos de pago. "Pegas los pedidos y se rehace solo" se demuestra en pantalla dos veces (pregunta 1 y resultado final).

**Estructura, no diferenciador:** las 4 preguntas del lunes (EXCELeINFO ya vende "pedirle a Claude que analice antes de generar"), el método Mapa · Meta · Prueba, Distribuidora Sur como universo de la serie, Claude, "automático" y la plantilla gratis.

- **Promesa en una frase:** "Al final de este video vas a poder armar en Excel para la web, gratis y con una IA, un dashboard de ventas que se rehace solo cuando pegas los pedidos nuevos, y vas a saber detectar el error que cada inicio de mes te muestra una caída de ventas que no existe."
  - Sin "[N] minutos" en la promesa: la duración del armado todavía no se midió (condición del creador). Si se mide y da 30 min o menos, se suma "en [N] minutos". Si da más, la voz vende "lo armas una vez; cada lunes, pegar y listo".

## Restricciones heredadas de video02 (sin cambios)

- **Respuestas reales (regla 4).** Los prompts se corren en claude.ai con el plan gratuito y se guardan textuales, con fecha y captura, en `produccion/video03/respuestas-ia.md`. Solo así el rótulo dice "Claude · versión gratuita"; si no, dice "Claude". En 0:25: "uso Claude gratis; el mismo prompt sirve en ChatGPT o Copilot, y la respuesta puede cambiar: para eso está la Prueba". Lo que no se corra queda pendiente y no sale en el video.
- **Datos ficticios declarados** en la voz (en 0:25) y en la descripción. La base es reproducible: `fuente/datos_base.py`, con semilla fija y las 12 filas de video02.
- Excel en español con `;` y la nota del separador en México. Excel para la web gratis. Sin VBA, Power Query ni Power Pivot.
- **Plantilla gratis y sin registro.**
- **Fecha de corte fija en la demo: 03/11/2026, en `Dashboard!B1`.** La plantilla trae `=HOY()` con una nota.

## La base: "Distribuidora Sur, pedidos 2026" (ficticia, sin cambios)

250 pedidos entre el 02/01/2026 y el 02/11/2026, en una **Tabla de Excel** llamada `Pedidos`. Tiene las columnas de video02 ya limpias: Fecha, Cliente, Vendedor, Código, Cant., Precio, Desc., Neto, Vence, Pagado y Estado.

Las cifras salen de `python3 produccion/video03/fuente/datos_base.py` (Python, no Excel; hay que confirmarlas en Excel para la web):

| Dato | Valor |
|---|---|
| Ventas acumuladas del año al 03/11 | 46.586.220 (46.145.220 antes de pegar el pedido del 02/11) |
| Septiembre / octubre (meses cerrados) | 4.213.090 / 4.574.425 → **+8,6 %** |
| Noviembre al día 3 (1 pedido: Hotel Mirador, 02/11, 50 × LIM-040) | 441.000 |
| **Dato ingenuo "este mes contra el anterior"** | **−90,4 %** |
| Mismo tramo: del 1 al 3 de noviembre contra del 1 al 3 de octubre (409.900) | **+7,6 %** |
| Por vendedor, en el año | Diego Paz 17.318.115 · Carla Ruiz 16.253.850 · Tomás Gil 13.014.255 |
| Producto que más vende | LIM-040 Papel higiénico x48: 13.011.460 |
| Vencido sin cobrar (Estado corregido de video02) | 16 facturas, 2.951.090 |
| **Gráfico mensual, 12 meses fijos (enero–diciembre)** | 5.001.725 · 5.084.160 · 4.883.505 · 3.737.280 · 4.173.060 · 4.267.840 · 5.569.025 · 4.641.110 · 4.213.090 · 4.574.425 · **441.000** · 0 |
| **Pedidos de hoy (03/11) que se pegan en el resultado final** (función `pedidos_hoy()`, no son parte de los 250) | Colegio Nuevo Horizonte, 80 × PAP-200: 324.000 · Librería San Martín Srl, 60 × PAP-220: 210.600 · Kiosco La Esquina, 15 × LIM-010: 36.000 |
| Después de pegarlos | 253 pedidos · acumulado 47.156.820 · **barra de noviembre: 441.000 → 1.011.600** · mismo tramo: +7,6 % → **+146,8 %** · mes cerrado: sigue en **+8,6 %** |

El salto del mismo tramo a +146,8 % con 3 pedidos se usa a propósito en el resultado final: muestra que, con 3 días de datos, cualquier comparación es ruido, y por eso la tarjeta grande es la del mes cerrado. La semilla se eligió para que la tendencia real sea estable (+8 %). Es una decisión de guion sobre datos inventados.

## El dashboard: 4 preguntas, 4 bloques (hoja `Dashboard`)

| Bloque | Pregunta del lunes | Qué se ve | Fórmula base (Excel en español, `;`) |
|---|---|---|---|
| 1 | ¿Cuánto vendimos? | 3 tarjetas: acumulado del año, mes cerrado y cantidad de pedidos | `=SUMAR.SI.CONJUNTO(Pedidos[Neto];Pedidos[Fecha];">="&FECHA(AÑO(B1);1;1);Pedidos[Fecha];"<="&B1)` |
| 2 | ¿Vamos mejor o peor? | Tarjeta "contra el mes anterior" + gráfico de barras **de 12 meses fijos** (los futuros en 0) | Mes por mes: `=SUMAR.SI.CONJUNTO(Pedidos[Neto];Pedidos[Fecha];">="&FECHA(2026;n;1);Pedidos[Fecha];"<="&FIN.MES(FECHA(2026;n;1);0))`. Primero la variación ingenua (el giro); después, la del mismo tramo y la del mes cerrado |
| 3 | ¿Quién y qué vende? | Barras por vendedor y top 3 de productos, con la **lista desplegable** de vendedor | Criterio `Pedidos[Vendedor];SI(B2="Todos";"*";B2)`. La voz dice: "no tienes que memorizarla: la escribe la IA y está en la plantilla" |
| 4 | ¿Quién nos debe? | Lista de vencidos, ordenada (el FILTRAR de video02, ahora sobre la Tabla) | `=ORDENAR(FILTRAR(…;Pedidos[Estado]="Vencido";"Sin vencidos");…)` |

## Escaleta (≈ 9,5 min, estructura A)

| Min. | Bloque | Notas |
|---|---|---|
| 0:00 | **Hook**: el dashboard terminado; se pega una fila y todo se rehace (3 s); en el segundo 5, zoom a la tarjeta **−90 %** en rojo | El −90 % está en pantalla antes del segundo 8 |
| 0:15 | Rótulo + voz: "Excel para la web gratis, Claude gratis, sin macros; los datos son inventados. Te enseño el criterio; la plantilla hace el resto." | Regla 7, unos 10 s |
| 0:25 | **"Lo probé": un solo mensaje** (≤ 30 s) | Lo que salió de verdad en claude.ai. Cierra con la tarjeta −90 % y "rápido, sí; pero mira este número". Si la corrida no se hizo, el acto se elimina |
| 0:55 | **Pregunta 1, ¿cuánto vendimos?** Primera vez que aparece el método: "Mapa · Meta · Prueba: dónde están los datos, qué quieres y cómo comprobarlo". 3 tarjetas | **Antes y después de la Tabla, en 20 s o menos:** en un rango, se pega el pedido del 02/11 y el total sigue en 46.145.220; en la Tabla, pasa a 46.586.220 |
| 2:10 | CTA de suscripción con motivo + reenganche: "en un rato, por qué este tablero te asusta cada día 3" | |
| 2:20 | **Pregunta 2, ¿vamos mejor o peor?**: gráfico de 12 meses (noviembre bajito, diciembre en 0) + tarjeta "contra el mes anterior" = **−90,4 %** en rojo | Se deja así a propósito. La tarjeta se achica y **queda en una esquina** |
| 3:30 | **Pregunta 3, ¿quién y qué vende?**: barras por vendedor + desplegable en "Carla Ruiz" | La tarjeta −90 % sigue en la esquina |
| 4:40 | **Pregunta 4, ¿quién nos debe?**: cobranza con el Estado de video02 | Tarjeta de YouTube con enlace a video02. El −90 % sigue en la esquina |
| 5:00 | **Corte de anuncios** + reenganche: "ahora sí: ese −90 %" | |
| 5:10–6:40 | **El paso secreto: la Prueba sobre la tarjeta** | Ver abajo. Al resolverse, `quitar` la tarjeta de la esquina |
| 6:40 | **Resultado final + cronómetro**: se pegan los 3 pedidos de hoy y la barra de noviembre crece de 441.000 a 1.011.600, el acumulado pasa a 47.156.820 y el mismo tramo salta a +146,8 % mientras el mes cerrado sigue en +8,6 % ("por eso la grande es esta") | `antes_despues` solo con tiempos **medidos** (condición del creador); si no, sin cronómetro |
| 7:40 | **Límites**: 1) más de ~10 mil filas o varias fuentes → tabla dinámica o Power BI; 2) el **modo dashboard de Excel con Copilot** ([Kenji Explains, 16/10/2026](https://youtu.be/PxmvWAOksls), 173 mil vistas en 10 días) existe, pero es de Insiders o de pago (hay que verificar la disponibilidad el día del guion), y la Prueba sirve igual con cualquier herramienta; 3) la IA no sabe qué te importa a ti | Firma 3. Seguimiento anotado en `ideas.md` |
| 8:40 | CTA de la plantilla + pantalla final de 20 s con **video02** a la izquierda | "Si tus datos vienen sucios, empieza por aquí" |

## El "paso secreto" o giro que sostiene el bucle abierto (5:10–6:40, ≈ 55–70 %)

El giro no depende de que la IA se equivoque. Depende de la aritmética: cualquier fórmula "mes actual contra mes anterior" da −90,4 % con estos datos el 03/11. Es correcta en lo literal y engañosa en lo que comunica.

1. Pregunta 2: la Meta pide lo que pediría cualquiera ("la variación de las ventas de este mes contra el mes anterior"). La tarjeta se pinta de rojo: **−90,4 %**. Queda en la esquina durante las preguntas 3 y 4.
2. **La Prueba**: "¿Qué situación puede hacer que esta tarjeta muestre un número creíble pero equivocado, sin dar error? ¿Qué debería mostrar con fecha de corte 03/11/2026?". La respuesta real de claude.ai gratis va textual. **Rama A:** la IA señala el mes incompleto. **Rama B:** no lo señala, se dice ("esta vez no lo vio") y se demuestra cambiando la fecha de corte a 31/10, con lo que la tarjeta salta a +8,6 %. Nunca se inventa la respuesta.
3. `aviso` rojo: "El día 3 de cada mes, este tablero le dice a tu jefe que las ventas se desplomaron. Así le llegaría." Se muestra el porqué: 3 días contra 31.
4. La corrección, en dos tarjetas (`actualizar_tarjeta`): **último mes cerrado = +8,6 %** (la grande) y **mismo tramo = +7,6 %** (la chica, con la nota "con 3 días, es ruido").
5. La lección, en una frase: "Un dashboard rápido no sirve si el número más grande es mentira. Antes de mandarlo, pregúntale qué puede salir mal."

## Plantilla gratis que deja el video (sin cambios)

**"Distribuidora Sur · Dashboard de ventas.xlsx"**, gratis y sin registro:
- `Pedidos`: la Tabla de 250 pedidos ficticios, con portada y declaración.
- `Dashboard`: las 4 preguntas, el gráfico de 12 meses fijos, el desplegable y las dos tarjetas corregidas. En B1, `=HOY()` con la nota "pon 03/11/2026 para ver lo mismo que en el video".
- `Prompts`: Mapa · Meta · Prueba de cada bloque, con la columna "Qué revisar" y el mensaje único del acto inicial, con lo que salió.
- `Tus datos`: 5 pasos para pegar tus pedidos.
- Regla 8: sin macros, sin vínculos externos y sin tablas dinámicas. La versión de pago (metas, interanual) queda fuera de este video.

## 10 títulos (≤ 60 caracteres)

1. **Dashboard en Excel con IA: el error de cada inicio de mes** (57) ← **principal, A/B 1**, con la miniatura B híbrida
2. **Dashboard en Excel con IA: pegas pedidos y se rehace solo** (57) ← **A/B 2**, con la miniatura A rehecha
3. *(Condicional, solo si la corrida real sale mal o a medias)* **Le pedí a la IA un dashboard en 1 mensaje: esto salió** (53) ← A/B 3, con la miniatura C hecha con lo que salió de verdad. Si sale bien, no hay A/B 3 y el acto queda en 20 s
4. Dashboard en Excel con IA gratis: se actualiza solo (51) (era el principal; queda de reserva porque es casi el título de EXCELeINFO)
5. Dashboard en Excel con IA, sin macros ni Copilot de pago (56)
6. Dashboard en Excel con IA: el número que asusta a tu jefe (57)
7. Dashboard en Excel con IA: el reporte del lunes, listo (54)
8. Dashboard en Excel con IA paso a paso (plantilla gratis) (56)
9. Dashboard en Excel con IA: listo en [N] min, sin macros (55) (solo con [N] medido)
10. Dashboard en Excel con IA que no te asusta cada día 3 (53)

**Por qué el principal:**
- Es el único empaque que **no se parece a nada del top**. Los competidores venden "automático", "se actualizan solos", "gratis" y "1 minuto". El título 2 de la ronda 1 era casi el de EXCELeINFO.
- Nombra un dolor que Laura y Martín reconocen sin saber de dashboards ("inicio de mes" = cuando se arma el reporte).
- No dice "mentira": el −90,4 % es correcto en lo literal, así que el título habla de un "error" (de lectura) y deja la cifra a la miniatura, sin repetirla.
- **Por qué no se usa "un solo prompt":** que ese formato funcione está probado solo en inglés (Vedakarna). En español, el mejor resultado es 2,2x, y Laura no vio esos virales. Queda como hipótesis condicional, con la redacción del espectador.

## 3 conceptos de miniatura (fondo #0F0F10, acento #FFD400, 1 protagonista, texto distinto del título, sin fórmulas legibles)

Todas llevan la burbuja de chat de la serie: genérica, chica y sin logo.

| | Protagonista visual | Texto (≤ 3 palabras) | Contraste | Va con |
|---|---|---|---|---|
| **B híbrida (principal)** | Al fondo, un dashboard oscuro reconocible (3 tarjetas chicas y barras verdes, apagado, sin fórmulas legibles). Adelante, una **tarjeta gigante "−90 %" en rojo con flecha hacia abajo que se sale del cuadro**. Sin sello | **¿ES REAL?** | Rojo de alarma contra el tablero apagado y texto amarillo | Título 1 |
| **A rehecha** | El dashboard de frente, con una fila nueva que entra pegada (resaltada en amarillo) y la barra de noviembre creciendo con una flecha | **PEGAS Y LISTO**. Si se miden los 20 s: **LUNES: 20 s** | Fila amarilla que entra contra el tablero verde | Título 2 |
| **C (condicional)** | Captura animada de lo que salió de verdad en el mensaje único (página web, valores fijos o lo que sea), con la parte que falla marcada | Según lo que salió (por ejemplo, "NO SE ACTUALIZA" o "NO ES EXCEL"), siempre cierto | Lo que salió contra el defecto marcado | Título 3 |

Se descartaron "LUNES RESUELTO" (suena a eslogan), "¿EN SERIO?" y el sello "FALSO" (responde la pregunta antes del clic). Boceto de la principal: `produccion/video03/miniatura-b.html` (+ `.png` si el render funcionó).

## Hook (2 ideas · tipo "Resultado primero" + "Contradicción")

> "Pego los pedidos y este dashboard se rehace solo. Pero me dice que las ventas cayeron un 90 %, y no es cierto: es un error que este tablero comete el día 3 de cada mes, y así le llegaría a tu jefe."

En pantalla: primer cuadro, el dashboard terminado; se pega una fila y todo se rehace (3 s); hacia el segundo 5, zoom a la tarjeta **−90 %** en rojo. Sin "al final te muestro" y sin "un solo prompt". "Gratis, sin macros, Excel para la web" y "datos inventados" van en el rótulo y la voz de 0:15.

## Producción con el motor v2 (acciones nuevas, documentadas en `sistema/motor-v2.md`)

Todo el video se puede hacer con el motor actual. No hay gráfico de líneas: la tendencia va en barras.

| Momento | Plantilla / acción |
|---|---|
| Dashboard (hook, preguntas, final) | `excel` con `tarjeta` (`id`, `titulo`, `valor`, `sub`, `x`, `y`, `ancho`, `color`) para las KPI, y `grafico` con `id`, `alto` y `max` para los 12 meses y los 3 vendedores. `max` fijo, para que la barra de noviembre crezca sin cambiar la escala del resto |
| Antes y después de la Tabla (pregunta 1) | `rellenar` de la fila pegada + `actualizar_tarjeta` que **no** cambia (rango) y que **sí** cambia (Tabla), con `resaltar` del total |
| −90 % en la esquina (preguntas 3 y 4) | `tarjeta` chica con `id: "alarma"` en una esquina libre de la hoja; `quitar` (`id: "alarma"`) al terminar el giro |
| Desplegable "Carla Ruiz" | `desplegable` (`celda`, `opciones`, `elegir`) + `actualizar_grafico` y `actualizar_tarjeta` |
| Giro | `chat` (respuesta real), `aviso` rojo y `actualizar_tarjeta` (−90,4 % → +8,6 % / +7,6 %), o `cifra` a pantalla completa para el +8,6 % |
| Resultado final | `rellenar` de los 3 pedidos de hoy + `actualizar_grafico` (noviembre 441.000 → 1.011.600) + `actualizar_tarjeta` (acumulado, mismo tramo, mes cerrado) |
| Ritmo | `capitulo` por pregunta, `rotulo` para el método, `antes_despues` solo con tiempos medidos, `final` con video02 |

Nota para el director visual: en la vista `excel` se ven unas 7 columnas y 12 filas. El dashboard se arma como una hoja con tarjetas y gráficos superpuestos (`x`, `y`). Conviene revisar con `motor.py --cuadros` que las tarjetas no tapen el desplegable en B2.

## Riesgos

- **Respuestas reales (regla 4).** El acto "lo probé" y la Prueba se corren en claude.ai gratis antes del guion (condición del creador; el orquestador puede no tener acceso). Hay que confirmar que el plan gratuito lee .xlsx. Lo que no se corra no sale: sin la corrida, el acto se elimina, no hay A/B 3 y el giro usa la rama B.
- **Excel para la web (verificar en español, con cuenta gratis):** la expansión de la Tabla al pegar, las referencias estructuradas (`Pedidos[Neto]`), la lista desplegable y que los gráficos conserven el formato. La segmentación de datos no se usa.
- **Cifras:** salen de Python. Hay que confirmar en Excel el −90,4 %, el +7,6 %, el +8,6 %, el +146,8 %, el 46.586.220, el 47.156.820 y el 2.951.090.
- **Tiempos:** [N] (el armado) y los "20 s" del lunes están sin medir. No entran en la promesa, el título ni la miniatura hasta que se midan.
- **Exclusividad del giro:** depende de la revisión de El Inge Francisco ([1pJqarOwgbA](https://youtu.be/1pJqarOwgbA)). Si ese video ya trata el mes incompleto, el principal se reevalúa.
- **Fecha:** el martes 03/11, 13:00 CDMX, se mantiene si las verificaciones del creador están el **viernes 30/10**. Si no, conviene mover la fecha antes que recortar la demostración. El giro no depende del día de publicación.
- **Herramientas que cambian:** Copilot en Excel, su modo dashboard y Claude para Excel se nombran solo como "de pago o Insiders" y se verifican el día del guion. No mencionar `=COPILOT()`.
- **Competencia y tráfico:** la búsqueda en español la dominan canales grandes; ver la "Lectura honesta".
- **Contenido inauténtico (regla 6):** es la misma empresa, pero con otro caso, otro error, otra estructura y otra base. Es un capítulo de una serie.
- **Temas sensibles:** ninguno.

## Respuesta a la ronda 1

### Correcciones obligatorias del showrunner
1. **Empaque principal = giro. Aceptada.** El principal es "Dashboard en Excel con IA: el error de cada inicio de mes" (57), con la miniatura B híbrida: dashboard oscuro al fondo, "−90 %" rojo que se sale del cuadro, sin sello, "¿ES REAL?" y la burbuja de la serie. Reescribí "Por qué el principal" y saqué la afirmación de que el título 3 es "el formato de los outliers".
2. **Variantes A/B. Aceptada.** A/B 2: "pegas pedidos y se rehace solo" (57), con la miniatura A rehecha y el texto "PEGAS Y LISTO" ("LUNES: 20 s" solo si se mide). El A/B 3 queda condicionado a la corrida real, con "Le pedí a la IA un dashboard en 1 mensaje: esto salió" (53). Eliminé "¿EN SERIO?" y "LUNES RESUELTO". El antiguo título 1 pasa a reserva (n.º 4).
3. **Hook en 2 ideas, con el −90 % antes del segundo 8. Aceptada.** No usé "casi lo mando así" (anécdota inventada): lo cambié por "así le llegaría a tu jefe". Saqué del hook "al final te muestro" y "un solo prompt". Gratis, macros y datos inventados van al rótulo de 0:15.
4. **Promesa y gráfico de 12 meses. Aceptada.** Ahora es "pegas los pedidos y se rehace solo" en la promesa, la descripción, el hook y el título 2. El gráfico mensual quedó en un rango fijo de enero a diciembre (futuros en 0). `datos_base.py` ahora tiene `meses()` y `pedidos_hoy()`: la barra de noviembre crece de 441.000 a 1.011.600 en el resultado final. Las cifras del giro no cambian.
5. **Escaleta. Aceptada.** El acto "lo probé" dura 30 s o menos. El paso 0 ya no existe: el antes y después del rango contra la Tabla va dentro de la pregunta 1, en 20 s o menos, con cifras (46.145.220 se queda igual en el rango; 46.586.220 en la Tabla). La tarjeta −90 % queda en la esquina durante las preguntas 3 y 4 y se quita al resolverse. El método se explica en una línea la primera vez. Sumé "no tienes que memorizarla" en el desplegable.
6. **Diferenciación, evidencia y producción. Aceptada.** El punto 4 ("primero las preguntas") pasó a estructura. La lectura honesta ahora tiene 500–1.600 vistas por día, 0,0–0,5x, ninguno nuevo en 60 días y la expectativa baja por búsqueda. El modo dashboard con Copilot quedó en Límites, con el seguimiento anotado en `ideas.md`. La sección de producción está reescrita con las acciones nuevas, y quité el riesgo de motor y el "no producir".

### Opcionales
- **RPM: aceptada a medias.** Cito la ficha como fuente; no hay cifra con fuente y fecha, así que no pongo ninguna. Sumé `informe de ventas`, `cuentas por cobrar` y `Power BI` a búsquedas, capítulos y Límites.
- **Densidad: aceptada.** En 0:15: "Te enseño el criterio; la plantilla hace el resto".
- **Sugerencias / Trends: aceptada como pendiente.** El proxy sigue dando 403; no bloquea.

### Objeciones de los críticos fuera de la lista del showrunner
- **Investigador, "79/65 sale de resultados en inglés": aceptada.** Ahora se aclara en la evidencia.
- **Retención, "mostrar un pedido de otro mes": aceptada en parte.** El rango fijo de 12 meses cubre el caso (cualquier mes del año aparece al pegar), y en el final se pega un pedido de noviembre, el mes nuevo. Un pedido de otro año no entra en esta versión (el gráfico es de 2026); queda anotado como mejora de la versión de pago (interanual).
- **Retención, "no aprobar 'gratis' sin las 3 verificaciones": aceptada.** Quedan como condiciones del creador antes del guion. "Gratis" ya no está en el título principal, solo en la descripción y en el rótulo, y se retira si Excel para la web no pasa la prueba.
- **Espectador, "[N] si da una tarde choca con los competidores de 1 minuto": aceptada.** [N] salió de la promesa hasta que se mida. La alternativa es "lo armas una vez; cada lunes, pegar y listo".
- **Retención, "Dice −90 % y es mentira" como título: rechazada.** Por veracidad (el número es literalmente correcto) y porque repetiría la cifra de la miniatura (regla de `04` §3: el título y la miniatura no se repiten). Decisión del showrunner, punto 2.
