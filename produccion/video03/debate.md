# video03 · Debate

## Ronda 1 · decisión del showrunner

**Etapa:** idea · **Resultado de `pipeline.py evaluar`:** REVISAR · **Nota:** 7,28 (umbral 8,0)
Criterios: demanda 8,0 · empaque 6,5 (mín. 8) · diferenciación 7,0 · rpm 7,0 · encaje 8,0.
Lectura: la idea es sólida (demanda probada, base y cifras reproducibles, giro que no depende de que la IA falle). Falla por una sola razón: el **empaque principal vende lo mismo que ya vende el top** ("se actualiza solo", dashboard de colores), mientras que lo único que nadie tiene (el −90 % del mes incompleto) quedó como variante. Los tres críticos coinciden: se invierte.

Cifras recalculadas desde la tabla de idea.md: 441.000 / 4.574.425 = −90,4 %; 441.000 / 409.900 = +7,6 %; 4.574.425 / 4.213.090 = +8,6 %. Están bien. El 03/11/2026 cae en martes.

### Dato nuevo del orquestador: el motor ya no es un bloqueo

El motor v2 (plantilla `excel`) ya tiene `grafico` con `id` (más `alto` y `max`), `actualizar_grafico`, `tarjeta`, `actualizar_tarjeta`, `desplegable` y `quitar`. No hay gráfico de líneas. Quedan resueltas las objeciones de motor de retención y espectador, y cae el "sin 1 y 2, recomiendo no producir" de idea.md. La tendencia mensual va en barras.

### Contradicciones resueltas (prioridad: veracidad y políticas > promesa cumplida > retención > estilo)

1. **Título principal: el ideador propone el 1 y los tres críticos el giro.** Gana la retención con el respaldo de la diferenciación: el título 1 es casi el de EXCELeINFO y el giro es lo único que no está en el top. El giro pasa a principal y "se actualiza solo" queda como A/B 2.
2. **"Dice −90 % y es mentira" (retención) contra "el error de cada inicio de mes" (retención y espectador).** Gana el segundo por veracidad: la propia idea dice que el −90,4 % es "correcto en lo literal y engañoso", así que llamarlo "mentira" en el título exagera. Además, el número ya va en la miniatura y no debe repetirse en el título.
3. **Miniatura B: sello "FALSO" (la propuesta) contra "sin sello" (retención).** Gana la retención: el sello responde la pregunta antes del clic y una tarjeta sola no se lee como dashboard. El espectador elogió la B por el −90 %, no por el sello, así que no hay conflicto real.
4. **Título 3 "¿un solo prompt? Lo probé": hipótesis (investigador), solo si la corrida sale mal (retención) o fuera del A/B (espectador).** Gana la veracidad: el título promete un veredicto que todavía no existe porque la corrida en claude.ai no se hizo. Sale del A/B y queda condicionado al resultado real (ver corrección 2).
5. **Tabla en 10 s (retención) contra el antes/después rango contra Tabla (espectador).** Gana la promesa cumplida: "pegas y se rehace" depende de la Tabla, y ese contraste es la prueba. Se hace en ≤ 20 s y dentro de la pregunta 1, no como bloque aparte, así que la retención también queda cubierta.
6. **El hook de retención incluye "casi lo mando así".** Gana la veracidad: es una anécdota inventada en primera persona con voz sintética. Se reemplaza por algo que no afirme un hecho que no pasó, por ejemplo "y así le llegaría a tu jefe".
7. **Fecha del 03/11 contra "no fijarla hasta tener el motor".** El motor ya está, así que la fecha se mantiene, pero ahora la condicionan las verificaciones del creador (ver abajo). El giro no puede depender de publicar el día 3: la voz dice "el día 3 de cada mes", nunca un "hoy" suelto.

### Correcciones obligatorias para el ideador (en orden)

1. **Empaque principal = giro.**
   - Título principal: `Dashboard en Excel con IA: el error de cada inicio de mes` (57).
   - Miniatura principal = **B híbrida**: dashboard oscuro reconocible al fondo (tarjetas y barras, sin fórmulas legibles), una tarjeta gigante **"−90 %"** en rojo con la flecha hacia abajo que se sale del cuadro, **sin sello** y con el texto **`¿ES REAL?`**. Mantener la burbuja de chat chica de la serie.
   - Reescribir "Por qué el principal" con este argumento y sacar de ahí la afirmación de que el título 3 es "el formato de los outliers".
2. **Variantes A/B.**
   - A/B 2: `Dashboard en Excel con IA: pegas pedidos y se rehace solo` (57) con la miniatura A rehecha. El texto debe ser concreto y no un eslogan ("LUNES RESUELTO" se descarta): por ejemplo, el cronómetro "LUNES: 20 s", pero **solo si los 20 s se midieron**. Si no se midieron, usar un texto sin cifra.
   - A/B 3: queda vacío hasta la corrida real del "un solo prompt". Si sale mal o a medias, entra `Le pedí a la IA un dashboard en 1 mensaje: esto salió` (53) con la miniatura C que muestre lo que salió de verdad. Si sale bien, no hay título 3 y el acto se reduce a 20 s.
   - Se elimina "¿EN SERIO?".
   - El título 1 actual ("gratis: se actualiza solo") pasa a reserva.
3. **Hook en 2 ideas, con el −90 % antes de los 8 s.**
   - Base: "Pego los pedidos y este dashboard se rehace solo. Pero me dice que las ventas cayeron un 90 %, y no es cierto." Después, una línea que deje el bucle abierto sin "al final te muestro".
   - "Gratis, sin macros, Excel para la web" y "datos inventados" van al rótulo y a la voz de 0:25.
   - "Un solo prompt" sale del hook.
4. **Promesa y fórmulas que cumplan "se rehace solo".**
   - Siempre "pegas los pedidos y se rehace solo" (nunca "se actualiza solo" a secas), en la promesa, la línea 1 de la descripción y la voz.
   - El gráfico mensual pasa a un **rango fijo de 12 meses (enero a diciembre)** con SUMAR.SI.CONJUNTO y los meses futuros en 0. Con el rango actual de enero a octubre, la barra de noviembre no existe y los pedidos pegados el 02/11 no se verían. En el resultado final se tiene que ver crecer la barra de noviembre (`actualizar_grafico`).
5. **Escaleta para la retención.**
   - El acto "lo probé" dura ≤ 30 s.
   - El paso 0 desaparece como bloque: la Tabla entra dentro de la pregunta 1 con el antes/después (en un rango, pegas una fila y el total no cambia; en la Tabla, sí), en ≤ 20 s.
   - La tarjeta "−90 %" queda visible en una esquina durante las preguntas 3 y 4 (`tarjeta` + `quitar` al resolverse el giro).
   - La primera vez que aparece el método, una línea de explicación: "Mapa · Meta · Prueba".
   - Sobre la fórmula del desplegable, decir: "no tienes que memorizarla: la escribe la IA y está en la plantilla".
