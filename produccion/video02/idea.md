# 10 fórmulas de Excel con IA: tu planilla se llena sola (versión ronda 3)

- **Pilar:** P1 · Excel + IA · **Formato:** estructura **A (tutorial con cronómetro)** de `youtube/04` adaptada a lista: los "pasos 1–3" son las fórmulas 1–6, el "paso secreto" es la fórmula 7 (al 70 %), y las fórmulas 8–10 son el resultado final que se arma en cascada. (`04` define las estructuras A, B y C; no hay D.) · **Duración objetivo:** 10,5 min (rango 9–12; un corte de anuncios a mitad, en el minuto 5:10, entre la fórmula 5 y la 6)
- **Palabra clave principal:** `fórmulas de excel con ia`
- **Búsquedas relacionadas (no salen de `investigar.py sugerencias`):** en esta sesión no hay credenciales de la API ni acceso de red a YouTube o Google, y el autocompletado ya había devuelto 403 el 25/10/2026. Candidatas **sin verificar**: `fórmulas de excel con chatgpt`, `chatgpt para excel`, `fórmulas de excel más usadas`, `buscarx`, `sumar.si.conjunto`, `función filtrar excel`, `fórmulas de excel para oficina`. **Pendiente:** correr `python3 herramientas/investigar.py nicho "fórmulas de excel con ia" --region MX` (y ES) antes del guion.
- **Evidencia de demanda (cualitativa, no medida). Es una condición pendiente del creador, no del ideador (decisión del showrunner, ronda 1):**
  - No hay oportunidad numerada: no se pudo generar un lote con la API (no hay credenciales en la sesión). El documento vigente (`sistema/investigacion/2026-10-iatube-y-nichos.md`) dice que "IA + Excel" es el tema que más sube el RPM del canal y que la búsqueda que crece es "cómo hacer X con IA en mi trabajo".
  - Señal de interés en texto (búsqueda web del 25/10/2026, registrada en `canales/atajos-ia/ideas.md`, idea 1): hay guías en español en medios grandes ([Xataka](https://www.xataka.com/basics/chatgpt-para-formulas-excel-como-usar-inteligencia-artificial-para-crearlas), [Digital Trends](https://es.digitaltrends.com/computadoras/chatgpt-para-escribir-formulas-de-excel/), [WWWhatsNew, 2024](https://wwwhatsnew.com/2024/01/22/manejo-de-formulas-de-excel-con-chatgpt-una-guia-practica/)). Son de 2023–2024 y están desactualizadas: no mencionan BUSCARX, FILTRAR ni TEXTODESPUES, ni que el `=COPILOT()` se retiró. Esto indica que el tema interesa, no cuánto se busca en YouTube.
  - Competidor de referencia: *Microsoft Excel a Todo Nivel* (~325 mil suscriptores, 2.173 videos). Enseña fórmulas, pero no con IA. **Outlier:** sin medir.
  - **Procedimiento pendiente (creador, como tarde antes de cerrar el guion):** correr `python3 herramientas/investigar.py nicho "fórmulas de excel con ia" --region MX` (y ES), o anotar a mano el top 5 de YouTube para `fórmulas de excel con ia` y `fórmulas de excel con chatgpt` (título, canal, vistas, antigüedad), y agregarlo aquí. **Umbral (propuesto por el investigador, ronda 2):** la idea pasa si en el top 10 de YouTube para `fórmulas de excel con ia` hay **al menos 2 videos de los últimos 12 meses con 30 mil vistas o más**, o **al menos 1 outlier de 3x** (vistas / suscriptores del canal). Si la mediana de vistas del top 10 de `fórmulas de excel con chatgpt` es **el doble o más** que la de "con ia", el creador corre los 10 prompts en ChatGPT gratis y entra el título A/B con "con ChatGPT". Si ninguna de las dos pasa el umbral, se reabre la idea.
  - Señales de interés de 2026 que mencionó el investigador (Cámara de Sevilla 07/2026, NYSSCPA 14/07/2026, Genbeta, ClickUp, Platzi, DataCamp, Ámbito): **no las incorporo sin enlace**. Regla 3: cada dato real lleva fuente. Entran cuando el investigador pase las URL.
- **Por qué ahora:** 1) Desde el 15/04/2026, Copilot gratis ya no está dentro de Excel para cuentas sin licencia, y el `=COPILOT()` se retiró el 14/09/2026. Mucha gente busca "la IA de Excel" y no la encuentra: la alternativa gratis es pedirle la fórmula a un chat. 2) La narrativa del momento es "IA aplicada > noticias de IA". 3) Es el lead magnet base del canal ("10 fórmulas resueltas"), así que conviene publicarlo temprano para empezar a juntar emails.
- **Ángulo propio (frente a las guías en texto revisadas; YouTube se verifica con la condición de demanda):**
  1. **Una sola planilla real de pyme que se completa de punta a punta** (pedidos → precios → vencimientos → cobranza → resumen del lunes), en vez de 10 ejemplos sueltos con datos de juguete. Cada fórmula usa el resultado de la anterior.
  2. **Un método con nombre, "Mapa · Meta · Prueba"**, en vez de "pídele a ChatGPT que te haga una fórmula". La tercera parte se guarda como bucle abierto.
  3. **Excel en español con `;` y Excel para la web gratis.** Las guías existentes muestran fórmulas en inglés con comas, que en un Excel en español dan error. El "Mapa" del prompt lo resuelve, y el video dice que en México Excel suele usar `,`.
  4. **Veredicto honesto en pantalla:** la fórmula escrita a mano que "funciona" pero miente (fórmula 7) y cómo la Prueba la desenmascara; NOMPROPIO convirtiendo "SRL" en "Srl"; y cuándo conviene escribirla a mano (si la fórmula es más corta que el prompt), siempre pasándola por la Prueba.
  6. **El caso de cobranza (cuentas por cobrar) de una pyme**, que tiene RPM alto (ficha): va en un capítulo ("Cobranza en Excel: el reporte del lunes") y en los metadatos (`cuentas por cobrar`, `cobranza en excel`, `plantilla excel pyme`), sin alargar el video.
  5. Fórmulas modernas que la audiencia no conoce y que la IA sí conoce: TEXTODESPUES, FIN.MES, FILTRAR con ELEGIRCOLS. Ahí la IA ahorra más tiempo, porque no sabes ni qué buscar en Google.
