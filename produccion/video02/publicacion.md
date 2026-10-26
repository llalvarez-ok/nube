# Video 02 · Publicación

**Título principal:** 10 fórmulas de Excel con IA: tu planilla se llena sola (54 caracteres)
**Metadatos:** `metadatos.json` (título, descripción con `{capitulos}`, 15 etiquetas, categoría 27, playlists y `titulos_ab`)
**Miniatura:** `miniatura.png` (= `miniatura-a.png`). `miniatura-b.png` y `miniatura-c.png` quedan para la prueba A/B.
**Capítulos:** `capitulos-estimados.txt` es una **estimación** sacada del motor sin voz (`build/datos.js`). El motor genera el `capitulos.txt` definitivo al renderizar con la voz real, y ese es el que usa `completar_video.py`. Los minutos pueden moverse unos segundos.

---

## 1. Pendientes antes de publicar (en este orden)

- [ ] **Decisión pendiente: la etapa idea quedó escalada.** `estado.json` sigue en `etapa: idea` (ronda 3: «escalado», nota 7,42; solo la demanda quedó abajo, 6 contra un mínimo de 7, por falta de datos de la API en el entorno). Forzar es una decisión tuya:
  - aprobarla: `python3 herramientas/pipeline.py forzar video02 idea "demanda pendiente de medir por falta de API; condición antes de publicar"`
  - o medir la demanda primero (punto opcional de abajo) y decidir con datos.
  - El guion quedó **aprobado en provisional** (ronda 3, nota 8,65: hook 9, ritmo 8, promesa 9, claridad 8, veracidad 9). Al forzar la idea, el pipeline avanza solo al guion. La condición del verificador sigue en pie: la comprobación en Excel para la web (punto 3).
- [ ] **Voz y render final.** Carga `GOOGLE_TTS_API_KEY` en el entorno y corre:
  `python3 herramientas/motor.py video02 --alta`
  Esto genera `produccion/video02/video02.mp4`, `video02.srt` y `capitulos.txt` con los tiempos reales. Compara `capitulos.txt` con `capitulos-estimados.txt` y recalcula los tiempos de los Shorts (sección 4).
- [ ] **Plantilla en Excel para la web.** Abre `plantilla/Distribuidora Sur.xlsx` y comprueba:
  - que `Resumen!D2` (FILTRAR/ORDENAR/ELEGIRCOLS: el reporte de cobranza) y `Resumen!A8` (ORDENAR/UNICOS: la lista de clientes) **desborden** en varias filas y no salgan con `@` ni muestren un solo valor. Si fallan, vuelve a escribir esas dos fórmulas a mano en el archivo y guárdalo;
  - que los nombres de las funciones en español sean los que muestra el video (ELEGIRCOLS, TEXTODESPUES, TEXTOANTES, UNICOS, FIN.MES);
  - que **TEXTODESPUES** (fórmula 3) devuelva «Diego Paz»;
  - que las cifras coincidan con el video: 8 vencidas y 2.446.165 con la fórmula escrita a mano; 4 y 1.835.590 con la corregida; diferencia 610.575.
- [ ] **Subir la plantilla** a Google Drive (enlace «cualquier persona con el enlace puede ver») o a Gumroad (precio 0, sin pedir email: el video y la descripción dicen «sin registro»). Pega el enlace en `metadatos.json` en lugar de `[ENLACE A LA PLANTILLA]`.
- [ ] *(Opcional)* Correr los prompts de `respuestas-ia.md` en claude.ai gratis, sobre todo el 7b (el giro). Si la respuesta señala «Pagado», se puede volver a poner el plan en el rótulo del chat. Si no lo señala, el giro vuelve a debate. Hoy la descripción dice solo «generadas con Claude el 25/10/2026», que es lo verificado.
- [ ] *(Opcional)* Medir la demanda: `python3 herramientas/investigar.py nicho "fórmulas de excel con ia" "fórmulas de excel con chatgpt" --region MX` (y `--region ES`). Umbral: en el top 10, al menos 2 videos de los últimos 12 meses con 30 mil vistas o más, o 1 outlier de 3x. Si «con chatgpt» duplica la mediana, conviene correr los prompts en ChatGPT y pasar a la variante «10 fórmulas de Excel con ChatGPT: tu planilla se llena sola». En esta sesión el autocompletado de YouTube no respondió (el proxy dio 403), así que las etiquetas salen de la idea y del debate, no de `investigar.py sugerencias`.