6. **Diferenciación, evidencia y producción, alineadas con lo verificado.**
   - Sacar el punto 4 ("primero las preguntas") de los diferenciadores: lo tiene EXCELeINFO. Se queda como estructura del video.
   - En "Lectura honesta", sumar las vistas por día en español (500–1.600/día, 0,0x–0,5x, ninguno nuevo en 60 días) y bajar la expectativa de búsqueda: el video depende de sugeridos y de video02.
   - En "Límites", nombrar el modo dashboard nativo de Excel con Copilot (Insiders o de pago, a verificar el día del guion) y anotar un seguimiento en `ideas.md`.
   - Reescribir la sección de producción con las acciones nuevas del motor (sin líneas) y quitar el riesgo de motor.

### Opcionales

- RPM: citar la ficha como fuente ("dashboards e informes de gestión", tema de RPM alto). Si se quiere una cifra, que sea con fuente y fecha; si no, no se inventa. Usar `informe de ventas`, `cuentas por cobrar` y `Power BI` en capítulos y descripción.
- Densidad: una frase en 0:25 del tipo "te enseño el criterio; la plantilla hace el resto".
- Reintentar `investigar.py sugerencias` o Google Trends para la palabra clave. No bloquea.

### Condiciones fuera del ideador (no bloquean la ronda 2; sí bloquean el guion o la fecha)

- **Investigador, antes de la ronda 2:** revisar El Inge Francisco, "¿Claude SIRVE?" (youtu.be/1pJqarOwgbA). Si ahí se revisa la exactitud de un KPI por un mes incompleto, el giro pierde exclusividad y el principal se reevalúa en la ronda 2. Los otros 4 del top ya quedaron confirmados por descripción (VBA, Gemini Canvas, Google Sheets, conversor de pago).
- **Creador (el orquestador puede no tener acceso a claude.ai), antes del guion:**
  - correr en claude.ai gratis el "un solo prompt" con el archivo y la Prueba del bloque 2, y guardar las respuestas textuales con fecha y captura en `respuestas-ia.md`;
  - confirmar que el plan gratuito lee .xlsx;
  - en Excel para la web gratis y en español, comprobar la expansión de la Tabla al pegar, las referencias estructuradas, la lista desplegable y que los gráficos conserven el formato;
  - medir [N] y los "20 s".
  - Lo que no se corra queda marcado como pendiente y no sale en el video.
- **Fecha:** se mantiene el martes 03/11/2026, 13:00 CDMX, si esas verificaciones están el **viernes 30/10**. Si no, recomiendo que el creador la mueva antes de recortar la demostración.

### No tocar (funciona)

- La base Distribuidora Sur (250 pedidos, semilla fija, las 12 filas de video02), la tabla de cifras y la fecha de corte fija en `Dashboard!B1`.
- El giro con dos ramas (la IA lo ve o lo ve la persona) y la regla de no inventar la respuesta. La corrección en dos tarjetas: mismo tramo y mes cerrado, con la tarjeta grande en el mes cerrado.
- Las 4 preguntas como columna vertebral, el corte de anuncios en 5:00, el giro entre el 60 % y el 75 % y el desplegable "Carla Ruiz".
- La plantilla gratis y sin registro (hojas `Pedidos`, `Dashboard`, `Prompts` y `Tus datos`) y lo de pago fuera del video.
- Las restricciones heredadas de video02 (regla 4, datos ficticios declarados, `;`, Excel para la web, sin VBA ni Power Query).
- La palabra clave `dashboard en excel con ia` al inicio de todos los títulos, menos el A/B 3 condicional.
- Riesgos de contenido inauténtico y de temas sensibles: bien resueltos.

## Ronda 2 · decisión del showrunner

**Etapa:** idea · **Resultado de `pipeline.py evaluar`:** REVISAR · **Nota:** 7,85 (umbral 8,0)
Criterios: demanda 8 · empaque 8 · diferenciación 8 · rpm 7 · encaje 8. Todos están sobre su mínimo.
Lectura: la ronda 1 se aplicó bien. Faltan 0,15 y salen de pulir el empaque, no de cambiar la idea. **La ronda 3 es la última**: no se abre nada nuevo.

### Contradicciones resueltas (prioridad: veracidad y políticas > promesa cumplida > retención > estilo)

1. **Título principal: consecuencia o causa.** Gana la **consecuencia**, con intención de tutorial. "Inicio de mes" responde la pregunta de la miniatura antes del clic (retención) y suena a arreglar un tablero que Laura no tiene (espectador). La causa no se descarta: queda como A/B, que es lo que propuso retención.
2. **"El número que asusta a tu jefe" contra Martín, que es el jefe.** Gana la versión sin "jefe", que sirve para los dos perfiles.
3. **"Y el error que todos cometen".** Se descarta por veracidad: "todos" no está medido.
4. **"SIN TOCAR NADA" en la miniatura A.** Se descarta por promesa cumplida: hay que pegar los pedidos, y eso mismo pidió el espectador en la ronda 1.

### Correcciones obligatorias (en orden)

1. **Títulos.**
   - Principal (A/B 1): `Dashboard en Excel con IA paso a paso: el número que asusta` (59), con la miniatura B. "Paso a paso" cubre la búsqueda de tutorial y es la idea 2 de `ideas.md`. "El número que asusta" es la consecuencia, no la causa.
   - A/B 2: `Dashboard en Excel con IA: el error de cada inicio de mes` (57), con la misma miniatura B (se prueba el título, no la miniatura).
   - A/B 3: `Dashboard en Excel con IA: pegas pedidos y se rehace solo` (57), con la miniatura A sin la palabra "pegas" en el texto: "LUNES: 20 s" si se midió; si no, el antes/después de la barra de noviembre (vacía → llena) sin texto. Si la corrida del mensaje único sale mal, el condicional "Le pedí a la IA un dashboard en 1 mensaje: esto salió" reemplaza a este A/B 3.
   - Agregar en `publicacion.md` la regla del investigador: a las 48–72 h comparar el CTR de las variantes y, si una gana con claridad, pasarla a principal.
2. **Miniatura B que se lea como Excel en el celular.**
   - El tablero de fondo al 35–45 % de brillo, con barras en el verde de Excel y una franja de cuadrícula con los encabezados A, B, C y una pestaña de hoja.
   - La tarjeta "−90 %" tapa como mucho el 50 % del tablero.
   - El texto pasa de "¿ES REAL?" (genérico) a **`¿CAYERON?`**.
   - Rehacer `miniatura-b.html` y `.png`, y revisarla a 168 px de ancho.