- **Línea 1 de la descripción:** "Tu planilla de Excel se completa sola, sin macros, con 10 fórmulas que le pides a una IA gratis (y una prueba para que no te engañen)." Aclara que "se llena sola" no es una macro.
- **Promesa en una frase:** "Al final de este video vas a poder pedirle a una IA gratis las fórmulas de Excel que usas en la oficina, en español, en menos de un minuto y de forma que puedas comprobarla antes de confiar en ella, y vas a tener las 10 que más se usan en una oficina funcionando en tu planilla."

## Restricción "Claude en la demo": qué cambia y alternativa honesta

- Las demos usan **Claude (plan gratuito de claude.ai)**, con respuestas reales. El primer chat de la demo muestra el rótulo "Claude · versión gratuita". En los primeros 30 s, la voz dice: "Uso Claude gratis; el mismo prompt funciona en ChatGPT gratis o en Copilot gratis" (regla 7).
- **Sí, debilita algo la idea.** `fórmulas de excel con chatgpt` es la búsqueda más intuitiva para Laura, que ya usa ChatGPT (ficha). Pero `fórmulas de excel con ia` la incluye por semántica, es más duradera (no envejece si ChatGPT cambia) y coincide con el posicionamiento "IA para Excel" del canal. "ChatGPT" va en la descripción, las etiquetas y un capítulo ("¿Y con ChatGPT o Copilot?"), nunca en el título.
- **Alternativa honesta más fuerte (la propongo, la decide el creador):** el creador pega los 10 prompts en **ChatGPT gratis** (unos 15 minutos), guarda las respuestas textuales con fecha y captura, y la demo usa esas respuestas. Así, la regla 4 se cumple y el título puede llevar "con ChatGPT". Si se hace, entra un título A/B "10 fórmulas de Excel con ChatGPT: tu planilla se llena sola" (59), se cambia el rótulo del chat y se puede mostrar una vez el mismo prompt en ChatGPT al lado del de Claude. Nunca se muestra un chat de ChatGPT que no se haya corrido.
- **Aviso de los primeros 30 s (junto con "gratis"):** "las fórmulas 3, 8 y 9 necesitan Excel para la web o Microsoft 365; no están en Excel 2016 ni 2019".

## La planilla: "Distribuidora Sur" (ficticia, declarada)

