# video02 · Debate

## Ronda 1 · decisión del showrunner

**Etapa:** idea · **Resultado de `pipeline.py evaluar`:** REVISAR · **Nota:** 6,92 (umbral 8,0)
Criterios: demanda 6,0 (mín. 7) · empaque 6,5 (mín. 8) · diferenciación 7,0 · rpm 7,0 · encaje 9,0.
Lectura: la idea es buena (encaje 9, el espectador haría clic y la terminaría). Falla por dos cosas: el **empaque**, que se arregla en esta ronda, y la **demanda**, que no se puede medir en esta sesión.

### Prueba real de la fórmula 7 (Mapa + Meta, sin Prueba)

Armé el prompt con la plantilla del método tal como está en idea.md. El Mapa nombra todas las columnas de `Pedidos` porque eso es lo que enseña el método, y sacar L de la lista para provocar el fallo sería amañar la prueba:

> Excel para la web en español, separador punto y coma. Hoja Pedidos: A Fecha, C Cliente, E Vendedor, F Código, G Cantidad, H Precio, I Descuento, J Neto, K Vence, L Pagado (Sí/No), M Estado. Los datos van de la fila 2 a la 13. La fecha de corte está en la hoja Resumen, celda B1.
> En M2 quiero el estado de cada factura: si ya venció, que diga "Vencido"; si no, "Al día". Dame una sola fórmula para copiar hacia abajo.

Respuesta real de Claude (yo, en esta sesión, sin forzar el resultado):

> `=SI(K2<Resumen!$B$1;"Vencido";"Al día")`
> Cópiala hasta M13; el `$` deja fija la fecha de corte.
> Un detalle: tienes la columna L (Pagado). Si una factura ya se pagó, seguramente no quieres que aparezca como "Vencido". En ese caso usa:
> `=SI(L2="Sí";"Pagado";SI(K2<Resumen!$B$1;"Vencido";"Al día"))`

**Resultado: SÍ tiene en cuenta la columna "Pagado".** Da primero la versión ingenua, pero enseguida avisa y ofrece la corregida. No se puede presentar como "la IA me dio una fórmula que mentía". **Se aplica el plan B**, y desde ahora es la base del video aunque la corrida en claude.ai gratis salga distinta. Así el empaque no depende de una casualidad. Salvedad: la prueba se corrió con Claude en esta sesión, no en claude.ai gratis. El guionista igual tiene que correr y guardar los prompts reales (regla 4), pero no se apuesta el giro a ese resultado.

### Contradicciones resueltas (prioridad: veracidad y políticas > promesa > retención > estilo)

1. **Giro "la IA me engañó" contra la prueba real.** Gana la veracidad: plan B. La fórmula ingenua se rotula "escrita a mano, como la escribe casi todo el mundo". La Prueba se aplica a esa fórmula y la IA encuentra el fallo. Las cifras (8 vencidas / 2.446.165, luego 4 / 1.835.590, diferencia 610.575) las recalculé con la tabla y están bien.
2. **Título 3 + miniatura C ("casi me engaña" / "TE MINTIÓ") contra el plan B.** Gana la veracidad: con el plan B sería clickbait, porque quien miente es la fórmula escrita a mano, no la IA. Se cambian según la objeción de retención: "¿VENCIDO?".
3. **Promesa "sin errores" y título 2 "no fallan" contra el veredicto honesto del propio video.** Gana la promesa cumplida: el video muestra fórmulas que fallan sin dar error, así que no puede prometer lo contrario.
4. **Título principal: el investigador pide el 3 o el 2, el espectador el 3 y retención "la planilla se llena sola".** Con el plan B, el 3 queda debilitado como principal. Gana la propuesta de retención: es la única que cumple la firma del canal (hoja terminada como protagonista) y coincide con el hook. El giro se prueba como A/B.
5. **Demanda (mínimo 7, exige datos de investigar.py) contra un entorno sin API ni autocompletado.** No es un defecto de la idea y el ideador no puede arreglarlo reescribiendo. Decisión: la demanda deja de ser una corrección para el ideador y pasa a ser una **condición pendiente del creador** (ver abajo). En la ronda 2, el investigador no debe bajar la nota por falta de datos de nuevo: puntúa solo si la evidencia cualitativa está bien presentada.
6. **Claude contra ChatGPT en la demo (investigador, retención y espectador piden ChatGPT).** Gana la veracidad (regla 4): en esta sesión solo hay respuestas reales de Claude. La demo se hace con Claude. Si el creador corre los 10 prompts en ChatGPT gratis (unos 15 min, respuestas textuales con fecha y captura), se cambia el rótulo del chat y entra un título A/B con "con ChatGPT". Nunca se muestra un chat de ChatGPT que no se haya corrido.
7. **Fórmula 1 (BUSCARX) se pisa con el video 3.** BUSCARX se queda en el video 2: es el arranque más fuerte y es parte de la cascada. A cambio, el video 2 no lo usa en la miniatura y el video 3 queda obligado a otro caso y otro error (BUSCARV que falla por coincidencia aproximada, números guardados como texto o espacios), no el "código no existe". Queda anotado para la idea del video 3.

### Condición pendiente (creador, no ideador): demanda

- Antes de **cerrar el guion** (como tarde, antes de publicar): correr `python3 herramientas/investigar.py nicho "fórmulas de excel con ia" --region MX` (y ES), o anotar a mano el top 5 de YouTube para `fórmulas de excel con ia` y `fórmulas de excel con chatgpt`: título, canal, vistas y antigüedad. Agregarlo a idea.md.
- Si "con chatgpt" gana con claridad (por ejemplo, el top 5 tiene el doble de vistas o es más reciente), el creador corre los prompts en ChatGPT y el título A/B pasa a "con ChatGPT". Si ninguna de las dos tiene demanda visible, se reabre la idea.
- Si la ronda 2 aprueba todo menos la demanda, y la demanda queda abajo solo por el entorno, recomiendo que el creador la apruebe con `python3 herramientas/pipeline.py forzar video02 idea "demanda pendiente de medir por falta de API; condición antes del guion"`. Forzar es una decisión humana: yo no la tomo.

### Correcciones obligatorias para el ideador (en orden)

1. **Reescribir el giro de la fórmula 7 con el plan B como base.** La fórmula ingenua se rotula "escrita a mano" y la Prueba se aplica pegando esa fórmula: "¿qué casos pueden dar un resultado equivocado sin error?". La IA señala "Pagado". Ajustar el hook ("la tercera parte es la que encontró la fórmula que le habría cobrado dos veces a un cliente"), el reenganche de 5:10 y el punto 4 del giro. Sumar el hallazgo honesto de la prueba: cuando el Mapa nombra todas las columnas, la IA ya ve "Pagado". Es una razón más para el Mapa y no contradice la lección. Dejar textual en idea.md el prompt de la fórmula 7 que está arriba.
2. **Títulos A/B (≤ 60 caracteres):**
   - Principal: `10 fórmulas de Excel con IA: tu planilla se llena sola` (54), o sin el "10" si se prefiere la palabra clave exacta al inicio. Si [N] medido ≤ 15 min y entra en 60 caracteres, se puede usar en su lugar.
   - A/B 2: `Fórmulas de Excel con IA: el paso que casi nadie pide` (53).
   - A/B 3: `Fórmulas de Excel con IA (y el error que cobra dos veces)` (57).
   - El título 1 actual ("10 que te ahorran horas") baja a la lista de reserva.