3. **Hook sin la causa.**
   - Se corta en: "…cayeron un 90 %, y no es cierto. Y con ese número decidirías el lunes."
   - Fuera "el día 3 de cada mes" y "tu jefe".
   - La causa aparece recién en el giro (pasados los 5:10).
   - Reenganche de 2:10: "y la tarjeta que lo arregla no es la que piensas".
4. **Intención de tutorial y "gratis" fuera del título.**
   - Línea 1 de la descripción: "Arma paso a paso un dashboard de ventas en Excel con IA: pegas los pedidos y se rehace solo, en Excel para la web gratis, sin macros."
   - Rótulo en pantalla desde 0:15: "Excel para la web gratis + Claude" (el plan de Claude según la corrección 5).
   - En el resultado final, una frase sobre el +146,8 %: "el de 3 días salta como loco; el que miras el lunes es el del mes cerrado: +8,6 %", con la tarjeta grande resaltada.
5. **Texto de diferenciación y RPM: cerrar lo que sigue abierto.**
   - Reemplazar la viñeta "falta revisar a El Inge" por lo revisado: no trata el mes incompleto, así que el giro sigue siendo exclusivo.
   - Diferenciador 1, textual: "Ningún video del top trata el error del mes incompleto ni muestra cómo detectar un KPI correcto en lo literal pero engañoso".
   - Sumar los 2 comentarios de 1pJqarOwgbA (25 y 20 votos) como evidencia cualitativa de una sola fuente.
   - RPM: una referencia con fuente y fecha si existe. Si no hay ninguna verificable, escribir "sin cifra verificada" y dejar `informe de ventas`, `cuentas por cobrar` y `Power BI` en los capítulos. No se inventa una cifra.

### Condición dura: "Claude gratis" (creador, bloquea el cierre del guion, no la ronda 3)

- **Antes de cerrar el guion**, el creador corre en claude.ai con el plan gratuito, con el .xlsx adjunto: (a) el mensaje único del acto "lo probé" y (b) la Prueba del bloque 2. Guarda las respuestas textuales con fecha y captura en `produccion/video03/respuestas-ia.md`. El orquestador no tiene acceso a claude.ai: no se simula.
- **Si funciona:** el rótulo es "Claude · versión gratuita" y "Claude gratis" puede ir en la voz y la descripción.
- **Si pide pagar, se agotan los mensajes o no lee el .xlsx:** se muestra tal cual en el acto "lo probé" (es un veredicto honesto y alimenta el A/B 3 condicional). El rótulo pasa a "Claude" a secas y "gratis" queda solo para Excel para la web. Los prompts Mapa · Meta · Prueba no necesitan el archivo (el Mapa describe las columnas), así que la demo principal no se cae.
- **Plazo:** viernes 30/10, junto con las pruebas de Excel para la web (Tabla, referencias estructuradas, desplegable, gráficos) y la medición de tiempos. Sin las tres pruebas con captura, el guion puede escribirse con marcas de pendiente, pero no se cierra y la fecha del 03/11 se mueve.

### No tocar (funciona)

- La miniatura B como concepto: el −90 % rojo gigante sobre el tablero, sin sello y sin repetir la cifra en el título.
- El giro con dos ramas, las cifras, la base y el gráfico de 12 meses con la barra de noviembre que crece.
- La escaleta de la ronda 1: el acto "lo probé" en ≤ 30 s, la Tabla dentro de la pregunta 1 y el −90 % en la esquina.
- La palabra clave al inicio de los títulos, la plantilla gratis y las restricciones heredadas de video02.

### Si la ronda 3 no aprueba

Recomendaré **aprobar con las objeciones pendientes documentadas**, salvo que falle la veracidad. La idea ya pasa todos los mínimos y lo que queda es pulido de empaque que se valida mejor con el CTR real que con otra ronda.

## Escalada · ronda 3 · recomendación del showrunner al creador

**Resultado:** ESCALADO tras 3 rondas, con nota 7,85 (umbral 8,0). Criterios: demanda 8 · empaque 8 · diferenciación 8 · rpm 7 · encaje 8. Todos están sobre su mínimo y no hay vetos.

**Recomendación: aprobar con las objeciones pendientes documentadas.**
- La distancia al umbral es de 0,15 y la explica el RPM (7). Ese criterio solo sube con una cifra con fuente, que hoy no existe, y otra reescritura no la crea.
- Las objeciones de la ronda 3 son de pulido de empaque y de guion, no de la idea. El espectador dice que la miniatura B es "la mejor de las tres rondas".
- Rehacer costaría la fecha sin una mejora esperable. Descartar no se justifica con demanda 8 y un giro que sigue siendo exclusivo.

Comando para el creador (forzar es una decisión humana; no la tomo yo):
`python3 herramientas/pipeline.py forzar video03 idea "3 rondas, todos los criterios sobre el mínimo; RPM sin cifra con fuente; ajustes de empaque de la ronda 3 pasan a la etapa empaque; bloqueo de verificaciones antes de cerrar el guion"`

### Contradicciones de la ronda 3

1. **"(y el número falso)" (retención).** Se descarta por veracidad: el −90,4 % es correcto en lo literal. Es la misma decisión que con "mentira" en la ronda 1.
2. **A/B 2 "inicio de mes": retención pide sacarlo y el espectador lo prefiere.** Lo decide el test, no una ronda más: se queda.
3. **Criterio de la ganadora del A/B.** Gana la veracidad del dato (investigador): "Probar y comparar" elige por proporción de tiempo de visualización, no por CTR.

### Ajustes para el seo-empaquetador (etapa empaque; no se rehace la idea)

1. **Miniatura B.**
   - La tarjeta lleva el título **"VENTAS"** grande (alrededor del 40 % del alto de la cifra), para que se lea "VENTAS −90 %" con "¿CAYERON?".
   - La flecha apunta a la barra de noviembre, sin taparla.
   - Revisarla otra vez a 168 px.
2. **Títulos del A/B.**
   - A/B 1: `Dashboard en Excel con IA paso a paso: el número que asusta` (59). Comprobar en la vista previa de Studio, en celular, que "asusta" no se trunque. Si se trunca, pasa a principal `Dashboard en Excel con IA: no lo mandes sin esta prueba` (55).
   - A/B 2: `Dashboard en Excel con IA: el error de cada inicio de mes` (57).
   - A/B 3: `Dashboard en Excel con IA: no lo mandes sin esta prueba` (55), con la **miniatura B**, salvo dos excepciones:
     - si se midieron los 20 s, el A/B 3 es "pegas pedidos y se rehace solo" con la miniatura A "LUNES: 20 s";
     - si el mensaje único falla, entra el condicional "Le pedí a la IA…".
   - Nunca "falso" ni "mentira".