Distribuidora mayorista ficticia de artículos de limpieza y librería. Exporta los pedidos de su sistema "sucios": nombres con espacios y mayúsculas mezcladas, y vendedor y código pegados. Sin símbolo de moneda, para que sirva en todos los países. **Fecha de corte fija: 04/11/2026**, en la celda `Resumen!B1` (no se usa HOY() en la demo, para que los resultados se puedan reproducir; la plantilla trae `=HOY()` con una nota).

**Hoja `Productos`** (A Código · B Producto · C Precio): LIM-010 Cloro 5 L 2.400 · LIM-020 Detergente 5 L 3.100 · LIM-030 Desinfectante 1 L 1.150 · LIM-040 Papel higiénico x48 9.800 · PAP-200 Resma A4 4.500 · PAP-210 Cuadernos x10 6.200 · PAP-220 Bolígrafos x50 3.900

**Hoja `Pedidos`:** las columnas blancas vienen del sistema y las de **F#** las completa la fórmula de ese número.

| A Fecha | B Cliente (sistema) | C Cliente **F2** | D Vendedor (sistema) | E Vendedor **F3** | F Código | G Cant. | H Precio **F1** | I Desc. **F4** | J Neto* | K Vence **F5** | L Pagado | M Estado **F7** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 04/08/2026 | `  ferretería el TORNILLO ` | Ferretería El Tornillo | V01 \| Diego Paz | Diego Paz | LIM-010 | 40 | 2.400 | 5 % | 91.200 | 30/09/2026 | Sí | Cobrado |
| 12/08/2026 | `LIBRERÍA SAN MARTÍN SRL` | Librería San Martín Srl | V02 \| Carla Ruiz | Carla Ruiz | PAP-200 | 120 | 4.500 | 10 % | 486.000 | 30/09/2026 | No | Vencido |
| 21/08/2026 | `kiosco la esquina` | Kiosco La Esquina | V03 \| Tomás Gil | Tomás Gil | LIM-020 | 15 | 3.100 | 5 % | 44.175 | 30/09/2026 | Sí | Cobrado |
| 02/09/2026 | `ferretería el tornillo  ` | Ferretería El Tornillo | V01 \| Diego Paz | Diego Paz | PAP-210 | 60 | 6.200 | 10 % | 334.800 | 31/10/2026 | Sí | Cobrado |
| 09/09/2026 | `  Colegio Nuevo Horizonte` | Colegio Nuevo Horizonte | V02 \| Carla Ruiz | Carla Ruiz | PAP-200 | 300 | 4.500 | 10 % | 1.215.000 | 31/10/2026 | No | Vencido |
| 15/09/2026 | `KIOSCO LA ESQUINA` | Kiosco La Esquina | V03 \| Tomás Gil | Tomás Gil | LIM-030 | 25 | 1.150 | 0 % | 28.750 | 31/10/2026 | No | Vencido |
| 23/09/2026 | `librería san martín srl ` | Librería San Martín Srl | V01 \| Diego Paz | Diego Paz | PAP-220 | 40 | 3.900 | 10 % | 140.400 | 31/10/2026 | Sí | Cobrado |
| 30/09/2026 | `Hotel  Mirador` | Hotel Mirador | V01 \| Diego Paz | Diego Paz | LIM-040 | 12 | 9.800 | 10 % | 105.840 | 31/10/2026 | No | Vencido |
| 06/10/2026 | `colegio nuevo horizonte` | Colegio Nuevo Horizonte | V02 \| Carla Ruiz | Carla Ruiz | PAP-220 | 150 | 3.900 | 10 % | 526.500 | 30/11/2026 | No | Al día |
| 14/10/2026 | `hotel mirador ` | Hotel Mirador | V03 \| Tomás Gil | Tomás Gil | LIM-040 | 30 | 9.800 | 10 % | 264.600 | 30/11/2026 | No | Al día |
| 22/10/2026 | `Kiosco La Esquina` | Kiosco La Esquina | V01 \| Diego Paz | Diego Paz | PAP-201 → PAP-210 | 10 | "Código no existe" → 6.200 | 5 % | 58.900 | 30/11/2026 | No | Al día |
| 28/10/2026 | `Ferretería El Tornillo` | Ferretería El Tornillo | V02 \| Carla Ruiz | Carla Ruiz | LIM-020 | 50 | 3.100 | 10 % | 139.500 | 30/11/2026 | Sí | Cobrado |

\* J Neto = `=G2*H2*(1-I2)` es una multiplicación simple: no cuenta como una de las 10.