3. **Miniaturas:**
   - **A (principal):** la hoja `Resumen` terminada a lo grande, con una burbuja de chat chica que "la escupe" y el texto `MAÑANA → [N] MIN`. Es el mismo cuadro del hook y no muestra código.
   - **B:** un solo contraste (`#N/A` gris contra la hoja terminada) con el texto `SIN #N/A`. "Gratis" va solo en la voz y en el título.
   - **C:** celda "Vencido" con sello "PAGADO" y el texto `¿VENCIDO?`, nunca "TE MINTIÓ".
   - Las tres llevan la burbuja de chat como señal de IA.
4. **Promesa:** cambiar "sin errores" por "fórmulas que puedes comprobar antes de confiar en ellas" o una equivalente. Va en la promesa de una frase y en todo lo que derive de ella.
5. **Adelantar el giro:** 2 s de "Vencido" + "PAGADO" en el hook, y nombrarlo en el reenganche de 3:30 ("en un rato vas a ver la fórmula que le cobra dos veces a un cliente"), para quien entra por el A/B 3.
6. **Limpiar la evidencia de demanda:** quitar "WebSearch no devolvió videos, puede ser un hueco" (WebSearch no indexa YouTube y eso no prueba nada) y dejar la demanda escrita como condición pendiente, con el procedimiento de arriba.

### Opcionales (si no agregan más de 20 s)

- Metadatos y un capítulo con `cuentas por cobrar`, `cobranza en Excel` y `plantilla Excel pyme`: el RPM es más alto y ese caso ya está en la planilla.
- En los primeros 30 s, junto con "gratis": "las fórmulas 3, 8 y 9 necesitan Excel para la web o 365, no 2016/2019".
- 5 s en la fórmula 1 para mostrar cómo saber si tu Excel usa `;` o `,`.
- Mencionar la hoja `Prompts` con la columna "Qué revisar" a mitad del video, en el CTA de 3:30 o en el de la plantilla.
- Ritmo: las fórmulas fáciles (2, 5, 9) más cortas y las de matriz (8) con un desglose pieza por pieza. Es nota para el guionista, no hace falta reescribir la idea.
- Si el creador corre un prompt en ChatGPT, mostrarlo una vez lado a lado. Solo con una respuesta real.

### No tocar (funciona)

- La planilla "Distribuidora Sur", con datos, errores sembrados y fecha de corte fija. Las cifras de las fórmulas 6, 7, 8 y 9 se recalcularon y están bien.
- El orden de las 10 fórmulas, el corte de anuncios en 5:10 y el giro al 70 %.
- El método "Mapa · Meta · Prueba" como hilo y bucle abierto.
- La plantilla de lead magnet (hojas `Prompts` y `Práctica`, nota del separador).
- La sección de riesgos y el aviso de "Claude gratis; el mismo prompt funciona en ChatGPT o Copilot" en los primeros 30 s.
- La palabra clave `fórmulas de excel con ia` hasta que haya datos que digan lo contrario.

## Respuesta del ideador a la ronda 1

Todos los cambios están en `idea.md`. La versión de la ronda 1 se guardó fuera del repo, como respaldo de sesión.

### Correcciones obligatorias del showrunner
1. **Giro de la fórmula 7 con el plan B como base: aceptada.** La fórmula ingenua ahora la escribe el narrador ("esta es corta, la escribo yo"), con el rótulo fijo "escrita a mano, como la escribe casi todo el mundo". La Prueba se aplica pegando esa fórmula en el chat ("¿qué casos pueden dar un resultado equivocado sin error? ¿qué debería dar en las filas 2 y 6?"), y la IA señala "Pagado". El prompt de la prueba y la respuesta quedaron textuales en idea.md, con la salvedad de que se corrieron en la sesión y no en claude.ai gratis. Sumé el hallazgo honesto: con el Mapa completo, la IA ya avisa de "Pagado", y eso es un argumento más para el Mapa y para pasar por la Prueba aunque la fórmula la escribas tú. Ajusté el hook, el reenganche de 5:10 y la secuencia del giro. Agregué un tope: si la respuesta real de claude.ai a la Prueba no señala "Pagado", el giro no se inventa y vuelve a debate.
2. **Títulos A/B: aceptada.** Principal: "10 fórmulas de Excel con IA: tu planilla se llena sola" (54). A/B 2: "…el paso que casi nadie pide" (53). A/B 3: "…(y el error que cobra dos veces)" (57). Elegí la versión con el "10" porque `04` pide un número concreto y la palabra clave sigue en las primeras 4 palabras. "10 que te ahorran horas" pasó a reserva. Agregué dos reservas condicionadas: con [N] medido, o si se corre en ChatGPT (59 caracteres).
3. **Miniaturas: aceptada.** A: hoja `Resumen` terminada con burbuja de chat y el texto `MAÑANA → [N] MIN`; si [N] pasa de 15 min, el texto es `UNA MAÑANA MENOS`. B: `#N/A` gris contra la hoja terminada, con `SIN #N/A`. C: "Vencido" con sello "PAGADO" y `¿VENCIDO?`. Las tres llevan la burbuja de chat y ninguna muestra código.
4. **Promesa sin "sin errores": aceptada.** Ahora dice "…de forma que puedas comprobarla antes de confiar en ella…". También quité "no fallan" de los títulos.
5. **Adelantar el giro: aceptada.** El hook muestra 2 s de "Vencido" con el sello "PAGADO", y el reenganche de 3:30 dice "en un rato vas a ver la fórmula que le cobra dos veces a un cliente, y cómo la atrapé".
6. **Limpiar la evidencia de demanda: aceptada.** Quité el argumento de "WebSearch no devolvió videos". Las guías en texto quedan presentadas como señal de interés, no de volumen. La demanda figura como condición pendiente del creador, con el procedimiento del showrunner copiado.

### Opcionales
- Cobranza y cuentas por cobrar en los metadatos y en un capítulo: **aceptada.** Va como punto 6 del ángulo propio y no agrega tiempo.
- Aviso de Excel 2016/2019 en los primeros 30 s: **aceptada.** Está en la sección de la restricción y en riesgos.
- 5 s sobre `;` o `,` en la fórmula 1: **aceptada.**
- Mencionar la hoja `Prompts` con "Qué revisar": **aceptada.** Va en el CTA de 3:30 y en el cierre.
- Ritmo (las fáciles en unos 35 s, la 8 desglosada pieza por pieza): **aceptada**, como nota para el guionista.
- ChatGPT lado a lado: **aceptada con condición.** Solo si el creador corre el prompt; está en la sección de la restricción.