3. **Regla del A/B en `publicacion.md`:** "si YouTube declara una ganadora por tiempo de visualización, pasa a principal; el CTR se anota como dato secundario para el analista".
4. **Línea 1 alternativa en `publicacion.md`,** lista para usar si falla una prueba:
   - sin "gratis" si falla Excel para la web gratis;
   - sin "se rehace solo" (por ejemplo, "se actualiza al pegar los pedidos y pulsar Actualizar") si falla la expansión de la Tabla o de los gráficos;
   - rótulo "Claude" a secas si falla claude.ai gratis.
5. **Texto de `idea.md`, línea 32:** "no trata el mes incompleto ni muestra un método para verificar KPI; solo concluye, en general, que hay que revisar lo que da la IA".

### Para el guionista (etapa guion)

- Hook: "Y el lunes tomarías decisiones con ese número" (se lee mejor en voz sintética).
- Reenganche de 2:10: "en un rato te muestro por qué ese −90 % no es cierto, y qué número sí mirar el lunes".

### Pendientes documentados (no bloquean el forzado; sí el cierre del guion o la publicación)

- **Condición dura de la ronda 2, sin cambios:** antes del viernes 30/10, el creador corre en claude.ai gratis el mensaje único y la Prueba con el .xlsx, prueba Excel para la web (Tabla, referencias estructuradas, desplegable, gráficos) y mide los tiempos, todo con captura. Sin eso, el guion no se cierra, la promesa no se publica y el 03/11 se mueve.
- **RPM sin cifra con fuente:** queda como tarea del investigador para el informe de noviembre.

## Guion · ronda 1 · respuesta del guionista (26/10/2026)

**Entregable:** `produccion/video03/guion.json` (30 escenas, motor v2). `puntuar_guion.py`: **100/100**. Duración estimada con la lógica de tiempos del motor: **≈ 9,1 min** (rango de la idea: 9–11). `plantilla_xlsx.py --verificar`: **sin diferencias** en las celdas que calcula LibreOffice. Las 12 celdas de la lista de cobranza (FILTRAR + ORDENAR + ELEGIRCOLS, que LibreOffice 24.2 no calcula) se compararon aparte contra `datos_base.py` y coinciden. Los estados que solo salen en el video también se recalcularon en LibreOffice con copias modificadas de la plantilla y coinciden: Carla Ruiz, corte al 31/10 y los 3 pedidos de hoy. Las cifras nuevas quedaron en `fuente/datos_base.py`, en la sección `extras`.

Mapa de tiempos (estimado): hook 0:00 · lo probé 0:33 · 4 preguntas 0:52 · P1 1:04 · reenganche 2:52 · P2 2:52 · CTA de suscripción 3:47 (42 %) · P3 3:59 · P4 4:59 · **corte de anuncios y giro 5:24 (60 %)** · aviso 6:03 · corrección 6:21 · resultado 7:04 · límites 7:51 · plantilla 8:24 · pantalla final 8:44.

### Decisiones del showrunner incorporadas
- **Hook (ronda 3):** «Pego los pedidos y este dashboard se rehace solo. Pero me dice que las ventas cayeron un 90 %, y no es cierto. Y el lunes tomarías decisiones con ese número.»
  - El −90,4 % entra en pantalla a los ≈ 3,5 s, con zoom.
  - El hook no dice «hoy», «día 3», «jefe» ni la causa.
  - Bucle abierto sin «al final»: «Te muestro cómo armarlo paso a paso, con IA, y cómo atrapar ese número antes de mandarlo.»
- **Reenganche de 2:10 (ronda 3), textual:** «En un rato te muestro por qué ese −90 % no es cierto… y qué número sí mirar el lunes.» Va en un `titular` al cerrar la pregunta 1.
- **Flecha y foco en la barra de noviembre:** en la pregunta 2 la barra de noviembre se pinta de amarillo (`destacar`), con zoom, y la voz dice «mira la barra de noviembre: casi no existe». En el resultado final es la barra que crece.
- **Rótulo desde 0:15:** «Excel para la web gratis + Claude», sin macros y con los datos ficticios dichos en voz. Pasa a «Claude · versión gratuita» solo si pasa la condición dura.
- **«Lo probé» ≤ 30 s:** dura ≈ 18 s y está marcado como `condicional` (se elimina si no hay corrida real).
- **Tabla dentro de la pregunta 1 en ≈ 20 s:** el antes/después usa dos números. Con rango fijo, al pegar el pedido del 02/11 el total sigue en 46.145.220. Con la Tabla, pasa a 46.586.220.
- **Tarjeta −90 % en la esquina durante las preguntas 3 y 4:** se crea con `id: "alarma"` en cada escena (las tarjetas viven dentro de su escena) y se quita en la corrección.
- **Otras correcciones de la ronda 1:**
  - El método se explica en una línea la primera vez: «mapa, meta y prueba».
  - La voz dice «No tienes que memorizar las fórmulas: te las da la IA, y están en la plantilla».
  - El desplegable usa «Carla Ruiz».
  - El gráfico va de enero a diciembre fijos, con `max` fijo para que noviembre crezca sin reescalar.
- **Giro con dos ramas:**
  - Las dos voces quedan escritas: `voz` es la rama A y `voz_rama_b`, la B.
  - La comprobación con el corte al 31/10 (+8,6 %) se hace en las dos ramas, así el giro no depende de la IA.
  - La corrección usa dos tarjetas: la grande es el mes cerrado (+8,6 %) y la chica, el mismo tramo (+7,6 %, «con 3 días, es ruido»).
  - En el final, el mismo tramo salta a +146,8 % y el mes cerrado sigue en +8,6 %, con la frase de la ronda 2.
- **Datos ficticios declarados en voz:** «los datos son inventados». Separador `;`. Sin VBA ni Power Query.
- **Límites:**
  - Power BI y tabla dinámica.
  - Modo dashboard con Copilot: verificado hoy solo con fuentes no oficiales (vista previa para Insiders, sin fecha de Microsoft). Por eso la voz dice «Excel está probando un modo dashboard… está en prueba» y no da precios ni fechas.
  - Datos reales de clientes.
  - «La IA no sabe qué te importa».
- **Pantalla final:** video02, con «Es este video, aquí en pantalla».