Notas para el guion:
- **Errores sembrados a propósito:** 1) los nombres sucios (sin limpiar, UNICOS devolvería 10 "clientes" en vez de 5: no distingue mayúsculas, pero sí espacios); 2) el código mal tipeado PAP-201 (BUSCARX avisa, se corrige en pantalla y la cascada se recalcula); 3) "Hotel  Mirador" con doble espacio interno (ESPACIOS lo arregla).
- **Columnas visibles:** el motor muestra unas 7 columnas. Cada escena `excel` muestra un subconjunto (por ejemplo, F-G-H para la fórmula 1). Las columnas B y D "del sistema" se ocultan después de las fórmulas 2 y 3, como haría alguien en Excel.

**Hoja `Resumen`:** B1 = fecha de corte · bloque "Ventas por vendedor y mes" (F6) · bloque "Cobranza del lunes" (F8) · bloque "Clientes" (F9 + F10) · gráfico de barras de ventas por vendedor (acción `grafico` del motor).

## Las 10 fórmulas, en orden de retención

Las fórmulas se escriben en Excel en español, con `;` como separador, y todas existen en Excel para la web. Los minutos son aproximados para 10,5 min.

| # | Min. | Fórmula (celda) | Caso real de oficina (1 línea) | Por qué la IA ahorra tiempo ahí |
|---|---|---|---|---|
| 1 | 1:20 | **BUSCARX** (H2): `=BUSCARX(F2;Productos!A:A;Productos!C:C;"Código no existe")` | Traer el precio de cada pedido desde el catálogo sin copiarlo a mano. | Nadie recuerda el orden de los argumentos ni que tiene un "si no lo encuentra" incorporado; la IA lo pone y te evita el #N/A. **Arranque fuerte:** es la búsqueda más conocida de Excel, y la fila con PAP-201 da el primer minigiro ("no es un error, es un aviso"). Una frase para Laura, que usa BUSCARV: "es la versión nueva de BUSCARV, la que no se rompe si agregas columnas". 5 s para mostrar cómo saber si tu Excel usa `;` o `,` (mirar una fórmula que ya tengas o la ayuda de la función). **Choque con el video 3:** BUSCARX se queda aquí, pero no aparece en la miniatura, y el video 3 queda obligado a otro caso y otro error (coincidencia aproximada, números guardados como texto, espacios), no el "código no existe". |
| 2 | 2:10 | **NOMPROPIO + ESPACIOS** (C2): `=NOMPROPIO(ESPACIOS(B2))` | Limpiar los nombres de clientes que el sistema exporta con espacios y mayúsculas mezcladas. | Hay que saber que existen dos funciones y anidarlas; la IA lo resuelve con "quiero el nombre prolijo". Veredicto honesto: "SRL" queda "Srl" y las tildes que faltan no se agregan. |
| 3 | 2:55 | **TEXTODESPUES** (E2): `=TEXTODESPUES(D2;"| ")` (+ TEXTOANTES para el código V01) | Separar el código del nombre del vendedor que vienen pegados en una celda. | Es una función de 2022 que la audiencia no conoce; sin IA terminaría usando EXTRAE+HALLAR o Texto en columnas a mano. |
| — | 3:30 | CTA de suscripción con motivo + reenganche del giro: "en un rato vas a ver la fórmula que le cobra dos veces a un cliente, y cómo la atrapé" + mención de la hoja `Prompts` con la columna "Qué revisar" | | |
| 4 | 3:40 | **SI.CONJUNTO** (I2): `=SI.CONJUNTO(G2*H2>=100000;10%;G2*H2>=40000;5%;VERDADERO;0)` | Aplicar el descuento por tramos de compra que tiene la política comercial. | Traduce "más de 100.000, 10 %; más de 40.000, 5 %; si no, nada" a una fórmula sin SI anidados ni paréntesis de más. Recuerda el orden de los tramos (de mayor a menor) y el `VERDADERO` final. |
| 5 | 4:30 | **FIN.MES** (K2): `=FIN.MES(A2;1)` | Calcular el vencimiento cuando la condición es "pago a fin del mes siguiente". | Casi nadie sabe que FIN.MES existe; la gente suma 30 días y se equivoca con los meses de 31. La IA da la función exacta a partir de la condición comercial escrita en palabras. |
| — | 5:10 | **Corte de anuncios** + reenganche: "lo que viene es lo que más me sirvió: una fórmula que escribí yo, que parecía perfecta y le cobraba dos veces a un cliente, y la parte del método que la atrapó" | | |
| 6 | 5:20 | **SUMAR.SI.CONJUNTO** (Resumen): `=SUMAR.SI.CONJUNTO(Pedidos!J:J;Pedidos!E:E;$A3;Pedidos!A:A;">="&B$2;Pedidos!A:A;"<="&FIN.MES(B$2;0))` | Total vendido por vendedor y por mes para la reunión de ventas. | El criterio de fechas con `">="&` es el punto donde todos se traban, igual que los `$`. La IA arma la fórmula para copiar en toda la tabla. Resultado: Carla Ruiz, septiembre: 1.215.000. |
| **7** | **6:20–7:40 (≈ 70 %)** | **SI (estado de cobro), EL GIRO.** Capítulo: "La IA como revisora de tus fórmulas" (M2). Primero, la versión escrita a mano `=SI(K2<Resumen!$B$1;"Vencido";"Al día")`, rotulada "escrita a mano"; después, la corregida `=SI(L2="Sí";"Cobrado";SI(K2<Resumen!$B$1;"Vencido";"Al día"))` | Marcar qué facturas están vencidas para saber a quién llamar. | Ver la sección del giro. La IA ahorra tiempo incluso con las fórmulas que escribes tú: la parte 3 del método (Prueba) encuentra el error que no da error. |
| 8 | 7:40 | **FILTRAR** (+ ORDENAR y ELEGIRCOLS) (Resumen): `=ORDENAR(FILTRAR(ELEGIRCOLS(Pedidos!A2:M13;3;11;10);Pedidos!M2:M13="Vencido";"Sin vencidos");2;1)` | El "reporte de cobranza del lunes": cliente, vencimiento y monto de lo vencido, ordenado, que se actualiza solo. | Es el premio después del giro: un informe que antes se armaba con filtros y copiar-pegar, en una celda. Combinar tres funciones de matriz dinámica es justo lo que nadie escribe de memoria. Resultado: 4 facturas, 1.835.590. |
| 9 | 8:25 | **UNICOS + ORDENAR** (Resumen): `=ORDENAR(UNICOS(Pedidos!C2:C13))` | La lista de clientes sin repetidos, para el resumen. | Reemplaza "Quitar duplicados" a mano, y la lista se actualiza sola. Paga el esfuerzo de la fórmula 2: con los nombres sucios, salían 10 "clientes" en vez de 5 (UNICOS no distingue mayúsculas, pero sí espacios: verificarlo en Excel). |
| 10 | 8:55 | **CONTAR.SI.CONJUNTO** (Resumen): `=CONTAR.SI.CONJUNTO(Pedidos!C:C;A12;Pedidos!M:M;"Vencido")` | Cuántas facturas vencidas tiene cada cliente, junto a la lista. | La IA arma los pares rango-criterio. Cierra el tablero: la hoja `Resumen` queda completa y se construye el gráfico. |
| — | 9:25 | Resultado final + cronómetro "a mano vs. con IA" (`antes_despues`) · 9:50 límites (cuándo escribirla a mano) · 10:10 CTA plantilla + pantalla final de 20 s | | |

