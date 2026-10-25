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
- **Cómo lo comprobé:** `produccion/video02/build/guion/verificar_lo242.py` usa la misma reconstrucción y comparación que `--verificar`, pero en una copia de la plantilla cambia BUSCARX por SI.ERROR(INDICE(COINCIDIR)), TEXTODESPUES por EXTRAE(HALLAR) y los desbordes de FILTRAR/ORDENAR y UNICOS/ORDENAR por fórmulas clásicas (K.ESIMO.MAYOR, SUMAPRODUCTO, MMULT) calculadas sobre los mismos datos. Resultado: **109/109 valores del video coinciden.** Chequeos extra con LibreOffice: 5 clientes distintos con nombres limpios y **10 con los nombres sucios** (CONTAR.SI, que no distingue mayúsculas y sí espacios, como UNICOS); con la fórmula escrita a mano, **8 vencidas y 2.446.165**; corregida, **4 y 1.835.590** (diferencia 610.575). Además, el generador del guion (`build/guion/armar_guion.py`) calcula todos los valores en Python desde los datos crudos, de forma independiente.
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