### Desvíos de la escaleta de la idea (con argumento)
1. **CTA de suscripción: de 2:10 a 3:47 (42 %).** La regla del guionista y `puntuar_guion.py` exigen pedirla después del 35 % del video. En 2:10 (≈ 24 %) habría costado 6 puntos y la habría pedido antes de entregar el segundo resultado. A las 2:10 queda solo el reenganche.
2. **Corte de anuncios: de 5:00 a ≈ 5:24.** Va donde termina la pregunta 4 y empieza «Ahora sí: ese −90 %». La escena tiene la marca `"corte_anuncios": true`, y el creador lo coloca en Studio según la duración real con voz.
3. **La pregunta 4 no tiene escena de chat.** La fórmula es la de video02 sobre la Tabla y se dice así. Ahorra unos 15 s y evita un prompt más sin respuesta real.
4. **El cronómetro «a mano contra con IA» no está.** No hay tiempos medidos, así que el final dice «Lo armas una vez. Cada lunes: pegar, y listo». La marca `pendiente_verificar` indica dónde va el `antes_despues` si el creador mide.

### Objeciones de los críticos de la idea que tocaban al guion
- **Espectador ronda 3, «decidirías el lunes» se traba en voz sintética: aceptada.** Cambié el hook y también el `aviso` del giro.
- **Espectador ronda 3, reenganche de 2:10: aceptada.** Va textual.
- **Espectador ronda 3, la flecha a la barra de noviembre: aceptada en el guion.** Hay `destacar` y zoom. En la miniatura la ajusta la etapa empaque.
- **Retención ronda 1, «tres tramos seguidos sin dashboard nuevo»: aceptada.** Entre el hook y el primer cálculo hay un chat de 18 s, una lista de 12 s y la Tabla con dos tarjetas. El primer número nuevo cae en ≈ 1:20.
- **Espectador ronda 1, «Laura no sabe la diferencia entre rango y Tabla»: aceptada.** Se muestra con números, no con palabras.
- **Espectador ronda 1, jerga y fórmula del desplegable: aceptada.** El método va en una línea, se dice «no tienes que memorizarlas» y el asterisco se explica como «cualquier texto».
- **Retención y espectador, «gratis» y «se rehace solo» sin verificar: aceptada como bloqueo.** El guion no se cierra hasta las pruebas del creador. Si falla la expansión de la Tabla, cambian las escenas 4, 25 y 26 (Pedidos y el dashboard final), además de la línea 1.
- **Retención ronda 3, «(y el número falso)»: rechazada.** Por veracidad: el −90,4 % es correcto en lo literal. En la voz nunca se dice «falso» ni «mentira»; se dice «no es cierto» que las ventas cayeron, que sí es exacto.

### Cambios en herramientas (necesarios para este guion)
- `produccion/render/motor/motor.js` y `sistema/motor-v2.md`: nueva opción `datos.filas` en `excel`, con los números de fila visibles. Sirve para mostrar el encabezado inmovilizado y las filas 241–254 de la Tabla, con su número real. Probada con `--cuadros`.
- `herramientas/plantilla_xlsx.py`:
  - Hojas extra desde un CSV, con Tabla de Excel con nombre (para `Pedidos[Neto]`) y fórmulas por fila.
  - `posicion` para fijar el orden de las hojas.
  - `graficos` (barras) y `validaciones` (lista desplegable).
  - Con `--verificar`, las celdas con funciones que LibreOffice 24.2 no calcula se informan como «verificar aparte» en lugar de contar como error. Con video02 pasa de 72 a 31 diferencias: las 41 restantes ahora se listan aparte, sin cambios en la plantilla de video02.

### Pendientes del creador (bloquean el cierre del guion, no la ronda)
1. Correr los prompts de `respuestas-ia.md` en claude.ai gratis y reemplazar los 5 textos «PENDIENTE» (y elegir la rama del giro y la del «lo probé»).
2. Excel para la web gratis, en español:
   - abrir la plantilla;
   - que la Tabla se expanda al pegar debajo;
   - que funcionen las referencias `Pedidos[...]`, el desplegable de B2 y los 3 gráficos;
   - que la lista de cobranza dé Colegio Nuevo Horizonte 1.215.000 arriba y 16 filas.
3. Medir el armado y el lunes, si se quiere cronómetro.
4. Fijar en Studio el corte de anuncios y la tarjeta hacia video02 (escena 16, beat 3; escenas y beats se cuentan desde 0).

## Guion · ronda 1 · decisión del showrunner

**Etapa:** guion · **Resultado de `pipeline.py evaluar`:** REVISAR · **Nota:** 7,03
Criterios: hook 7 · ritmo 7 · promesa 7,5 · claridad 6,5 · veracidad 7, **con veto del verificador**.
Lectura: la estructura, las cifras (todas recalculadas por el verificador, OK) y el giro con dos ramas funcionan. El veto viene de frases y de la plantilla que afirman cosas que no son ciertas o que todavía no se corrieron. La claridad baja porque el título promete "paso a paso" y varias piezas aparecen ya hechas. Todo se arregla sin alargar el video.
Escenas numeradas desde 0, como en `guion.json`. Los críticos citan desde 1: la "esc. 1" de retención es la 0 de aquí.

### Datos del orquestador (firmes)
- El creador corre los prompts en claude.ai y prueba la plantilla en Excel para la web; el plazo es el viernes 30/10. Hasta entonces las respuestas siguen pendientes y con ramas, y nada se atribuye a Claude sin texto real.
- La cadencia martes/viernes **no** está confirmada (video02 salió un lunes): no se promete.

### Réplicas del guionista (desvíos de la escaleta)
Se aceptan los 4:
- el CTA al 42 % (regla del guionista);
- el corte de anuncios en ≈ 5:24 con marca para Studio;
- la pregunta 4 sin chat (un prompt menos sin respuesta real);
- sin cronómetro mientras no haya medición.

También se acepta el rechazo de "número falso" (veracidad).

### Contradicciones resueltas (prioridad: veracidad > promesa > retención > estilo)

1. **Más "paso a paso" (espectador) contra recortar (retención).** Gana la promesa, porque el título dice "paso a paso", pero se paga con recortes de relleno. Lo que se agrega suma unos 15 s y lo que se quita, unos 60 s (ver la corrección 3). La meta neta es ≤ 9,1 min.
2. **B1 fija contra =HOY().** Gana la veracidad y la promesa. La plantilla trae `=HOY()` en B1, porque con B1 fija los pedidos pegados después del 03/11 no entran y el Estado tampoco se actualiza, así que "se rehace solo" sería falso para el espectador. El video usa la fecha fija y lo dice.
3. **Modo dashboard de Copilot: en voz (idea, ronda 1) o a la descripción (retención).** Va a la descripción. Según el Microsoft 365 Roadmap está "en desarrollo" (Excel canvas, RM569424), así que en voz aporta poco y suma riesgo. Revierto mi pedido de la ronda 1.
4. **Video02: avisar en el minuto 1 (espectador) o al final (retención).** Ni lo uno ni lo otro: una frase en la pregunta 4 ("la columna Estado ya viene en la plantilla; cómo se arma, en el video del final") y la pantalla final sin condicional.
5. **"Datos inventados" solo en el rótulo (retención) o también en voz.** Gana la política: el canal los declara en voz al inicio. Queda en 3 palabras dentro de la frase del rótulo.
6. **"ChatGPT o Copilot gratis" al inicio (espectador).** Entra como "sirve igual con ChatGPT", en 4 palabras. No se dice "Copilot gratis" porque Copilot en Excel es de pago y la frase confunde.