**Por qué este orden:** abre con la fórmula más buscada (BUSCARX) y un minigiro; 2–3 dan victorias rápidas y muy visuales (la cascada de nombres limpios); 4–5 enseñan algo que nadie sabía (FIN.MES) justo antes del anuncio; el giro cae al 70 %; 8 es el premio emocional (el informe del lunes en una celda) y 9–10 cierran el tablero que se prometió en el hook. Ninguna escena de fórmula dura más de 75 s, y cada 60–90 s hay un `capitulo`, `aviso` o `antes_despues` (regla 5 del motor).

## El método "Mapa · Meta · Prueba" (hilo y bucle abierto)

El prompt de 3 partes, que aparece en un panel `chat` y en la plantilla:
1. **Mapa (dónde están los datos):** "Excel para la web en español, separador punto y coma. Hoja Pedidos: A Fecha, F Código, G Cantidad… Los datos van de la fila 2 a la 13. El catálogo está en la hoja Productos, columnas A (código) y C (precio)."
2. **Meta (qué quiero, con la regla en palabras):** "En H2 quiero el precio de cada código; si el código no existe, que diga 'Código no existe'. Dame una sola fórmula para copiar hacia abajo."
3. **Prueba (la que nadie usa):** "Antes de darme la fórmula, dime qué casos pueden hacer que dé un resultado equivocado sin mostrar error, y dime qué debería dar en dos filas concretas para que yo lo compruebe."

