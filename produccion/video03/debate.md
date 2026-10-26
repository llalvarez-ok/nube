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