### Correcciones obligatorias (en orden)

1. **Veracidad de la plantilla y de la voz (levanta el veto).**
   - **B1:** `=HOY()` en la plantilla. Léeme: "para ver los números del video, escribe 03/11/2026 en B1".
   - **Voz de la esc. 6:** "Aquí la dejo fija en el 3 de noviembre; en tu plantilla tiene =HOY(), así se actualiza sola cada día."
   - **Hoja Prompts:** la columna "Fórmula que dio Claude" pasa a "Fórmula de la plantilla (verificada)" y se agrega "Respuesta de Claude (fecha)", con `[PENDIENTE]` hasta pegar el texto real.
   - **B7 (la variación ingenua):** sale del Dashboard de la plantilla, para que sea cierto que "la alarma roja se va" y no aparezca el −77,9 % en la esc. 26. La fórmula queda documentada en Prompts como "la ingenua, para que la veas".
   - **Conteo:** sumar a Prompts B11, B12 y Estado, y que la voz diga "todas las fórmulas", no "12".
   - **Esc. 11:** fuera "cada martes y viernes"; queda "suscríbete para el próximo atajo de Excel con IA".
   - **Esc. 27:** fuera la frase de Copilot (va a la descripción con la fuente del Roadmap y la redacción "si tienes Copilot en Excel").
2. **Nada atribuido a Claude antes de la respuesta real.**
   - **Esc. 18 ("Lo vio…"):** escribir ya las dos voces (A: la IA lo señala; B: "esta vez no lo vio; lo compruebo yo") y elegir según `respuestas-ia.md`.
   - **Esc. 13 (el asterisco):** lo explica el narrador, sobre la fórmula de la plantilla, no como "lo que dijo Claude".
   - **Esc. 1:** sigue condicional: si la corrida no dio un dashboard, se elimina.
   - **Rótulo:** "Claude · versión gratuita" solo con captura.
3. **"Paso a paso" sin alargar.**
   - **Se agrega (≈ 15 s):**
     - esc. 4: con `escribir`, la fórmula pasa de `=SUMA(Pedidos!H2:H250)` a `=SUMA(Pedidos[Neto])`, más la línea "en Diseño de tabla le pones de nombre Pedidos". El 46.586.220 aparece después de reescribir, no antes;
     - esc. 10: 5 s de la tabla de meses H:I y "la seleccionas, Insertar, Gráfico de columnas";
     - una línea sobre qué es una tarjeta: "una celda grande con un solo número";
     - esc. 5: "copia este prompt de la plantilla y cambia solo los nombres de tus columnas".
   - **Se quita (≈ 60 s):**
     - esc. 0: la logística (0:19–0:32) queda en el rótulo fijo "Excel para la web gratis + Claude · datos inventados" y una frase de voz: "Sin macros, los datos son inventados y sirve igual con ChatGPT. Lo armamos paso a paso, y a mitad del video atrapamos ese número". Fuera "la plantilla hace el resto", que pasa a la esc. 28;
     - las cifras en voz van redondeadas ("46,6 millones", "4,6 millones", "1 millón") y el total del año se dice una sola vez; en pantalla, la cifra exacta;
     - pregunta 3 en ≈ 35 s: fuera Diego Paz y el papel higiénico en voz (quedan en el gráfico);
     - esc. 19 a 21: se quita "La fórmula no está mal…" y se fusionan el `aviso` y el `antes_despues` en un solo antes/después con la consecuencia ("frenarías compras por una caída que no existe");
     - esc. 27: límites en 2 frases (volumen o varias fuentes → tabla dinámica o Power BI; con datos de clientes reales, solo el mapa).
4. **Arranque y bucle abierto.**
   - **Esc. 1–2:** las 4 preguntas se presentan como "lo que tiene que contestar el tablero", no como una forma de comprobar. Mapa · Meta · Prueba se nombra por primera vez en la esc. 5.
   - **Esc. 7 y 11:** los reenganches agregan algo. Por ejemplo, la esc. 11: "la tarjeta roja vuelve, y la arregla una sola pregunta". Fuera "sigue ahí, esperando".
   - **Tarjeta `alarma`:** queda fija en una esquina durante las preguntas 3 y 4, sin nombrarla en voz.
   - **Objetivo:** el giro empieza en ≤ 5:10 gracias a los recortes. Se mantiene en la zona del 55–60 %.
5. **Video02 y cierre.**
   - **Esc. 16:** "la columna Estado ya viene en la plantilla; cómo se arma, en el video del final". La fórmula FILTRAR se explica en una frase ("se queda con los vencidos y los ordena") y en voz: "ELEGIRCOLS no está en Excel 2021; en la web y en 365, sí".
   - **Esc. 29:** la pantalla final sin condicional: "La columna Estado que viste hoy se arma en este video".
   - **Esc. 26:** la tarjeta chica del +146,8 % queda con la regla actual ("con tres días salta; el lunes miras la grande").
6. **Cuadro roto del zoom a 0:08 (esc. 0).** Lo corrige el **guionista** en `guion.json`, porque los parámetros del zoom son del artefacto: centrar el zoom en la tarjeta para que la ventana de Excel no deje negro entre x≈1265 y 1920. El **director visual** valida el cuadro 8 con `--cuadros`, porque es la fuente de la miniatura B.

### Bloqueos (creador, viernes 30/10; no impiden la ronda 2, sí el cierre del guion)
- Respuestas reales en `respuestas-ia.md` (los 5 PENDIENTE, rama del giro y del "lo probé").
- Captura con fecha en Excel para la web de que la Tabla se expande al pegar, registrada en `fuentes`. Sin ella, el verificador mantiene el veto en el cierre aunque la ronda 2 apruebe el texto.
- Las referencias `Pedidos[...]`, el desplegable, los 3 gráficos y la lista de cobranza (Colegio Nuevo Horizonte 1.215.000 arriba, 16 filas).

### No tocar (funciona)
- El hook (las 3 primeras frases) y el reenganche de 2:10, textuales.
- El −90 % en pantalla a los ≈ 3,5 s.
- El giro con dos ramas y la comprobación con el corte al 31/10 en ambas.
- Las dos tarjetas de la corrección: la grande en el mes cerrado (+8,6 %).
- Todas las cifras (verificadas).
- El antes/después rango contra Tabla con números (46.145.220 → 46.586.220).
- El gráfico de 12 meses con `max` fijo y la barra de noviembre que crece.
- El final "pegar, y listo" sin cronómetro inventado.
- "No es cierto" en lugar de "falso" o "mentira".
- El CTA al 42 % y la marca del corte de anuncios.
- Los cambios en las herramientas (`datos.filas` y `plantilla_xlsx.py`): aceptados, pendientes de que el coordinador los confirme.