**Cómo funciona el bucle:** en el hook se anuncia que el método tiene 3 partes. De la fórmula 1 a la 6 se usan solo Mapa y Meta, y funcionan, así que el espectador cree que ya tiene el método. En la fórmula 7 se revela la Prueba y se ve por qué importa. A partir de la 8, los prompts se muestran completos con las 3 partes.

## Hook (2 frases, tipo "Resultado primero" + "Cronómetro")

> "Esta planilla de pedidos se completa sola: precios, vencimientos, cobranza y el resumen del lunes, con 10 fórmulas, casi todas se las pedí a una IA gratis y la que escribí yo la revisó ella, en [N] minutos, cuando a mano me llevaba unas 4 horas. Uso un prompt de 3 partes; casi todos usan solo las dos primeras, y la tercera es la que encontró la fórmula que le habría cobrado dos veces a un cliente."

En pantalla: **en el primer cuadro, un destello de 1 s del sello "PAGADO" cayendo sobre una celda "Vencido"**, y después la hoja `Resumen` terminada con el gráfico y el cronómetro (`antes_despues`). En la segunda frase vuelve 2 s la celda "Vencido" con el sello (adelanto del giro para quien entra por el A/B 3 o la miniatura C). [N] **se mide de verdad** al armar la plantilla. Las "4 horas" a mano también se miden: el creador arma a mano 2 de las fórmulas y la cobranza y extrapola, y en pantalla dice "estimado". Si da menos, la cifra cambia en el hook y en la miniatura A; si da más de 15 minutos, la frase cambia y el hook empieza por el error de cobranza ("Esta fórmula le iba a cobrar dos veces a un cliente…").

## El "paso secreto" o giro que sostiene el bucle abierto (fórmula 7, ≈ 70 %). Plan B como base

**Por qué el plan B es la base (prueba real del showrunner, ronda 1):** con Mapa + Meta, Claude da primero la versión que ignora "Pagado", pero enseguida avisa que existe la columna L y ofrece la versión corregida. No se puede decir "la IA me dio una fórmula que mentía". El giro no depende de esa casualidad: la fórmula que falla es **una que escribo a mano**, y la IA es la que la atrapa.

Prompt real de la prueba (Mapa + Meta, sin Prueba), textual:

> Excel para la web en español, separador punto y coma. Hoja Pedidos: A Fecha, C Cliente, E Vendedor, F Código, G Cantidad, H Precio, I Descuento, J Neto, K Vence, L Pagado (Sí/No), M Estado. Los datos van de la fila 2 a la 13. La fecha de corte está en la hoja Resumen, celda B1.
> En M2 quiero el estado de cada factura: si ya venció, que diga "Vencido"; si no, "Al día". Dame una sola fórmula para copiar hacia abajo.

Respuesta (Claude en la sesión del showrunner, no en claude.ai gratis; el guionista corre y guarda la de claude.ai): `=SI(K2<Resumen!$B$1;"Vencido";"Al día")` y a continuación: "tienes la columna L (Pagado). Si una factura ya se pagó, seguramente no quieres que aparezca como 'Vencido'…" con `=SI(L2="Sí";"Pagado";SI(K2<Resumen!$B$1;"Vencido";"Al día"))`.

Secuencia en el video:
1. **"Esta es corta, la escribo yo."** Conecta con el veredicto del canal (si la fórmula es más corta que el prompt, escríbela a mano). En pantalla se escribe `=SI(K2<Resumen!$B$1;"Vencido";"Al día")` con un rótulo fijo, **"escrita a mano, como la escribe casi todo el mundo"**. No da error y la columna se pinta en cascada.
2. Adelanto de la cobranza: **8 facturas vencidas, 2.446.165 por cobrar**. Pausa.
3. **Se revela la parte 3, Prueba:** se pega esa fórmula en el chat con el Mapa y la consigna "¿Qué casos pueden hacer que esta fórmula dé un resultado equivocado sin mostrar error? Dime qué debería dar en las filas 2 y 6." La respuesta real señala que **ignora la columna "Pagado"** (y, si lo dice, también las fechas vacías). El guionista corre este prompt en claude.ai gratis y usa la respuesta textual. Si no señala "Pagado", el giro no se inventa y vuelve a debate.
4. `aviso` rojo: la Ferretería El Tornillo aparece con 2 facturas vencidas **que ya pagó**, y lo mismo pasa con Kiosco La Esquina y Librería San Martín. El lunes habrías llamado a 3 clientes para cobrarles 4 facturas ya pagadas (610.575 de más). La fórmula corregida da **4 facturas y 1.835.590**.
5. **Hallazgo honesto (10 s), capítulo "La IA como revisora de tus fórmulas":** "A veces la IA te avisa sola: cuando le pedí esta misma fórmula con el Mapa completo, ya me habló de la columna Pagado. Pero a veces no. La Prueba hace que te lo diga sí o sí." Por eso el Mapa nombra todas las columnas, y por eso, aunque la escribas tú, la pasas por la Prueba.
6. Lección del canal: "Una fórmula que da error es fácil de arreglar. La peligrosa es la que da un resultado creíble y equivocado."