### Objeciones de los críticos que no estaban en la lista del showrunner
- Investigador: "principal el 3 o el 2". **Rechazada como principal y aceptada como A/B.** Con el plan B, el 3 ya no puede prometer que la IA miente, y el 2 es abstracto en la página de resultados. El principal nuevo es el único que coincide con la firma del canal (la hoja terminada en la miniatura y en el hook). La prueba "Probar y comparar" de YouTube Studio decide entre los tres con datos.
- Espectador: "la C, que habla a Martín, como principal". **Rechazada como principal, aceptada en parte.** Martín ya tiene su entrada en el A/B 3 con "cobra dos veces", y la cobranza va en los metadatos. Una miniatura principal con "Vencido" no muestra el resultado del video (las 10 fórmulas).
- Espectador: "Laura usa BUSCARV". **Aceptada en parte.** BUSCARX se queda porque funciona en Excel para la web, trae el "si no existe" incorporado y es parte de la cascada. Agregué una frase en la fórmula 1: "es la versión nueva de BUSCARV, la que no se rompe si agregas columnas".
- Espectador: "si el cronómetro no impresiona, empezar por el error de cobranza". **Aceptada.** Si [N] pasa de 15 min, el hook arranca con "Esta fórmula le iba a cobrar dos veces a un cliente…".
- Investigador: "se pisa con el video 3". **Aceptada según la decisión del showrunner.** BUSCARX queda en el video 2, pero no en la miniatura, y el video 3 queda obligado a otro caso y otro error. Lo anoté en la fila de la fórmula 1.
- Investigador, retención y espectador: palabra clave y Claude contra ChatGPT. **Sin cambios.** Se mantiene la decisión del showrunner (regla 4) y la condición del creador.

### Lo que no toqué
Según "No tocar": la planilla, las cifras, el orden de las 10 fórmulas, el corte de 5:10, el giro al 70 %, el método, la plantilla y los riesgos.

## Respuesta del ideador a la ronda 2

1. **Miniatura A: aceptada.** Un solo protagonista (el gráfico de barras de `Resumen`), burbuja de chat genérica y chica sin logo, y el texto `4 HORAS → [N] MIN`. Si [N] no impresiona, el respaldo es `4 H → 1 CELDA`. Quité "MAÑANA". Salvedad que dejé escrita: las "4 horas" no son una cifra verificada, sino una estimación. El creador tiene que medirlas (arma a mano 2 fórmulas y la cobranza, y extrapola) y en el video se dicen "estimado". Si dan menos, cambian en el hook y en la miniatura.
2. **Miniatura B: aceptada.** Celda verde con check y grieta roja, con el texto `PARECE BIEN`, para el título 2. "SIN #N/A" queda como alternativa fuera del A/B, con la sugerencia del espectador de probarla en un segundo A/B con el título 1.
3. **Miniatura C: aceptada.** Texto `610.575 DE MÁS`, sello PAGADO sobre "Vencido" y burbuja sin alerta. La cifra sale de la tabla y hay que verificarla en Excel.
4. **Hook: aceptada.** Destello de 1 s del sello "PAGADO" en el primer cuadro. La frase ahora dice "10 fórmulas, casi todas se las pedí a una IA gratis y la que escribí yo la revisó ella", así que es honesta con el plan B.
5. **Promesa y descripción: aceptada.** "Las fórmulas de Excel que usas en la oficina" reemplaza a "cualquier fórmula". Agregué la línea 1 de la descripción: "Tu planilla de Excel se completa sola, sin macros, con 10 fórmulas que le pides a una IA gratis (y una prueba para que no te engañen)".
6. **Giro: aceptada.** El capítulo 7 se llama "La IA como revisora de tus fórmulas". La frase es: "A veces la IA te avisa sola… Pero a veces no. La Prueba hace que te lo diga sí o sí".
7. **Demanda y ángulo: aceptada.** Agregué el umbral del investigador: en el top 10, al menos 2 videos de los últimos 12 meses con 30 mil vistas o más, o al menos 1 outlier de 3x. Si la mediana de "con chatgpt" es el doble o más, se pasa a ChatGPT. Si ninguna de las dos pasa, se reabre la idea. "Ángulo propio" ahora dice "frente a las guías en texto revisadas; YouTube se verifica con la condición de demanda".
8. **Señales de interés de 2026 (Cámara de Sevilla, NYSSCPA, Genbeta, ClickUp, Platzi, DataCamp, Ámbito): rechazada por ahora.** La crítica no trae enlaces y en esta sesión no tengo acceso web para encontrarlos. La regla 3 de la ficha exige fuente para cada dato real. Entran cuando el investigador pase las URL.
9. **"Pasar a 'lista en [N] min' cuando [N] se mida" (retención): aceptada.** Está como reserva condicionada del título principal.

Es la ronda 3. Si el empaque sigue por debajo de 8, propongo no descartar la idea: el encaje es 9, el espectador haría clic y la terminaría, y la demanda baja solo por el entorno. Tampoco conviene seguir puliendo en abstracto. Lo mejor es pasar a la condición del creador (umbral de demanda, medir [N] y las 4 horas) y que el A/B de YouTube decida el empaque con datos reales.

## Etapa guion · ronda 1 · notas del guionista

Entregables: `guion.json` (motor v2, 38 escenas, 1.435 palabras de locución, ~10,4 min estimados por el motor sin voz) y `respuestas-ia.md` (los 11 prompts con su respuesta completa). `puntuar_guion.py`: 100/100.

### Ajustes del coordinador al hook (aplicados)
1. **Primer cuadro = hoja Resumen terminada con el gráfico de barras** (escena excel marcada `solo_video`); el sello "PAGADO" es un `resaltar` amarillo sobre la celda de Ferretería El Tornillo (0 vencidas) en ese mismo cuadro, sin cortar a otra imagen. El gráfico va a la derecha (columnas G-H) para no tapar los bloques de la hoja.
2. **Primera frase partida en dos:** "Esta planilla se completa sola: precios, vencimientos, cobranza y el resumen del lunes." / "Diez fórmulas que le pedí a una IA gratis, en minutos. A mano me llevaban unas cuatro horas; es una estimación mía." Sin número de minutos inventado. "La que escribí yo y la revisó la IA" pasó al giro. Es honesto: las diez fórmulas finales salen de la IA (la 7 corregida la da la respuesta a la Prueba).
3. **Promesa:** "Al final vas a poder pedir tus fórmulas y comprobarlas antes de confiar en ellas." "Oficina" no aparece en la locución.

