# Video 03 · Publicación (BORRADOR adelantado: sin render con voz)

**Título principal:** Dashboard en Excel con IA paso a paso: el número que asusta (59 caracteres)
**Metadatos:** `metadatos.json` (título, descripción con `{capitulos}`, 14 etiquetas, categoría 27, playlist y `titulos_ab`, más `titulos_ab_condicionales`)
**Miniatura principal:** `miniatura.png` (= `miniatura-b.png`: «¿CAYERON?» + tarjeta «VENTAS −90 %» sobre la hoja de Excel). `miniatura-a.png` y `miniatura-c.png` quedan para las variantes condicionales del A/B 3.
**Capítulos:** `capitulos-estimados.txt` es una **estimación**: sale del motor sin voz (`build/datos.js`, 26/10, con el guion pulido). `completar_video.py` usa el `capitulos.txt` definitivo, que se genera al renderizar con la voz real. No copies el estimado encima del definitivo.

> **Duración estimada: 7:58** (477,8 s, sin voz). Para los anuncios a mitad del video hacen falta **8:00 o más** con la voz real. Si con la voz da menos, lo resuelve el guionista con contenido (regla del showrunner, etapa visual); el empaque no cambia. Si se elimina el acto «Lo probé» (escena 1, unos 14 s), la duración baja todavía más.

### Por qué la miniatura B es la principal
- Es la única de las tres que no se parece a nada del top en español: todos venden velocidad con dashboards de colores en ángulo (el estilo de la miniatura A). La B vende la consecuencia («¿CAYERON?») sin responderla. El sello «FALSO» se descartó.
- Tiene un solo protagonista (la tarjeta «VENTAS −90 %»). A 168 px se leen «¿CAYERON?» y «−90 %», y la hoja verde con barras se reconoce como Excel (`miniatura-b-168.png`). Los ajustes de la ronda 3 ya están aplicados: «VENTAS» grande en la tarjeta y la flecha que apunta a la barra de noviembre sin taparla.
- Cumple «título y miniatura no se repiten»: la cifra va solo en la miniatura, y el título dice «el número que asusta».
- Es lo que se ve en el segundo 4 del video (el hook), así que la promesa se cumple enseguida. El showrunner la marcó como «no tocar» en las tres rondas del visual.

---

## 1. Pendientes antes de publicar (en este orden; fecha límite: viernes 30/10)

- [ ] **Correr los prompts en claude.ai gratis** (`respuestas-ia.md`): el prompt 1 (mensaje único, con el .xlsx), los prompts 2 a 5 en la misma conversación y sin archivo, y el 5b (el 5 con el .xlsx). Guarda la respuesta textual, la fecha, el modelo y una captura.
  - Anota si el plan gratuito **lee el .xlsx** o pide pagar, si se agotan los mensajes o si no lo lee.
  - Con esa fecha, reemplaza `[FECHA DE LA CORRIDA]` en `metadatos.json` (descripción, «Sobre este video») y en `guion.json` (`descripcion_avisos`).
- [ ] **Elegir las ramas** de las escenas 1, 9 y 19 en `guion.json` (instrucciones en `respuestas-ia.md`). Sin eso, el motor no hace el render final.
- [ ] **Probar la plantilla en Excel para la web** (cuenta gratis, en español), con capturas: que la Tabla se expanda al pegar, que funcionen las referencias `Pedidos[Neto]`, la lista desplegable de B2 y los gráficos, y que las cifras coincidan (−90,4 %, +7,6 %, +8,6 %, +146,8 %, 46.586.220, 47.156.820 y 2.951.090). Agrega la captura con fecha a la fuente de las Tablas en `guion.json`.
- [ ] **Medir los tiempos** del armado y del «lunes» (pegar y listo). Si dan unos 20 s, se activa el A/B 3 alternativo (sección 3).
- [ ] **Línea 1 de la descripción: elegir según las pruebas.** Si todo pasa, va la que ya está en `metadatos.json`. Si algo falla, reemplázala por la que corresponda:

| Si falla… | Línea 1 (reemplaza la de `metadatos.json`) | Otros cambios |
|---|---|---|
| Nada | «Arma paso a paso un dashboard de ventas en Excel con IA: pegas los pedidos y se rehace solo, en Excel para la web gratis, sin macros.» | Si claude.ai gratis leyó el .xlsx y respondió, agrega en «Sobre este video»: «Uso Claude gratis; el mismo prompt sirve en ChatGPT o Copilot, y la respuesta puede cambiar: para eso está la Prueba.» |
| Excel para la web gratis | «Arma paso a paso un dashboard de ventas en Excel con IA: pegas los pedidos y se rehace solo, en Microsoft 365, sin macros.» | En «Qué Excel necesitas», borra la línea de Excel para la web y la fuente de Excel gratis. El rótulo de 0:15 y la voz «Con Excel para la web, gratis» vuelven al guionista |
| La expansión de la Tabla o de los gráficos al pegar | «Arma paso a paso un dashboard de ventas en Excel con IA: se actualiza al pegar los pedidos y pulsar Actualizar, en Excel para la web gratis, sin macros.» | No uses el A/B 3 «pegas pedidos y se rehace solo». El capítulo «Resultado: pegas los pedidos y se rehace solo» y la voz vuelven al guionista |
| claude.ai gratis (pide pagar, se agotan los mensajes o no lee el .xlsx) | La misma de la primera fila | El rótulo dice «Claude» a secas. No escribas «Claude gratis» en ningún lado: «gratis» queda solo para Excel para la web. Si falló el mensaje único, entra el A/B 3 condicional (sección 3) |

- [ ] **Voz y render final.** Con `GOOGLE_TTS_API_KEY` cargada:
  `python3 herramientas/motor.py video03 --alta`
  Genera `produccion/video03/video03.mp4`, `video03.srt` y `capitulos.txt`. Compara `capitulos.txt` con `capitulos-estimados.txt` (si se eliminó la escena 1, desaparece el capítulo «Lo probé») y recalcula los Shorts (sección 5) con las frases de inicio y fin.
- [ ] **Subir la plantilla** (`plantilla/Distribuidora Sur · Dashboard de ventas.xlsx`) a Google Drive («cualquier persona con el enlace puede ver») o a Gumroad (precio 0, sin pedir email, porque el video dice «sin registro»). Reemplaza `[ENLACE PLANTILLA]` en `metadatos.json` y en el comentario fijado (sección 2).
- [ ] **Miniatura C** (solo si falla el mensaje único): el director visual la rehace con la captura real. Hoy `miniatura-c.png` es un borrador y no se sube.

## 2. Subida y metadatos