## 2. Subida y metadatos

- [ ] Sube `produccion/video02/video02.mp4` (el render con voz, **no** el `-preview`) desde YouTube Studio como **Privado**.
- [ ] Corre `python3 herramientas/completar_video.py video02`, que carga título, descripción con capítulos, etiquetas, categoría, idioma, miniatura, subtítulos `video02.srt` y playlists. Si no toma el último video subido, pásale el ID: `python3 herramientas/completar_video.py video02 <ID>`.
- [ ] Revisa en Studio:
  - **Categoría 27, Educación.** Es un tutorial de funciones de Excel, la audiencia busca «cómo hacer X en Excel» y es la categoría donde están los tutoriales de Excel de la competencia. El video 1, que era sobre herramientas de IA, usó la 28. La categoría casi no pesa en el ranking: si prefieres que todo el canal use la misma, la 28 también es válida.
  - Idioma español. «Contenido alterado o sintético»: **no** hace falta marcarlo, porque la voz no imita a una persona real ni muestra hechos realistas falsos. Igual se declara en la descripción.
  - Capítulos: aparecen solos con la descripción (10 capítulos, el primero en 0:00).
  - Playlists: «Flujos paso a paso con IA» y «Empieza aquí: lo mejor de Atajos IA». Es el primer video del nicho Excel + IA, así que conviene que sea la puerta de entrada.
  - Pantalla final (últimos 20 s): botón **Suscribirse** en el círculo de la derecha y, en el recuadro de la izquierda, **"Lo mejor para el espectador"** (es el primer video del canal: todavía no hay otro al que mandar). El cierre de la voz invita a suscribirse.
  - **Comentario fijado:** «¿Qué fórmula te gustaría pedirle a la IA? La plantilla gratis, sin registro: [enlace]».

## 3. Prueba A/B y horario

- [ ] En Studio, **Probar y comparar**, carga los 3 títulos con sus 3 miniaturas (cada par es una variante):

| Variante | Título | Miniatura | Ángulo |
|---|---|---|---|
| A (principal) | 10 fórmulas de Excel con IA: tu planilla se llena sola | `miniatura-a.png` («SE LLENA SOLA» + gráfico de ventas) | resultado terminado (firma del canal) |
| B | Fórmulas de Excel con IA: el paso que casi nadie pide | `miniatura-b.png` («PARECE BIEN» + 2.446.165 agrietado) | el método, el error silencioso |
| C | Fórmulas de Excel con IA (y el error que cobra dos veces) | `miniatura-c.png` («610.575 DE MÁS» + Vencido/PAGADO) | el giro y la cobranza (para Martín) |

  **Por qué la A es la principal:** es el mismo cuadro que abre el video (la hoja Resumen con el gráfico de barras), así que lo que promete se ve en los primeros segundos. Cumple la firma del canal (el resultado terminado como protagonista) y tiene un solo elemento, que se lee a 168 px. Las cifras del gráfico (666.000, 264.600, 58.900) son las de octubre en el video. Las otras dos dependen de entender un error antes de hacer clic, y para eso está la prueba. (La miniatura C ya muestra «610.575» con punto, igual que el video.)
- [ ] **Horario recomendado: viernes 30/10/2026, 13:00 h de Ciudad de México** (16:00 Buenos Aires y Santiago, 15:00 Bogotá y Lima, 20:00 Madrid). Es el horario fijo del plan (`youtube/03-sistema-operativo.md` §5) y cae en un día de cadencia (martes o viernes). Todavía no hay datos de «Cuándo están conectados tus espectadores»: en esta sesión la API no tenía credenciales, y el canal tiene muy poco historial. Hay que ajustarlo desde el mes 2. Si los pendientes de la sección 1 no están listos el jueves 29/10, pásalo al **martes 03/11/2026 a las 13:00 h** de CDMX: no lo publiques sin la comprobación en Excel para la web.
- [ ] Programa la publicación en esa fecha (Visibilidad → Programar).

## 4. Shorts (1, 3 y 5 días después)