### Decisiones propias (desvíos de idea.md, con motivo)
- **Sin `antes_despues`.** El cronómetro necesita [N] medido y no se inventa. La estimación de 4 h va solo en la voz, dicha como estimación. Cuando el creador mida [N], entra un `antes_despues` {antes: 14400 s "a mano (estimado)", después: N s} después del hook.
- **Aviso de versiones corregido:** idea.md decía "las fórmulas 3, 8 y 9 no están en 2016/2019". En realidad tampoco está BUSCARX (fórmula 1), y TEXTODESPUES y ELEGIRCOLS solo están en 365/web. La voz dice "Varias de estas fórmulas no existen en Excel 2016 ni 2019" y la lista pide Excel para la web o 365.
- **Fórmula 6 con un solo mes elegible** (`$B$2`) en vez de una tabla vendedor × mes: el motor solo rellena hacia abajo y una tabla de dos ejes obligaba a escribir la fórmula tres veces. El cambio de mes (septiembre → octubre) muestra que se recalcula sola. Resultado clave de la idea intacto: Carla Ruiz, septiembre, 1.215.000.
- **Fórmula 8 con SI.ERROR y orden por neto (de mayor a menor).** La respuesta real a la Prueba detectó que `ORDENAR(FILTRAR(…;"Sin vencidos");2;1)` de idea.md da error cuando no hay vencidas (el riesgo que idea.md dejó anotado). Ordenar por neto evita además los empates de vencimiento. Es una segunda demostración de la Prueba, después del giro.
- **"Cobrado"** como estado de las pagadas: es el texto que eligió la respuesta real a la Prueba (7b), igual que la planilla de idea.md.
- **Fórmulas 9 y 10 en un solo capítulo** ("9 y 10"), para que el bloque final no se haga largo. Fórmulas 2, 3, 5, 9 y 10 se pegan sin mostrar el chat (la voz dice que se pidieron con la meta); sus respuestas reales están en `respuestas-ia.md`.
- **Pantalla final:** manda al video 1 (resumir PDF con IA), que es el único publicado.

### Exactitud y verificación
- `python3 herramientas/plantilla_xlsx.py video02 --verificar` **sigue marcando 72 diferencias, todas por la versión de LibreOffice del entorno (24.2.7)**, que no tiene BUSCARX, TEXTODESPUES, FILTRAR, ORDENAR, UNICOS ni ELEGIRCOLS (llegan en 24.8/25.x). Da `#NAME?` en H y E, y eso arrastra I, J, las ventas del Resumen y los desbordes. No pude instalar una versión nueva: el proxy bloqueó la descarga (403).
- **Cómo lo comprobé:** `produccion/video02/fuente/verificar_lo242.py` usa la misma reconstrucción y comparación que `--verificar`, pero en una copia de la plantilla cambia BUSCARX por SI.ERROR(INDICE(COINCIDIR)), TEXTODESPUES por EXTRAE(HALLAR) y los desbordes de FILTRAR/ORDENAR y UNICOS/ORDENAR por fórmulas clásicas (K.ESIMO.MAYOR, SUMAPRODUCTO, MMULT) calculadas sobre los mismos datos. Resultado: **109/109 valores del video coinciden.** Chequeos extra con LibreOffice: 5 clientes distintos con nombres limpios y **10 con los nombres sucios** (CONTAR.SI, que no distingue mayúsculas y sí espacios, como UNICOS); con la fórmula escrita a mano, **8 vencidas y 2.446.165**; corregida, **4 y 1.835.590** (diferencia 610.575). Además, el generador del guion (`produccion/video02/fuente/armar_guion.py`) calcula todos los valores en Python desde los datos crudos, de forma independiente.
- **Pendiente para el verificador:** confirmar en Excel para la web en español las fórmulas 1, 3, 8 y 9, el orden de ORDENAR con tildes y que UNICOS no distinga "KIOSCO" de "kiosco".

### Cambios en herramientas (necesarios para este video; revisar si el coordinador los acepta)
- `herramientas/plantilla_xlsx.py`: fechas dd/mm/aaaa como fechas reales (antes quedaban como texto y FIN.MES, SUMAR.SI.CONJUNTO con fechas y SI con la fecha de corte no funcionaban en la plantilla); traduce VERDADERO/FALSO y ELEGIRCOLS; FILTRAR y ORDENAR con el prefijo `_xlfn._xlws.` que pide Excel; rellenar ajusta `$A3`; las celdas de `datos` de escenas posteriores ya no pisan fórmulas escritas antes ni celdas de desborde; escenas con `"solo_video": true` no entran en la plantilla; formato de fecha en celdas cuyo valor esperado es fecha.
- `produccion/render/motor/motor.js`: escapa el texto animado (el `<` de `K2<Resumen!$B$1` y de `"<="&` cortaba la fórmula en la celda, la barra y el chat); `<br>` permitido en las respuestas del chat; las referencias a otra hoja (`Pedidos!A2:M13`) ya no se dibujan sobre la hoja actual.
- `produccion/render/motor/estilos.css`: `box-sizing: border-box` y `white-space: pre` en las celdas (las columnas ocultas de 2 px dejaban ver texto, y no se veía el doble espacio de "Hotel  Mirador"); las fórmulas largas saltan de línea en el chat; más margen bajo el título del gráfico (la etiqueta de la barra más alta lo pisaba).

### Pendientes
- **Respuestas de IA:** las generó Claude en la sesión del guionista, no claude.ai gratis. El rótulo dice "versión gratuita", así que el creador debe correr los prompts de `respuestas-ia.md` en claude.ai gratis antes de publicar, sobre todo el 7b (giro). Si no señala "Pagado", el giro vuelve a debate.
- **La plantilla generada** tiene Pedidos, Productos y Resumen, pero no las hojas Prompts ni Práctica que promete la voz: hay que agregarlas al armar el lead magnet. Además, openpyxl guarda FILTRAR/UNICOS sin los metadatos de matriz dinámica, y Excel podría abrirlas con `@` (un solo valor). Hay que probarlas en Excel para la web; si pasa, se vuelven a escribir a mano en el archivo.
- La fila 13 de Pedidos no entra en pantalla (el motor muestra 12 filas): el relleno baja una fila más allá de lo visible. Es menor y no cambia ningún valor mostrado.
- [N] y las 4 horas siguen sin medir (condición del creador).

## Guion · ronda 1 · decisión del showrunner

**Etapa:** guion · **Resultado de `pipeline.py evaluar`:** PROVISIONAL-REVISAR · **Nota:** 6,33 (umbral 8,5)
Criterios: hook 6,0 (mín. 8) · ritmo 6,0 (mín. 8) · promesa 7,5 (mín. 8) · claridad 7,5 (mín. 8) · **veracidad 5,0 (mín. 9, veto del verificador)**.
Lectura: la estructura, los datos y el giro funcionan. El veto viene de afirmaciones que no se pueden sostener (el plan gratuito, ChatGPT/Copilot, las 4 horas, Excel 2021, FIN.MES). Hook y ritmo fallan por dos motivos: la fórmula 1 aparece recién en 1:12 y hay tramos largos de Excel sin ningún corte visual. Todo se arregla en el guion: no hace falta volver a la idea.

### Decisiones del orquestador (firmes, se aplican tal cual)
- Rótulo de los chats: `"app": "Claude"` sin `modelo`. Ninguna frase de la voz dice que se usó el plan gratuito. Descripción: "Respuestas generadas con Claude el 25/10/2026". Si el creador corre los prompts en claude.ai gratis, se vuelve a poner el plan.
- Frase de ChatGPT/Copilot reformulada como propone el verificador (ver obligatoria 2).
- Fuera "unas cuatro horas, estimación mía". El hook no lleva cifras sin medir.
- `antes_despues` permitido solo con cifras verificadas de la planilla ("10 clientes → 5", "8 vencidas → 4"). Nada de tiempos.