## Respuesta a la ronda 1 (guion · guionista, 26/10/2026)

**Resultado de los controles:**
- `puntuar_guion.py video03`: **100/100**.
- `plantilla_xlsx.py video03 --verificar`: **sin diferencias** en las celdas calculables. Las 12 celdas de la lista de cobranza (FILTRAR, ORDENAR, ELEGIRCOLS) se informan aparte, como antes, y coinciden con `datos_base.py`.
- Duración estimada: **8,25 min**, por debajo de la meta de ≤ 9,1 min. El giro empieza en **5:07** (62 %).
- Revisé con `--cuadros` los cuadros 8, 80, 88, 200 y 208.

**Prompts:** sus textos **no cambiaron**. En `respuestas-ia.md` solo se actualizaron los números de escena (los prompts 4 y 5 ahora están en las escenas 14 y 19) y las voces que dependen de cada respuesta.

**Hoja Pedidos:** sin cambios. El CSV, la Tabla y la fórmula de Estado siguen igual, así que no regeneré `Distribuidora Sur - Pedidos 2026.xlsx`.

### Correcciones obligatorias del showrunner
1. **Veracidad de la plantilla y de la voz: aceptada.**
   - **B1:** `=HOY()` en la plantilla. Lo aplica el campo nuevo `plantilla_extra.reemplazos` de `plantilla_xlsx.py`: el archivo entregado lleva `=HOY()` y `--verificar` recalcula la versión con 03/11/2026, que es lo que muestra el video.
   - **Léeme y Tus datos (paso 1):** «Para ver los números del video, escribe 03/11/2026 en Dashboard!B1».
   - **Escena 6:** «Aquí la dejo fija en el 3 de noviembre.» + «En tu plantilla tiene igual a hoy, así se actualiza sola cada día», con una nota `=HOY()` en B1.
   - **Hoja Prompts:** las columnas ahora son «Fórmula de la plantilla (verificada)» y «Respuesta de Claude (fecha)», esta última con `[PENDIENTE: respuesta real]`.
   - **B7 fuera del Dashboard:** la corrección se hace **en la misma celda**. En la escena 22, B7 pasa de `=B6/B5-1` a la fórmula del mes cerrado, con la etiqueta A7 reescrita, y B8 es el mismo tramo.
     - La plantilla no tiene la variación ingenua. Así «la alarma roja se va» es cierto y el −77,9 % desaparece de la escena 26.
     - La ingenua queda en Prompts como la fila 3b, «la ingenua, para que la veas».
   - **Conteo:** la voz dice «todas las fórmulas están en la plantilla, verificadas». Prompts ahora trae B3–B8, B10–B12, D2, H2, I2, L2, O2 y Estado (Pedidos!K2).
   - **Escena 12:** «suscríbete para el próximo atajo de Excel con IA», sin días.
   - **Escena 27:** sin Copilot. Va a `descripcion_avisos` («Si tienes Copilot en Excel: … Excel canvas … RM569424») y a `fuentes`, con la entrada del Roadmap que reemplaza la fuente no oficial.
2. **Nada atribuido a Claude antes de la respuesta real: aceptada.**
   - **Escena 19, beat 2:** la voz por defecto es neutra («Su respuesta queda en pantalla, tal cual. Y lo compruebo yo, con la fecha de corte.»). `voz_rama_a` y `voz_rama_b` quedan escritas, con `elegir_rama` apuntando a `respuestas-ia.md`.
   - **El asterisco:** lo explica el narrador sobre la fórmula de la plantilla (escena 15: «En la plantilla, el criterio del vendedor es este…»). El chat de la escena 14 solo muestra la respuesta pendiente.
   - **Escenas 5 y 9:** la voz no describe lo que devolvió Claude («Su respuesta, tal cual. Las fórmulas que uso son las de la plantilla.»).
   - **Escena 1:** sigue condicional, ahora también si la corrida «no dio un dashboard».
   - **Rótulo:** «versión gratuita» solo con captura (`pendiente_verificar`).
3. **«Paso a paso» sin alargar: aceptada.**
   - Lo que se agrega:
     - **Escena 4:** el total vive en L248. Se ve `=SUMA(Pedidos!H2:H250)`, pegar no lo cambia, se crea la Tabla («en Diseño de tabla le pongo de nombre Pedidos») y **se reescribe** a `=SUMA(Pedidos[Neto])`. El 46.586.220 aparece después de reescribir.
     - **Escena 10, nueva y solo de video:** la tabla de meses H2:I13, «la seleccionas, Insertar, Gráfico de columnas», y el gráfico aparece.
     - **Escena 6:** «una tarjeta es eso: una celda grande, con un solo número».
     - **Escena 5:** «Copia este prompt de la plantilla y cambia solo los nombres de tus columnas», con un rótulo que menciona la coma.
   - Lo que se quita:
     - **Escena 0:** sale la logística. Queda el rótulo «Excel para la web gratis + Claude · datos inventados · sirve igual con ChatGPT» y la frase del brief en 2 beats. «La plantilla hace el resto» pasa a la escena 28.
     - **Cifras en voz redondeadas:** 46,6 millones (dicho una sola vez, en la escena 4), 4,6 millones, 441 mil, un millón, 47,2 millones, 16,3 millones, 1,2 millones y casi 3 millones. En pantalla, la cifra exacta.
     - **Pregunta 3:** unos 32 s (chat de 6 s + excel de 26 s). Salen Diego Paz y el papel higiénico en voz.
     - **Giro:** sale «La fórmula no está mal…». El `aviso` y el `antes_despues` quedan fusionados en uno solo, con la consecuencia «frenarías compras por una caída que no existe».
     - **Límites:** 2 frases.
4. **Arranque y bucle abierto: aceptada.**
   - Las 4 preguntas se presentan como «lo que tiene que contestar el tablero del lunes». El rótulo «Mapa · Meta · Prueba» salió de «lo probé»: el método aparece por primera vez en la escena 5.
   - **Escena 12:** «La tarjeta roja vuelve, y la arregla una sola pregunta».
   - **Tarjeta `alarma`:** fija en las escenas 15 y 17, sin nombrarla en voz. Salió «sigue ahí, esperando».
   - **Giro:** empieza en 5:07, cumple el ≤ 5:10. Con el video más corto (8,25 min), el 5:07 cae en el 62 %, no en el 55–60 %. No lo fuerzo: para bajarlo habría que alargar el final o recortar las preguntas, y las dos cosas chocan con otras correcciones.