Los tiempos son **estimados** (motor sin voz, `build/datos.js`, antes del pulido final: pueden correrse unos segundos). Después de renderizar con voz, busca en `video02.srt` la frase con la que empieza y termina cada tramo y corrige `desde` y `hasta`. Cada tramo tiene que durar 55 s o menos. El `--titulo` de `shorts.py` se quema en el video sin salto de línea, así que va corto (unos 20 caracteres a 74 px). El título completo se escribe al subir el Short. Se recortan del **video final con voz** (`produccion/video02/video02.mp4`, que es el que lee `shorts.py`). En cada Short, en «Video relacionado», enlaza el video largo.

### Short 1 · el giro de la fórmula 7 · publicar el día +1 (sábado 31/10, 13:00 h CDMX)
- **desde** 4:49.2 · **hasta** 5:41.0 (≈ 52 s)
- **Título:** «Esta fórmula le cobraba dos veces a un cliente»
- **Tramo:** de «La copio: ocho facturas vencidas, dos millones cuatrocientos cuarenta y seis mil por cobrar» a «610.575 de más en la lista de cobranza».
- **Por qué se entiende solo:** presenta la fórmula, muestra que «no da error», aplica la prueba y revela el cobro doble con la cifra.
- **Última frase que manda al video largo:** «610.575 de más en la lista de cobranza.» La corrección queda abierta a propósito. Agrega como texto final o en la descripción del Short: «La fórmula corregida y las otras 9, en el video completo.»
- `python3 herramientas/shorts.py video02 4:49.2 5:41.0 --titulo "Le cobraba dos veces" --salida short1-giro`

### Short 2 · FILTRAR arma la cobranza · publicar el día +3 (lunes 02/11, 13:00 h CDMX)
- **desde** 6:20.1 · **hasta** 7:10.6 (≈ 50 s)
- **Título:** «El reporte de cobranza en una sola celda»
- **Tramo:** de «Fórmula ocho: el reporte de cobranza de la semana» a «la lista se rehace sola».
- **Por qué se entiende solo:** el prompt, la prueba que encuentra el caso sin vencidas, la fórmula explicada de adentro hacia afuera y el resultado (1.835.590, a quién llamar).
- **Última frase que manda al video largo:** «Y si alguien paga, cambias su Pagado a sí, y sale de la lista. Lo mismo con la fecha de corte: la lista se rehace sola.» Agrega en la descripción: «Las 10 fórmulas y la plantilla gratis, en el video completo.»
- `python3 herramientas/shorts.py video02 6:20.1 7:10.6 --titulo "Cobranza en 1 celda" --salida short2-filtrar`

### Short 3 · FIN.MES, antes y después · publicar el día +5 (miércoles 04/11, 13:00 h CDMX)
- **desde** 3:00.1 · **hasta** 3:39.2 (≈ 39 s)
- **Título:** «No sumes 30 días: usa FIN.MES»
- **Tramo:** de «Fórmula cinco: vence a fin del mes siguiente. ¿Y si sumas treinta días?» a «Después viene la fórmula que casi le cobra dos veces a un cliente.»
- **Por qué se entiende solo:** el error (+30 días da el 3 de septiembre), la solución (FIN.MES da el 30), qué significan el 1 y el 0, y el formato de fecha.
- **Última frase que manda al video largo:** «Después viene la fórmula que casi le cobra dos veces a un cliente.» Es un bucle abierto natural hacia el video largo. Corta antes de «Si te está sirviendo, suscríbete».
- `python3 herramientas/shorts.py video02 3:00.1 3:39.2 --titulo "No sumes 30 días" --salida short3-finmes`

Los Shorts quedan en `produccion/video02/shorts/`. Súbelos desde la app o desde Studio con la descripción «Video completo: 10 fórmulas de Excel con IA (enlace en Video relacionado) #Excel #IA #Shorts».

## 5. Después de publicar

- [ ] A las 48 h, revisa el CTR de cada variante en «Probar y comparar». YouTube elige la ganadora sola. Anota el resultado para el `analista`, en `canales/atajos-ia/aprendizajes.md`, a los 7 y a los 28 días.
- [ ] Si gana la A y el CTR queda bajo, la segunda prueba es la miniatura alternativa «SIN #N/A» con el título 1 (ver `idea.md`).