### Contradicciones resueltas (prioridad: veracidad y políticas > promesa > retención > estilo)
1. **Retención pide saltear el chat en 2 de cada 3 fórmulas, pero el título promete "con IA".** Gana la promesa, con un ajuste. El chat completo queda en 1, 4, 7 (el giro) y 8. Ya está fuera en 2, 3, 5, 9 y 10, y ahí no hace falta sacar más. Lo que se corrige es la duración: ningún chat dura más de 12 s, salvo el 7b (giro), que puede llegar a 20 s. Las fórmulas sin chat no pueden quedar sin rastro de IA: se abren con un `rotulo` (p. ej. "02 · Se la pedí a Claude · prompt en la hoja Prompts"). Así cada fórmula prueba que hubo IA sin repetir el patrón capítulo→chat→excel.
2. **Retención propone "Nueve se las pedí a una IA gratis" y el orquestador quita "gratis".** Gana la veracidad. Queda: "Nueve se las pedí a una IA. La décima la escribí yo… y casi le cobro dos veces a un cliente que ya había pagado." Así se resuelve también la objeción [0:05 vs 5:28].
3. **Retención pide recortar desvíos de la fórmula 1, el espectador pide más aclaraciones (el $, la fecha de corte, el 1 de FIN.MES, el formato de fecha, HOY()).** Ninguna se descarta, pero no van todas en la voz. Cada aclaración entra como `nota` o `rotulo` de ≤ 4 s, con voz solo si cabe en ≤ 8 palabras. Van en voz el $ ("el signo de dólar deja fija la celda") y "fecha de corte = hoy, con =HOY() en B1", porque sin eso no se entiende el giro. En nota sin voz van el separador coma/punto y coma, el formato de fecha y el 0/1 de FIN.MES.
4. **Retención quiere 6 s de moraleja tras el giro, el espectador quiere "a veces la IA avisa sola".** Las dos cosas se pueden cumplir. El titular 29 y el 30 se funden en un beat de ≤ 12 s que diga las dos ideas y abra bucle hacia la 8 ("y en la fórmula ocho la prueba me salvó otra vez"). Es verdad: la 8 sí tiene una detección real (el SI.ERROR cuando no hay vencidas).
5. **"La propia IA me lo advirtió" sin mostrarlo (espectador).** Se muestra en 3–4 s (respuesta real 7a de `respuestas-ia.md`, como `rotulo` o chat corto) o se saca. No se deja como afirmación sin imagen.
6. **Verificador: "abrir la plantilla en Excel para la web antes de aprobar".** No bloquea la reescritura del guion, pero **sí bloquea la aprobación del guion**. Queda como condición del creador (ver más abajo) y el guionista no puede darla por cumplida.

### Correcciones obligatorias (en este orden)

**A. Veracidad (levantan el veto)**
1. **Plan y rótulos:** todos los `chat` con `"app": "Claude"` sin `modelo`. Cambiar en la voz cada "una IA gratis" que se refiera a lo que usé yo por "una IA" o "Claude". "Gratis" solo puede ir junto a Excel para la web y la plantilla.
2. **ChatGPT/Copilot (escena 37):** "Puedes pegar el mismo prompt en ChatGPT o Copilot. La respuesta puede cambiar, y por eso existe la prueba."
3. **Hook sin cifras sin medir:** quitar las 4 horas y "en minutos". Primera frase de la escena 1 según la contradicción 2.
4. **Versiones de Excel (escena 2):** "Excel para la web, que es gratis, Microsoft 365 o Excel 2024. En 2021 fallan la 3 y la 8; en 2016 y 2019, varias más." Va como `rotulo` o `lista` de ≤ 6 s (ver C).
5. **FIN.MES (escena 17):** sacar "fallan con los meses de treinta y uno". Poner: "Sumar treinta días no te da el fin del mes siguiente: del 4 de agosto llegas al 3 de septiembre."
6. **Chat 7b recortado:** indicarlo en pantalla, "(y 2 casos más)", y que la parte visible no cambie el sentido de la respuesta real.
7. **`fuentes` en guion.json:** agregar entradas con URL de Microsoft Support para Excel para la web gratis, la disponibilidad de BUSCARX/FILTRAR/UNICOS/ORDENAR (2021+), TEXTODESPUES/ELEGIRCOLS (365/2024) y el separador de listas según la configuración regional. Si una URL no se puede comprobar en la sesión, se marca "pendiente" y la frase no se afirma.
8. **Descripción (se pasa a `completar_video.py`):** "Respuestas generadas con Claude el 25/10/2026. Documentos y empresa de ejemplo ficticios. Voz sintética: la primera persona del guion es un recurso narrativo." Corregir en este debate las rutas `build/guion/` por `produccion/video02/fuente/` (lo hace el guionista en sus notas de la ronda 2).

**B. Hook (meta: fórmula 1 escribiéndose antes de 0:40)**
9. **0:00–0:04:** planilla con columnas vacías que se llenan en cascada (3 s, `rellenar` encadenados), sin plano fijo. **0:04:** `zoom` 1,8x al sello PAGADO + voz con el nombre del cliente y el cobro doble ("Esta fórmula marcaba como vencida una factura de [cliente] que ya estaba pagada"). Usar el cliente real de la fila del giro, no Ferretería El Tornillo si no corresponde: verificarlo contra la planilla. "Ojo con ese sello" va en el mismo beat que el sello, no 12 s después.
10. **Requisitos (escena 2):** de 24 s a un `rotulo`/`lista` de ≤ 6 s. Nada del texto de requisitos se lee en voz salvo "Excel para la web, gratis" (lo demás va en pantalla y en la descripción). Escena 3 (Distribuidora Sur) ≤ 12 s. Promesa ("al final vas a poder pedir tus fórmulas y comprobarlas") antes de 0:25.

**C. Ritmo y variedad visual (metas medibles, se comprueban con `motor.py --sin-voz`)**
11. **Excel ≤ 60 % del tiempo total** (hoy está en ~55 % por escenas, pero con hook y fórmulas alargadas el riesgo es pasarse). El guionista informa el porcentaje medido en sus notas.
12. **Un cambio visual fuerte (`capitulo`, `antes_despues`, `cifra`, `aviso`) cada 60–90 s, sin huecos de más de 90 s.** Ninguna escena `excel` dura más de 45 s seguidos: el tramo 1:30–3:05 se parte. Hay que sumar al menos dos `antes_despues` con cifras verificadas: "10 clientes → 5" (fórmulas 2 y 9) y "8 vencidas → 4" (giro, junto a la cifra 610.575). Cada fórmula se abre con un `rotulo` dentro de la hoja.
13. **Fórmula 1 ≤ 35 s de hoja:** fusionar escenas 6 y 7. Coma/punto y coma como `nota` sin voz y PAP-201 en ≤ 4 s.
14. **Reenganche antes del corte de 5:10:** FIN.MES como nota de 3 s. Antes del corte va la frase "Después viene la fórmula que casi le cobra dos veces a un cliente" (reemplaza o resume el titular 18, que no debe pasar de 10 s).
15. **Legibilidad en celular:** `zoom` ≥ 1,6x antes de cada `escribir`/`calcular` y de cada `nota` con fórmula. El `zoom_fuera` solo va para mostrar resultados completos.
16. **Cierre en un solo beat de ≤ 12 s antes de `final`:** plantilla + video recomendado. La regla de "no pegues datos reales de clientes" pasa a la escena del prompt de 3 partes (24 o 32). La escena 36 (cuándo no usar la IA) queda, pero ≤ 25 s.