5. **Video02 y cierre: aceptada.**
   - **Escena 17:** «La columna Estado ya viene en la plantilla; cómo se arma, en el video del final», con la tarjeta de YouTube.
   - **FILTRAR en una frase:** «se queda con los vencidos y los ordena».
   - **En voz:** «Ojo: ELEGIRCOLS no está en Excel 2021; en la web y en 365, sí».
   - **Escena 29:** «La columna Estado que viste hoy se arma en este video…», sin condicional.
   - **Escena 26:** «Con tres días, salta; el lunes miras la grande».
6. **Zoom de 0:08: aceptada.**
   - El zoom pasa a `C1:E7` a 1,4x (antes `F1:F4` a 1,7x) y la tarjeta −90 % va en x = 1244.
   - El cálculo de la cámara deja el centro en x = 909 y y = 414. Con eso la ventana cubre el cuadro: borde derecho en 1927 px, superior en −20 px e inferior en 1211 px.
   - El cuadro 8 se sacó con `--cuadros`: sin negro y con las 3 tarjetas y el gráfico enteros. Falta la validación del director visual para la miniatura.

### Objeciones de los críticos (`rondas/guion-1.json`)
**Retención**
1. **Logística de 0:19–0:32 y «la plantilla hace el resto»: aceptada.** Ver la corrección 3. El bucle queda en «Te muestro el armado paso a paso, y a mitad del video atrapamos ese número».
2. **Zoom de 0:08: aceptada** (corrección 6).
3. **Las 4 preguntas mezcladas con el método: aceptada.** Ver la corrección 4.
   - Cerrar «lo probé» con «Pero mira este número»: **rechazada**. Supone que el dashboard de Claude trae esa tarjeta, y eso no se sabe hasta la corrida. Queda «¿cómo sabes si esos números están bien?», que sirve con cualquier resultado.
4. **El bucle se paga tarde y los reenganches suenan a relleno: aceptada.** El giro pasa de 5:24 a 5:07, la pregunta 3 dura unos 32 s y los reenganches agregan algo.
5. **Cifras completas en voz: aceptada** (corrección 3).
6. **Tres escenas que repiten «tres días contra un mes»: aceptada.** Quedan dos: la demostración con el corte al 31/10 y un solo antes/después con la consecuencia.
7. **«Lo vio» da por hecha la rama A: aceptada.** Voz neutra más las dos ramas escritas.
8. **Unos 70 s de cierre:**
   - **Aceptada:** límites en 2 frases, pantalla final sin condicional y la escena 17 sin excluir a quien no vio video02.
   - **ChatGPT y Copilot a la descripción: aceptada en parte.** Copilot va a la descripción. «Sirve igual con ChatGPT» pasa al inicio, por la decisión 6 del showrunner. El cierre baja a unos 54 s.

**Verificador**
1. **«En tu plantilla dice igual a hoy» es falso: aceptada.** La plantilla trae `=HOY()` (corrección 1).
2. **«Fórmula que dio Claude»: aceptada.** La columna se renombró y se agregó la de la respuesta, pendiente.
3. **Fuente no oficial del modo dashboard: aceptada.** Ahora es RM569424 y solo está en la descripción, con «Si tienes Copilot en Excel».
4. **Convertir en Tabla no reescribe la fórmula: aceptada.** Hay `escribir` de `=SUMA(Pedidos[Neto])` antes del 46.586.220.
5. **Expansión de la Tabla sin captura: aceptada como bloqueo.** En `fuentes` figura como «PENDIENTE: captura con fecha». Sin ella, el guion no se cierra.
6. **«Las 12 fórmulas»: aceptada.** La voz dice «todas las fórmulas» y Prompts las trae todas.
7. **B7 y el −77,9 %: aceptada.** B7 se corrige en la misma celda y la ingenua sale del Dashboard.
8. **«Martes y viernes»: aceptada.** Se quitó.
9. **Escenas 14 y 19 atribuyen a Claude: aceptada** (corrección 2). «Gratis» para Claude sigue solo con captura.
10. **Cifras verificadas: sin cambios.** No toqué ninguna cifra; solo cambió cómo se dicen en voz.

**Espectador**
1. **El gráfico y las tarjetas aparecen hechos: aceptada.** Hay una escena nueva con la tabla de meses y «Insertar › Gráfico de columnas», más la línea sobre qué es una tarjeta.
2. **No se ve el cambio a `Pedidos[Neto]` ni el nombre de la Tabla: aceptada.**
3. **El bloque del Mapa: aceptada.** «Copia este prompt de la plantilla y cambia solo los nombres de tus columnas», con el rótulo sobre la coma.
4. **La cobranza excluye a quien no vio video02 y ELEGIRCOLS no se explica: aceptada,** salvo el aviso «en el minuto 1». Por la decisión 4 del showrunner, el aviso va en la pregunta 4.
5. **El −90 % se resuelve tarde: aceptada en parte.** El giro adelanta 17 s y se acortan las preguntas 3 y 4. No lo muevo antes de la pregunta 3 porque el showrunner mantiene el orden y el corte de anuncios.
6. **La tarjeta chica del +146,8 % confunde: aceptada.** Queda la regla «Con tres días, salta; el lunes miras la grande».
7. **«Yo uso Claude» y Laura usa ChatGPT: aceptada.** «Sirve igual con ChatGPT» va en voz y en el rótulo desde 0:10. No se dice «Copilot gratis» (decisión 6).
8. **B1 no se entiende y los 46,5 millones se dicen tres veces: aceptada.** Se dice «tiene igual a hoy, así se actualiza sola cada día», con la nota `=HOY()`, y el total se dice una sola vez.

### Cambios en herramientas (ronda 2)
- `herramientas/plantilla_xlsx.py`:
  - `plantilla_extra.reemplazos` cambia celdas solo en el archivo entregado; `--verificar` usa los valores del video.
  - `plantilla_extra.formatos` fija formatos de número (`mmm`, `0.0%`, `#,##0`, fechas).

### Pendientes del creador (sin cambios)
1. Respuestas reales de los prompts 1–5 y 5b, con la rama del giro y la de «lo probé».
2. Captura con fecha de la Tabla expandiéndose en Excel para la web, para `fuentes`.
3. Comprobar en Excel para la web `Pedidos[...]`, el desplegable, los 3 gráficos, la lista de cobranza y que `=HOY()` en B1 funcione.
4. **Nuevo:** con 8,25 min estimados, quedan unos 15 s de margen sobre los 8 min que necesitan los anuncios a mitad de video. Si la voz real sale más rápida, hay que avisar antes de recortar algo más.