**Cómo cambia el bucle:** de la fórmula 1 a la 6 se usan Mapa y Meta. En la 7 se revela la Prueba aplicada a una fórmula escrita a mano. De la 8 en adelante, los prompts se muestran con las 3 partes. La promesa ("fórmulas que puedes comprobar antes de confiar en ellas") sale exactamente de este momento.

## Plantilla gratis que deja el video

**"Distribuidora Sur · 10 fórmulas con IA.xlsx"** (gratis a cambio del email; es el lead magnet base del canal, como dice `ideas.md`):
- `Pedidos`, `Productos` y `Resumen`: la misma planilla que se ve en pantalla, con las 10 fórmulas funcionando y datos ficticios declarados en una celda de portada.
- `Prompts`: las 10 consignas completas con Mapa · Meta · Prueba, la fórmula que salió y una columna "Qué revisar" (se menciona en el CTA de 3:30 y en el cierre).
- `Práctica`: la misma planilla, sin fórmulas, para completar uno mismo, con la solución en comentarios.
- `Resumen!B1` = `=HOY()` (con una nota: "pon una fecha fija para reproducir el video: 04/11/2026").
- Regla 8: sin macros ni vínculos externos, probada en Excel para la web en español. Lleva una nota "si tu Excel usa coma como separador (habitual en México), las fórmulas se convierten solas al abrir el archivo; solo cambia el separador cuando copies desde el chat".
- Versión de pago, más adelante: no para este video. Sí puede ser el puente al pack de plantillas en la pantalla final.

## Títulos (todos con 60 caracteres o menos; palabra clave en las primeras 4 palabras)

1. **10 fórmulas de Excel con IA: tu planilla se llena sola** (54) ← **principal, A/B 1**
2. **Fórmulas de Excel con IA: el paso que casi nadie pide** (53) ← **A/B 2** (método)
3. **Fórmulas de Excel con IA (y el error que cobra dos veces)** (57) ← **A/B 3** (giro y cobranza)
4. Fórmulas de Excel con IA: 10 que te ahorran horas (49) (era el principal en la ronda 1; queda de reserva por genérico)
5. Fórmulas de Excel con IA gratis: 10 para la oficina (51)
6. Fórmulas de Excel con IA: el prompt de 3 partes (47)
7. Fórmulas de Excel con IA: deja de buscarlas en Google (53)
8. Fórmulas de Excel con IA: una planilla, 10 atajos (49)
9. Fórmulas de Excel con IA: 10 que todo administrativo usa (56)
10. Fórmulas de Excel con IA sin memorizar nada: 10 casos (53)

Reserva condicionada: cuando [N] esté medido y sea ≤ 15 min, el principal pasa a "Fórmulas de Excel con IA: tu planilla lista en [N] min" (≤ 55), que confirma que no es una macro. Si el creador corre los prompts en ChatGPT: "10 fórmulas de Excel con ChatGPT: tu planilla se llena sola" (59).

**Por qué el principal:** dice lo distintivo (una planilla que se completa, no una lista suelta), coincide con el hook y con la miniatura A, y cumple la firma del canal. "Gratis" (regla 7) va en la voz de los primeros 30 s, no en el título. Se descartaron "pídelas así y no fallan" (contradice el veredicto honesto) y "la que casi me engaña" (con el plan B, quien miente es la fórmula escrita a mano, no la IA).

## 3 conceptos de miniatura (fondo #0F0F10, acento #FFD400, 1 protagonista, texto distinto del título, sin código legible)

Las tres llevan una **burbuja de chat genérica y chica, sin logo** (es la señal de IA y sigue sirviendo si el título cambia a ChatGPT). Cada una tiene un solo protagonista.