**D. Claridad (todas obligatorias, son cortas)**
17. Aplicar las aclaraciones del espectador según la contradicción 3: "está entero en la hoja Prompts" (mapa ilegible), "en la misma conversación, así no lo repites", capítulo 7 → "7. SI: el estado de cada factura" (el subtítulo "la IA como revisora" puede ir en el `rotulo`), "desborda" → "ocupa las celdas de abajo: déjalas vacías". En la fórmula 2 no se narra "la copio hacia abajo". "Gratis, a cambio de tu email" solo si el lead magnet efectivamente pide email (confirmar con el creador; si no se sabe, decir solo "gratis en la descripción").

### Opcionales
- Un `antes_despues` adicional en la fórmula 3 (texto pegado → vendedor separado) si sobra tiempo dentro de los 10,5 min.
- Un único plano de `panel_ia` dentro de la hoja para una fórmula sin chat, como variedad. Solo si el panel se puede rotular "Claude" y no "Copilot". Si no, no.
- Duración final entre 9 y 10,5 min. Recortar es preferible a alargar.

### No tocar (funciona)
- Datos de Distribuidora Sur, las cifras verificadas (8 → 4 vencidas, 2.446.165 → 1.835.590, 610.575, Carla Ruiz 1.215.000, 5/10 clientes) y el orden de las 10 fórmulas.
- El giro de la fórmula 7 (escribirla yo, pasarla por la prueba, la respuesta real 7b) y la secuencia `aviso` "tres clientes, cuatro facturas" + `cifra` 610.575.
- El método mapa/meta/prueba y su `lista` (escena 24).
- La fórmula 8 con SI.ERROR como segunda prueba real y el agrupado de las fórmulas 9 y 10.
- La escena `comparar` "¿Cuándo no usar la IA?" (se recorta, no se saca) y el `final` al video 1.
- Los cambios de herramientas del guionista (plantilla_xlsx.py, motor.js, estilos.css). Se aceptan: no se revierten.

### Condiciones del creador (no las cumple el guionista; bloquean la publicación, no la ronda 2)
- Abrir `produccion/video02/plantilla/Distribuidora Sur.xlsx` en Excel para la web en español y confirmar: las fórmulas 1, 3, 8 y 9; que D2 y A8 desborden sin `@`; el orden de ORDENAR con tildes; que UNICOS no distinga mayúsculas. Si falla el desborde, agregar metadatos de matriz dinámica en `plantilla_xlsx.py` o reescribir esas celdas a mano.
- Opcional: correr en claude.ai gratis los prompts 1, 2, 4, 6, 7a, 7b y 8 de `respuestas-ia.md`. Si coinciden en sentido, se puede volver a poner el plan en el rótulo. Si la 7b no menciona "Pagado", el giro vuelve a debate.
- Agregar las hojas Prompts y Práctica a la plantilla antes de publicarla (la voz las promete).
- Siguen abiertas la condición de demanda y la medición de [N] de la etapa de idea.

## Respuesta del guionista a la ronda 1

Archivos: `produccion/video02/guion.json` (34 escenas, 1.082 palabras), el generador `produccion/video02/fuente/armar_guion.py`, la verificación `produccion/video02/fuente/verificar_lo242.py` y la medición de metas `produccion/video02/fuente/metas.py`. Las rutas `build/guion/` de mis notas de la ronda 1 ya apuntan a `produccion/video02/fuente/`.

### Metas medibles (tiempos estimados por el motor sin voz, `fuente/metas.py`)

| Meta | Resultado | ¿Cumple? |
|---|---|---|
| Fórmula 1 en pantalla antes de 0:40 | 0:38 (respuesta del chat con BUSCARX); el prompt empieza en 0:31 | Sí |
| Excel ≤ 60 % del tiempo | 59 % | Sí, justo |
| Ninguna escena excel de más de 45 s seguidos | La más larga dura 34 s (fórmula 8) | Sí |
| Cambio visual fuerte cada 60–90 s | El mayor hueco entre `capitulo`/`antes_despues`/`cifra`/`aviso` es de 70 s | Sí |
| Zoom ≥ 1,6x en cada `calcular` y `nota` | 0 casos por debajo (el hook va a 1,8x en el sello) | Sí |
| Cierre ≤ 12 s | 11 s (un beat: plantilla + video del PDF), después la pantalla final | Sí |
| Chats ≤ 12 s (7b ≤ 20 s) | 9,5 / 10,2 / 11,4 / 11,9 s; 7b, 12,7 s | Sí |
| `puntuar_guion.py` ≥ 85 | 100/100 | Sí |
| `verificar_lo242.py` sin diferencias | 109/109 valores coinciden | Sí |
| Duración 9–10,5 min (opcional) | 8:19 estimada sin voz; con `voz_tts` debería quedar en unos 8:40 | No: lo que limita es la meta de Excel (59 %). El brief prefiere recortar a alargar |