- [ ] Sube `produccion/video03/video03.mp4` (el render con voz, **no** el `-preview`) desde YouTube Studio como **Privado**.
- [ ] Corre `python3 herramientas/completar_video.py video03`. Carga título, descripción con capítulos, etiquetas, categoría, idioma, `miniatura.png`, subtítulos `video03.srt` y playlist. Si no toma el último video subido, pásale el ID: `python3 herramientas/completar_video.py video03 <ID>`.
- [ ] Revisa en Studio:
  - **Categoría 27, Educación**, igual que video02.
  - Idioma español. «Contenido alterado o sintético»: **no** hace falta marcarlo (la voz no imita a una persona real y no muestra hechos realistas falsos). Igual se declara en la descripción.
  - Capítulos: aparecen solos, con 9 capítulos (8 si se eliminó «Lo probé»), el primero en 0:00.
  - **Playlist:** «Flujos paso a paso con IA». Existe y tiene 3 elementos (consulta a la API del 26/10). No lo puse en «Empieza aquí: lo mejor de Atajos IA»: la puerta de entrada del nicho sigue siendo video02, y video03 entra ahí solo si los datos lo justifican. Si quieres una playlist de la serie (por ejemplo, «Excel + IA: Distribuidora Sur»), créala antes en Studio y agrégala a `metadatos.json`. Si no existe, `completar_video.py` solo avisa «(no existe)».
  - **Tarjeta** hacia video02 (https://youtu.be/drjrSlUxi78) en la pregunta 4, **≈ 4:21**, cuando la voz dice «Estado ya viene en la plantilla». Texto: «Así se arma la columna Estado».
  - **Pantalla final** (últimos 20 s, desde ≈ 7:38): **video02** en el recuadro de la izquierda (la voz dice «Te espero en este video») y **Suscribirse** a la derecha.
  - **Comentario fijado:** «¿Qué número miras primero el lunes en tu tablero? La plantilla gratis, sin registro, con todas las fórmulas y los prompts: [ENLACE PLANTILLA]»
- [ ] **En el celular:** abre la vista previa de Studio y comprueba que «asusta» no se corte en el título. Si se corta, el principal pasa a **«Dashboard en Excel con IA: no lo mandes sin esta prueba»** (55). Cámbialo en `metadatos.json` (`titulo`), y el A/B 1 queda con ese título.

## 3. Prueba A/B (Probar y comparar)

- [ ] En Studio, **Probar y comparar**, carga las 3 variantes. Si las tres llevan la misma miniatura, es una prueba **de títulos**.

| Variante | Título | Miniatura | Ángulo |
|---|---|---|---|
| A/B 1 (principal) | Dashboard en Excel con IA paso a paso: el número que asusta (59) | `miniatura-b.png` | tutorial + consecuencia |
| A/B 2 | Dashboard en Excel con IA: el error de cada inicio de mes (57) | `miniatura-b.png` | la causa (el giro) |
| A/B 3 | Dashboard en Excel con IA: no lo mandes sin esta prueba (55) | `miniatura-b.png` | el método (la Prueba) |

**El A/B 3 cambia en dos casos** (están en `titulos_ab_condicionales`):
- **Si se midieron los 20 s del lunes:** «Dashboard en Excel con IA: pegas pedidos y se rehace solo» (57), con `miniatura-a.png` (con el texto «LUNES: 20 s»; sin texto si no se midió). Pasa a ser una prueba de título y miniatura.
- **Si el mensaje único falló o salió a medias:** «Le pedí a la IA un dashboard en 1 mensaje: esto salió» (53), con `miniatura-c.png` rehecha con la captura real. Este caso tiene prioridad sobre el anterior.
- Nunca usar «falso» ni «mentira»: el −90,4 % es correcto en lo literal.

**Regla para elegir la ganadora:** si YouTube declara una ganadora por **tiempo de visualización**, esa pasa a principal (aunque sea la 2 o la 3). El CTR de cada variante se anota como **dato secundario** para el `analista`. «Probar y comparar» elige por proporción de tiempo de visualización, no por CTR, y puede tardar hasta 2 semanas. No la cortes a mano a las 48 h. Si termina sin ganadora clara, se queda la principal.

## 4. Horario

- [ ] **Recomendado: martes 03/11/2026, 13:00 h de Ciudad de México** (16:00 Buenos Aires y Santiago, 14:00 Bogotá y Lima, 20:00 Madrid).
  - Es el horario fijo del plan (`youtube/03-sistema-operativo.md` §5) y cae en día de cadencia.
  - Es el día 3 del mes, la situación exacta del giro. Igual, la voz nunca dice «hoy», así que el video funciona en cualquier fecha.
  - Todavía no hay datos de «Cuándo están conectados tus espectadores»: video02 salió el 26/10 y el canal casi no tiene historial. Se revisa desde el mes 2.
- [ ] **Si los pendientes de la sección 1 no están el viernes 30/10:** pásalo al **viernes 06/11/2026, 13:00 h CDMX** (el siguiente día de publicación). No lo publiques sin las pruebas: conviene mover la fecha antes que recortar la demostración.
- [ ] Programa la publicación (Visibilidad → Programar).
- No choca con video02: sus Shorts salen el 27, el 29 y el 31/10.

## 5. Shorts (1, 3 y 5 días después)

Tiempos **estimados** (motor sin voz, `build/datos.js` del 26/10). Después del render, busca en `video03.srt` la frase de inicio y la de fin de cada tramo y corrige `desde` y `hasta`. Corta medio segundo antes de la primera palabra y medio después de la última. Cada tramo dura 55 s o menos. El `--titulo` se quema sin salto de línea, así que va corto (unos 20 caracteres). El título completo se escribe al subir. Se recortan del **video final con voz**. En cada Short, en «Video relacionado», enlaza el video largo.

Fechas, si se publica el 03/11: Short 1 el **miércoles 04/11**, Short 2 el **viernes 06/11** y Short 3 el **domingo 08/11**, a las 13:00 h CDMX. Si el largo pasa al 06/11: el 07, el 09 y el 11/11.

### Short 1 · el −90 % que no es cierto · día +1
- **desde** 4:40.2 · **hasta** 5:23.8 (≈ 44 s, estimado)
- **Título:** «Tu dashboard dice −90 % (y no cayeron)»
- **Empieza en:** «Ahora sí: ese −90 %. Aquí entra la tercera parte del método, la prueba.»
- **Termina en:** «…Y el lunes frenarías compras por una caída que no existe.»
- **Por qué se entiende solo:** la tarjeta −90 % está en pantalla, la pregunta a la IA, la comprobación con la fecha de corte (+8,6 %) y la causa (3 días contra 31). Deja abierto qué tarjeta poner en su lugar. Texto final o descripción: «Qué número mirar el lunes, en el video completo.»
- **Depende de la rama de la escena 19.** La rama A (la IA ve el mes incompleto) está en el texto de hoy. Con la rama B («esta vez no lo vio») el tramo sirve igual, porque las frases de inicio y fin no cambian. Revisa que la respuesta real se lea en el cuadro vertical.
- `python3 herramientas/shorts.py video03 4:40.2 5:23.8 --titulo "¿Cayeron un 90 %?" --salida short1-giro`

### Short 2 · el total que no suma lo nuevo · día +3
- **desde** 0:54.0 · **hasta** 1:23.0 (≈ 29 s, estimado)
- **Título:** «Tu total de Excel no suma lo que pegas»
- **Empieza en:** «Este total suma la columna Neto, de la fila 2 a la 250.»
- **Termina en:** «Ahí sí: 46,6 millones. Cada pedido que pegues abajo, la Tabla lo suma.»
- **Por qué se entiende solo:** el problema (pegas el pedido y el total no cambia), la solución (Insertar › Tabla, nombre Pedidos, fórmula con `Pedidos[Neto]`) y el resultado con la cifra. Texto final o descripción: «El dashboard completo con esta Tabla y la plantilla gratis, en el video completo.»
- `python3 herramientas/shorts.py video03 0:54.0 1:23.0 --titulo "El total no se entera" --salida short2-tabla`

### Short 3 · pegar y listo · día +5
- **desde** 6:18.7 · **hasta** 6:56.0 (≈ 37 s, estimado)
- **Título:** «Pegas 3 pedidos y el dashboard se rehace»
- **Empieza en:** «Y ahora, el lunes: llegan tres pedidos. Los copio del sistema y los pego debajo de la Tabla.»
- **Termina en:** «Lo armas una vez. Cada lunes: pegar, y listo.»
- **Por qué se entiende solo:** se ve el dashboard, se pegan 3 filas, crece la barra de noviembre y cambia el acumulado. La frase «la chica salta / la grande sigue» deja la pregunta de por qué hay dos tarjetas. Texto final o descripción: «Cómo se arma, paso a paso, y la plantilla gratis, en el video completo.»
- **Solo si la expansión de la Tabla pasó la prueba en Excel para la web.** Si no pasó, usa la **reserva**: el desplegable por vendedor, **desde** 3:47.3 · **hasta** 4:17.4 (≈ 30 s), de «Quiero elegir un vendedor de una lista» a «Vuelvo a Todos, y el total regresa», con `--titulo "Filtra por vendedor" --salida short3-desplegable`.
- `python3 herramientas/shorts.py video03 6:18.7 6:56.0 --titulo "Pegar y listo" --salida short3-pegar`

Los Shorts quedan en `produccion/video03/shorts/`. Descripción al subirlos: «Video completo: Dashboard en Excel con IA paso a paso (enlace en Video relacionado). Datos ficticios, voz sintética. #Excel #IA #Shorts».

## 6. Después de publicar

- [ ] Sigue «Probar y comparar» hasta que YouTube declare una ganadora (regla de la sección 3).
- [ ] A los 7 y a los 28 días, el `analista` anota en `canales/atajos-ia/aprendizajes.md`: la variante ganadora por tiempo de visualización, el CTR de cada una (dato secundario), la retención en el giro (≈ 4:40–5:24) y cuánto tráfico llegó desde video02 (tarjeta y pantalla final) y desde sugeridos.
- [ ] Si tienes los datos, actualiza la pantalla final de video02 para que mande a video03 (es el paso siguiente de la serie).