| | Protagonista visual | Texto | Contraste | Va con |
|---|---|---|---|---|
| **A (principal)** | **Solo el gráfico de barras** de la hoja `Resumen` (ventas por vendedor), grande y en ángulo, con la burbuja de chat chica en una esquina. Sin tabla ni otros elementos | **4 HORAS → [N] MIN** ([N] medido). Si [N] no impresiona (más de 15 min): **4 H → 1 CELDA** (el reporte de cobranza que se arma con la fórmula 8). Nunca sin cifra | Barras verde brillante sobre negro; flecha y texto en amarillo | Título 1 |
| **B** | Una celda verde con un check y, debajo, una grieta roja que la parte | **PARECE BIEN** | Verde "correcto" contra grieta roja: el error silencioso del título 2 | Título 2 |
| **C** | Celda gigante "Vencido" en rojo con un sello amarillo "PAGADO" encima; burbuja de chat chica, sin alerta | **610.575 DE MÁS** | Rojo contra sello amarillo; la cifra sale de la planilla (diferencia entre 2.446.165 y 1.835.590) | Título 3 |

**Alternativa fuera del A/B:** la miniatura "SIN #N/A" (`#N/A` en gris contra la hoja terminada). Pega fuerte para Laura, pero contradice el título 2 (el error del video no da #N/A). Si el A/B del título 1 pierde, se puede probar en un segundo A/B, con el título 1.

Ninguna muestra `=BUSCARX(`: no se lee a 120 px y el video 3 lo necesita. **Respaldo de las cifras:** "4 HORAS" es una estimación medida por el creador y en el video se dice "estimado". "610.575" está calculado con la tabla y hay que verificarlo en Excel.

## Riesgos

- **Respuestas de Claude reales (regla 4):** los 10 prompts (y el de la Prueba sobre la fórmula escrita a mano) se corren en claude.ai gratis antes de escribir el guion y se guardan textuales con fecha. El giro ya no depende de que la IA se equivoque, solo de que la Prueba señale "Pagado". El límite de mensajes del plan gratis puede obligar a repartir las corridas en dos sesiones.
- **Separador y regionalización:** Excel para la web toma el separador de la configuración regional. En es-MX suele ser `,` y en es-ES y es-AR, `;`. Hay que avisarlo en pantalla en la fórmula 1 y meterlo en el "Mapa". Verificar con una cuenta configurada en México.
- **Disponibilidad de funciones en Excel para la web:** TEXTODESPUES/TEXTOANTES, ELEGIRCOLS, FILTRAR, ORDENAR, UNICOS y SI.CONJUNTO existen en Excel para la web y Microsoft 365, pero **no en Excel 2016/2019**: se avisa en los primeros 30 s y de nuevo con un `aviso` breve en la fórmula 3. Probar las 10 fórmulas en Excel para la web en español el día del guion, con los resultados exactos de la tabla (los valores de esta idea están calculados con un script y no se probaron en Excel).
- **FIN.MES y fechas:** las celdas de vencimiento necesitan formato de fecha; si no, se ve el número de serie (46.326). Es un buen momento de veredicto honesto, pero hay que mostrarlo bien.
- **ORDENAR sobre "Sin vencidos":** si no hay vencidos, la fórmula 8 devuelve una sola celda de texto; verificar que no dé #¡VALOR!.
- **Cronómetro "a mano vs. con IA":** el tiempo con IA se mide al construir la plantilla y el "a mano" se estima y se declara como estimación. No se inventa.
- **Herramientas que cambian:** el límite del plan gratis de Claude, ChatGPT y Copilot puede cambiar; hay que verificarlo el día del guion. No mencionar Copilot dentro de Excel salvo para decir que es de pago (cambió dos veces en 2026).
- **Demanda sin medir (condición del creador):** ver el procedimiento en "Evidencia de demanda".
- **Temas sensibles:** ninguno. Cobranza y descuentos son gestión, no consejo financiero. Todos los nombres de clientes y vendedores son ficticios: verificar que no coincidan con empresas conocidas del rubro.
- **Contenido inauténtico (regla 6):** el video tiene su caso propio (distribuidora, cobranza), su error típico propio (la fórmula que ignora "Pagado") y su método. No reutilizar esta planilla en los videos 3 (BUSCARX) ni 9 (inventario).
- **Ritmo (nota para el guionista):** las fórmulas fáciles (2, 5, 9) duran unos 35 s; la 8 (matriz) se desglosa pieza por pieza (ELEGIRCOLS → FILTRAR → ORDENAR).