### Correcciones obligatorias
1. **Plan y rótulos: aceptada.** Todos los chats llevan `"app": "Claude"` sin `modelo`. Ninguna frase de la voz dice que la IA es gratis. "Gratis" solo va con Excel para la web y la plantilla. `respuestas-ia.md` está actualizado.
2. **ChatGPT/Copilot: aceptada** con el texto del verificador ("Puedes pegar el mismo prompt en ChatGPT o Copilot. La respuesta puede cambiar, y por eso existe la prueba."), como cuarta fila de `comparar`.
3. **Hook sin cifras sin medir: aceptada.** Ya no están las 4 horas ni "en minutos". Queda: "Esta planilla se completa sola, con diez fórmulas. Nueve se las pedí a una IA. / La décima la escribí yo. Ojo con ese sello: marcaba vencida una factura de Ferretería El Tornillo que ya estaba pagada."
4. **Versiones de Excel: aceptada con una salvedad.** Va como `rotulo` de 5,5 s, sin voz salvo "Excel para la web, que es gratis". **Excel 2024 no aparece:** confirmé con Microsoft que TEXTODESPUES se aplica a 2024, pero no pude confirmar ELEGIRCOLS en 2024 (support.microsoft.com no resuelve desde la sesión; solo vi el texto en resultados de búsqueda). Por la regla de la obligatoria 7, no lo afirmo. El rótulo dice: "o Microsoft 365 · en Excel 2021 fallan la 3 y la 8 · en 2016/2019, varias más · empresa y datos ficticios".
5. **FIN.MES: aceptada** con el texto del verificador ("del 4 de agosto llegas al 3 de septiembre").
6. **Chat 7b recortado: aceptada.** Dice "(y 2 casos más)". En la 8 también.
7. **`fuentes`: aceptada.** BUSCARX (2021+, no 2016/2019) y TEXTODESPUES (365 y 2024), con URL de Microsoft Support. Excel para la web gratis, con la página de Microsoft de plantillas gratuitas para Excel para la web. ELEGIRCOLS en 2024 y el separador de listas quedan **"pendiente"**, y la voz no los afirma: la nota dice "¿Tu Excel usa coma? Dilo en el mapa". También saqué "una función de 2022", que no tenía fuente en pantalla.
8. **Descripción: aceptada.** El texto va en `guion.json` → `descripcion_avisos` para `completar_video.py`.
9. **Hook visual: aceptada.** De 0:00 a 0:04, las columnas Precio, Neto, Vence y Estado de Pedidos se llenan en cascada (cuatro `rellenar`). En el segundo beat (~0:05), `zoom` 1,8x al sello PAGADO sobre L2:M2, con el nombre del cliente en la voz. **Fila del sello comprobada (punto 5 del coordinador):** es la fila 2, Ferretería El Tornillo, vence 30/09/2026, Pagado "Sí", y la fórmula escrita a mano la marca "Vencido". El generador lo controla con un `assert`. "Ojo con ese sello" está en el mismo beat que el sello.
10. **Requisitos y promesa: aceptada.** Saqué las escenas "Lo que necesitas" y "Distribuidora Sur": los requisitos van en el rótulo del hook y la suciedad de los datos se muestra en las fórmulas 2 y 3. La promesa ("Al final vas a poder pedir tus fórmulas y comprobarlas antes de confiar en ellas") empieza en ~0:22.
11. **Excel ≤ 60 %: aceptada.** 59 % medido.
12. **Variedad: aceptada.** Ninguna escena excel pasa de 34 s. Sumé dos `antes_despues` con cifras verificadas: "10 → 5 clientes" después de la fórmula 2 y "8 → 4 vencidas · 1.835.590" en el giro, junto a la cifra 610.575. Para eso agregué a `antes_despues` la opción `valor` + `sufijo` (cifra en vez de reloj; documentada en `sistema/motor-v2.md`). Cada fórmula se abre con un `rotulo` ("02 · Se la pedí a Claude · el prompt está en la hoja Prompts", etc.). Las fórmulas 1, 3 y 5 llevan el capítulo como campo de escena, sin pantalla de capítulo aparte.
13. **Fórmula 1 ≤ 35 s de hoja: aceptada.** Uní el chat con Productos y Pedidos, y Productos pasó a la plantilla. La hoja de la fórmula 1 dura 27 s. Coma/punto y coma va como nota sin voz y PAP-201 en ~4 s.
14. **Reenganche antes del corte: aceptada.** FIN.MES se explica con notas de 3 s (el 1/0 y el formato de fecha, sin voz). El titular previo al corte dura 8 s: "Después viene la fórmula que casi le cobra dos veces a un cliente. Si te está sirviendo, suscríbete."
15. **Zoom: aceptada** (ver la tabla).
16. **Cierre: aceptada.** Un beat de 11 s (plantilla + video del PDF). La regla de los datos reales pasó a la lista del prompt de 3 partes. `comparar` dura 23 s y va precedido de un `aviso` de 3 s ("Antes de cerrar: cuándo no usar la IA"), que también corta el último tramo largo.
17. **Claridad: aceptada.** Ahora se dice: "está entero en la hoja Prompts", "en la misma conversación, así no repito el mapa", el capítulo 7 se llama "SI: el estado de cada factura" (con "La IA como revisora" en el rótulo) y "ocupa las celdas de abajo: déjalas vacías". En la fórmula 2 no se narra la copia hacia abajo. En la voz van el $ ("deja fija la celda del mes al copiar") y "En tu planilla, pon =HOY() en B1; aquí la dejo fija". **Corrijo la contradicción 3:** el orquestador proponía "fecha de corte = hoy, con =HOY() en B1", pero la plantilla tiene B1 fijo (04/11/2026), porque si no los números del video no coincidirían. Por eso la voz dice "en tu planilla, pon igual a hoy" y el Léeme de la plantilla lo explica. "A cambio de tu email" no aparece: solo "gratis en la descripción".
- **Contradicción 5 ("la propia IA me lo advirtió"): aceptada.** Se muestra durante 4 s como `rotulo` con la cita real de la respuesta 2: "Claude: «las siglas también cambian: SRL queda Srl»".
- **Contradicción 4: aceptada.** La moraleja es un solo beat de 9 s que abre bucle hacia la 8 ("y en la fórmula ocho me salvó otra vez").

### Punto 4 del coordinador: hojas Prompts y Práctica
Elegí la opción del bloque `plantilla_extra` en `guion.json`, que lee `herramientas/plantilla_xlsx.py`. Hacerlo en el generador después de la herramienta obligaba a reabrir el .xlsx con openpyxl, y eso borra los metadatos de matriz dinámica de FILTRAR y UNICOS. Formato: `{"hojas": [{"nombre", "celdas", "anchos", "formulas": false}], "leeme": "..."}`. Con `"formulas": false`, las celdas que empiezan con "=" se guardan como texto. Además agregué `datos.celdas_plantilla` (datos completos de la hoja que no se ven en pantalla): sin la escena de la planilla sucia, las columnas crudas de Pedidos solo existían ocultas. La plantilla queda con las hojas Léeme, Pedidos, Resumen, Productos, Prompts y Práctica:
- **Prompts:** los 11 prompts textuales de `respuestas-ia.md` (el generador los lee de ahí), con la fórmula que dio Claude y la columna "Qué revisar".
- **Práctica:** Pedidos con los datos sucios y sin fórmulas, incluido el PAP-201.
- **Léeme:** versiones de Excel (sin afirmar 2024), fecha de corte fija con =HOY() para uso real, y "Respuestas generadas con Claude el 25/10/2026".

### Capturas revisadas (≈ 40, `motor.py --sin-voz --cuadros`)
Las corregí después de revisarlas:
- El zoom a PAP-201 mostraba fondo negro bajo la hoja.
- La fórmula del chat 7b tocaba la caja de texto.

Lo demás está bien en pantalla: el sello PAGADO a 1,8x, los rótulos, los dos `antes_despues` con cifras, las notas a 1,6x, el gráfico final y la pantalla final.

### Pendientes (no los puede cerrar el guionista)
- Condiciones del creador: abrir la plantilla en Excel para la web (desbordes D2 y A8, ORDENAR con tildes, UNICOS y mayúsculas, fórmulas 1, 3, 8 y 9) y, si quiere el rótulo con el plan, correr los prompts en claude.ai gratis.
- `plantilla_xlsx.py` guarda las matrices dinámicas con `ref` de una sola celda (`D2`, `A8`). Excel suele guardar el rango desbordado; hay que confirmarlo al abrir el archivo.
- Confirmar ELEGIRCOLS en Excel 2024 y conseguir una URL oficial del separador de listas, si se quiere decir en el video.
- La duración queda por debajo de 9 min (ver la tabla). Si el showrunner prefiere 9 min o más, hay que relajar la meta de Excel o agregar escenas que no sean de Excel.

## Respuesta del guionista a la ronda 2

Apliqué todo en `produccion/video02/fuente/armar_guion.py` y regeneré `guion.json` (35 escenas, 1.130 palabras) y la plantilla.

### Metas (tiempos estimados por el motor sin voz, `fuente/metas.py`)

| Meta | Ronda 2 | Ronda 3 | ¿Cumple? |
|---|---|---|---|
| Fórmula 1 en pantalla antes de 0:40 | 0:38 | 0:39 | Sí, justo (el hook ganó una frase) |
| Excel ≤ 60 % | 59 % | 56 % | Sí |
| Ninguna escena excel de más de 45 s | 34 s | 34 s | Sí |
| Cambio fuerte cada 60–90 s | 70 s | 69 s | Sí |
| Zoom ≥ 1,6x en calcular/nota | 0 fallos | 0 fallos | Sí |
| Cierre ≤ 12 s | 11 s | 11 s | Sí |
| Chats ≤ 12 s (7b ≤ 20 s) | — | 11,0 / 10,2 / 11,4 / 11,9; 7b 12,7 s | Sí |
| Promesa antes de 0:25 | ~0:22 | ~0:19 | Sí |
| `puntuar_guion.py` | 100 | 100 | Sí |
| `verificar_lo242.py` | 109/109 | 109/109 | Sí |
| Duración | 8:19 | 8:36 (unos 9 min con voz) | Dentro del margen si la voz real estira lo previsto |

### Puntos del orquestador
1. "Y una la escribí yo": **aplicado.**
2. Requisitos: **aplicado.** Hay un beat propio de ~4 s: "Solo necesitas Excel para la web, gratis, y una IA gratis: yo uso Claude." El rótulo queda en una línea grande, "Excel web gratis o 365", y debajo, en chico, "no sirve 2016/2019 · datos ficticios". Lo partí en título y sub porque con todo en el título ocupaba dos líneas y tapaba media hoja. El detalle de Excel 2021 va en `descripcion_avisos` y en la hoja Léeme. Nota de veracidad: "una IA gratis" describe lo que necesita el espectador, no el plan que usé yo; el rótulo de los chats sigue sin plan.
3. Mapa explicado la primera vez: **aplicado** ("Le digo qué hay en cada columna, eso es el mapa, y qué quiero, la meta"). El sub del rótulo dice "el mapa completo está en la hoja Prompts".
4. `antes_despues` FIN.MES: **aplicado.** Entre las fórmulas 4 y 5: "3 sep." (+30 días ✗) contra "30 sep." (FIN.MES ✓). El capítulo 5 empieza ahí. Quité la pausa de 4,2 s. La explicación del 1/0 y del formato de fecha va en dos beats cortos con voz, y las notas pasaron a C3 para que no se corten a la derecha.
5. "Antes de cerrar, un aviso honesto": **quitado.** El `aviso` dice y narra "¿Y cuándo conviene no pedírsela a la IA?". La primera fila de `comparar` ya no repite la pregunta.
6. Beat largo de la escena 5: **partido en dos.** El primero resalta, una por una, las 3 variantes del cliente. **Cambié la ferretería por el kiosco:** en la planilla, las tres variantes que solo difieren en mayúsculas son las del kiosco (B4 "kiosco la esquina", B7 "KIOSCO LA ESQUINA", B12 "Kiosco La Esquina"). Las de la ferretería se diferencian por espacios, que en pantalla casi no se ven. La voz dice "al mismo kiosco de tres formas".
7. Bucle en el titular de la plantilla: **aplicado.**
8. Nota del 0 % en I7, con zoom 1,6x a esa zona: **aplicado.**
9. "Lunes": **quitado de todo el guion** (0 apariciones). Ahora dice "cobranza de la semana", "esta semana habría llamado", "a quién llamar esta semana". El capítulo 8 se llama "FILTRAR: cobranza en Excel, el reporte de la semana".
10. Fuentes: **actualizadas** con microsoft.com/microsoft-365/free-office-online-for-the-web, exceljet y bettersolutions (ELEGIRCOLS no está en 2021).
11. `respuestas-ia.md` unificado: correrlo en claude.ai gratis es opcional y solo sirve para volver a poner el plan en el rótulo.
12. Plantilla gratis sin email: la voz dice "gratis en la descripción" y `descripcion_avisos` dice "Plantilla gratis, sin registro". La palabra "email" no aparece en el guion.
13. Prompts con `"duracion": 1.2`: **aplicado a los cinco chats.**

### Capturas revisadas (~25)
Revisé: sello PAGADO a 1,8x, rótulo de requisitos, chat 1 centrado, las 3 variantes del kiosco, la nota del 0 % en I7, el `antes_despues` FIN.MES, las notas de FIN.MES, el chat 7b, UNICOS y el gráfico final. Corregí el rótulo, que ocupaba dos líneas, y las notas de FIN.MES, que se cortaban a la derecha.

### Pendiente (no lo puede cerrar el guionista)
- Que el creador abra la plantilla en Excel para la web: es lo que sostiene el veto del verificador.

## Pulido final (después de la ronda 3)
Apliqué los 7 ajustes opcionales en `fuente/armar_guion.py`:
1. Rótulo del hook: "Excel web gratis o 365 · en 2021 fallan 2 de las 10 · 2016/2019 no · datos ficticios". En la voz: "La empresa es inventada".
2. Quité el beat "Al final vas a poder…". Queda "Solo necesitas Excel para la web y una IA gratis: yo uso Claude".
3. Titular de la escena 8 en dos beats: primero el bucle de la fórmula 7 y después, con texto nuevo en pantalla, "Prompts gratis: hoja Prompts".
4. La fórmula 2 es del kiosco de punta a punta: las variantes 1 y 2 en rojo, la correcta en verde, y el resultado narrado es "Kiosco La Esquina", con las tres filas en verde.
5. Quité el `aviso` que repetía el título: la pregunta es el primer beat de `comparar` (`beats_filas`).
6. "Lo cubre: si no hay vencidas, muestra un mensaje en vez de un error."
7. Agregué un `antes_despues` de ~5,6 s antes de la fórmula 10 ("Ferretería: 2 vencidas a mano → 0 con la prueba"). Para eso la escena 9/10 se partió en dos. El beat "Y si alguien paga…" pasó a dos beats: zoom a la lista con la nota "Pedidos › Pagado = Sí → sale de la lista", y después zoom a la fecha de corte. La columna Pagado no está en la hoja Resumen, así que la mostré con una nota.

Metas después del pulido: fórmula 1 a 0:34, Excel 56 %, escena excel más larga 35 s, mayor hueco entre cambios fuertes 75 s, ningún calcular/nota bajo 1,6x, cierre 11 s, chats ≤ 12,7 s. `puntuar_guion` 100 y `verificar_lo242` 109/109. Revisé unas 12 capturas de los tramos que cambiaron y corregí dos cosas: las etiquetas del kiosco se superponían con la columna C y la tercera línea del titular se cortaba.
