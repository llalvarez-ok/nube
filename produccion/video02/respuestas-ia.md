# video02 · Prompts y respuestas de IA usados en el video

- **Herramienta:** Claude. Las respuestas las generó Claude (el mismo modelo que escribe este guion) el 25/10/2026, en la sesión del guionista. **No se corrieron en claude.ai con el plan gratuito.** Desde la ronda 2 del guion, el rótulo del chat dice solo "Claude", sin plan, y la voz no menciona el plan gratuito. Correr estos prompts en claude.ai gratis es **opcional**: solo hace falta si se quiere volver a poner el plan ("versión gratuita") en el rótulo. Si se corren y alguna respuesta cambia de sentido (sobre todo la 7b, que sostiene el giro), se reemplaza el texto en `guion.json` y se vuelve a debate.
- **Formato:** es una sola conversación. El primer mensaje lleva el Mapa completo y los demás mensajes dan por sabido ese Mapa. Desde la fórmula 8, cada prompt lleva las tres partes (Mapa · Meta · Prueba).
- **Qué se muestra:** en `guion.json` las respuestas aparecen recortadas para que entren en pantalla, sin cambiar el sentido. Aquí está el texto completo.
- Los datos son de la planilla ficticia "Distribuidora Sur".

---

## 1 · BUSCARX (Mapa + Meta) · se muestra en pantalla

**Prompt**

> Excel para la web en español, separador punto y coma. Hoja Pedidos, filas 2 a 13: A Fecha, B Cliente, C Cliente limpio, D Vendedor, E Vendedor limpio, F Código, G Cantidad, H Precio, I Descuento, J Neto, K Vence, L Pagado (Sí/No), M Estado. Catálogo en la hoja Productos: A Código, C Precio. Fecha de corte en Resumen!B1.
> En H2 quiero el precio de cada código; si no existe, que diga "Código no existe". Una fórmula para copiar hacia abajo.

**Respuesta**

> Escribe esto en H2 y cópialo hasta H13:
>
> `=BUSCARX(F2;Productos!A:A;Productos!C:C;"Código no existe")`
>
> BUSCARX busca el código de F2 en la columna A de Productos y devuelve el precio de la columna C. El último argumento es lo que muestra si no encuentra el código, así que no verás #N/A.
>
> Si tu Excel no tiene BUSCARX (Excel 2019 o anterior), avísame y te la paso con BUSCARV o con INDICE y COINCIDIR.

## 2 · NOMPROPIO + ESPACIOS (Meta) · no se muestra el chat, se pega la fórmula

**Prompt**

> En C2 quiero el nombre del cliente de B2, prolijo: sin espacios de más y con mayúscula inicial en cada palabra.

**Respuesta**

> `=NOMPROPIO(ESPACIOS(B2))`
>
> ESPACIOS quita los espacios del principio y del final, y deja uno solo entre palabras. NOMPROPIO pone en mayúscula la primera letra de cada palabra y el resto en minúscula.
>
> Ojo: las siglas también cambian ("SRL" queda "Srl") y no agrega tildes que falten. Revisa esos casos a mano.

## 3 · TEXTODESPUES (Meta) · no se muestra el chat

**Prompt**

> En D2 viene el vendedor así: "V01 | Diego Paz". En E2 quiero solo el nombre.

**Respuesta**

> `=TEXTODESPUES(D2;"| ")`
>
> Devuelve todo lo que viene después de "| ". Si alguna vez necesitas el código, usa `=TEXTOANTES(D2;" |")`.
>
> TEXTODESPUES está en Excel para la web y en Microsoft 365. Si alguna fila no tiene la barra, devuelve #N/A; puedes usar `=TEXTODESPUES(D2;"| ";;;;D2)` para que, en ese caso, deje el texto original.

## 4 · SI.CONJUNTO (Meta) · se muestra en pantalla

**Prompt**

> En I2 quiero el descuento según el total de la compra (G2*H2): 10 % si llega a 100.000; 5 % si llega a 40.000; si no, 0 %.

**Respuesta**

> `=SI.CONJUNTO(G2*H2>=100000;10%;G2*H2>=40000;5%;VERDADERO;0)`
>
> Las condiciones se evalúan en orden, por eso va primero el tramo más alto. El VERDADERO del final funciona como "en cualquier otro caso". Dale formato de porcentaje a la columna I.
>
> Si H2 dice "Código no existe", el resultado será #¡VALOR!: corrige el código y se arregla solo.

## 5 · FIN.MES (Meta) · no se muestra el chat

**Prompt**

> En K2 quiero el vencimiento: la condición es pago a fin del mes siguiente a la fecha de A2.

**Respuesta**

> `=FIN.MES(A2;1)`
>
> FIN.MES devuelve el último día del mes que está a un mes de A2. Para un pedido del 04/08/2026 da 30/09/2026.
>
> Dale formato de fecha a la columna K; si no, vas a ver un número como 46295.

## 6 · SUMAR.SI.CONJUNTO (Meta) · se muestra en pantalla

**Prompt**

> En Resumen tengo los vendedores en A3:A5 y en B2 el primer día del mes que quiero ver. En B3 quiero el neto vendido por ese vendedor en ese mes. Una fórmula para copiar hacia abajo.

**Respuesta**

> `=SUMAR.SI.CONJUNTO(Pedidos!J:J;Pedidos!E:E;A3;Pedidos!A:A;">="&$B$2;Pedidos!A:A;"<="&FIN.MES($B$2;0))`
>
> Suma el neto (J) de las filas donde el vendedor limpio (E) es el de A3 y la fecha (A) está entre el primer y el último día del mes de B2. Los $ dejan fija B2 cuando copias hacia abajo; A3 sí cambia.
>
> Si en Pedidos hay fechas guardadas como texto, no se suman y no da error: compruébalo con un filtro.

## 7a · SI, estado de cobro, con Mapa + Meta (sin Prueba) · no se muestra; respalda el "hallazgo honesto"

**Prompt**

> En M2 quiero el estado de cada factura: si ya venció a la fecha de corte, que diga "Vencido"; si no, "Al día". Una fórmula para copiar hacia abajo.

**Respuesta**

> `=SI(K2<Resumen!$B$1;"Vencido";"Al día")`
>
> El $ deja fija la fecha de corte cuando copias la fórmula.
>
> Un detalle: tienes la columna L (Pagado). Una factura pagada no debería figurar como "Vencido". Si quieres tenerlo en cuenta:
>
> `=SI(L2="Sí";"Cobrado";SI(K2<Resumen!$B$1;"Vencido";"Al día"))`

## 7b · Prueba sobre la fórmula escrita a mano · se muestra en pantalla (el giro)

**Prompt**

> Escribí esta fórmula para M2: =SI(K2<Resumen!$B$1;"Vencido";"Al día"). ¿Qué casos pueden hacer que dé un resultado equivocado sin mostrar error? ¿Qué debería dar la fila 2 (vence 30/09/2026, Pagado: Sí) y la fila 6 (vence 31/10/2026, Pagado: No), con corte 04/11/2026?

**Respuesta**

> Casos que dan un resultado equivocado sin mostrar error:
>
> 1. Facturas pagadas: la fórmula no mira la columna L. Si una factura ya se pagó pero su vencimiento pasó, dice "Vencido".
> 2. Vencimiento vacío: una celda vacía cuenta como 0, así que también dice "Vencido".
> 3. Fechas guardadas como texto: Excel considera que un texto es mayor que cualquier número, así que dice "Al día" aunque esté vencida.
> 4. Vence el mismo día del corte: dice "Al día", porque usas < y no <=. Decide si es lo que quieres.
>
> Comprobación:
> - Fila 2: tu fórmula da "Vencido", pero la factura ya está pagada. Debería decir algo como "Cobrado".
> - Fila 6: da "Vencido", y es correcto: venció el 31/10 y no está pagada.
>
> Fórmula corregida (cubre el caso 1):
>
> `=SI(L2="Sí";"Cobrado";SI(K2<Resumen!$B$1;"Vencido";"Al día"))`
>
> Si también quieres cubrir el caso 2, agrega `SI(K2="";"Sin fecha";…)` antes de comparar la fecha.

## 8 · FILTRAR + ORDENAR + ELEGIRCOLS (Mapa · Meta · Prueba) · se muestra en pantalla

**Prompt**

> Mapa: el de antes. Meta: en Resumen!D2, una lista que se actualice sola con Cliente (C), Vence (K) y Neto (J) de las facturas "Vencido", de mayor a menor neto. Prueba: antes de darme la fórmula, dime qué casos darían un resultado equivocado sin error y qué debería salir arriba.

**Respuesta**

> Casos a vigilar:
>
> 1. Si no hay ninguna vencida, FILTRAR no tiene nada que devolver y ORDENAR daría error. Lo cubro con SI.ERROR.
> 2. Los pedidos que agregues debajo de la fila 13 quedan afuera. Amplía los rangos o convierte los datos en una tabla.
> 3. Si algún neto está guardado como texto, se ordena mal sin avisar.
> 4. Deja libres las celdas de D2 hacia abajo y hacia la derecha: si hay algo escrito, verás #¡DESBORDAMIENTO!.
>
> Arriba debería salir la factura vencida con el neto más alto. Compruébalo filtrando Pedidos por "Vencido" y ordenando J de mayor a menor.
>
> `=SI.ERROR(ORDENAR(FILTRAR(ELEGIRCOLS(Pedidos!A2:M13;3;11;10);Pedidos!M2:M13="Vencido");3;-1);"Sin vencidos")`
>
> ELEGIRCOLS toma las columnas 3, 11 y 10 (C, K y J), FILTRAR deja solo las vencidas y ORDENAR las ordena por la tercera columna (Neto), de mayor a menor. Dale formato de fecha a la columna E.

## 9 · UNICOS + ORDENAR (Mapa · Meta · Prueba) · no se muestra el chat

**Prompt**

> Meta: en Resumen!A8, la lista de clientes de Pedidos!C2:C13, sin repetidos y en orden alfabético. Prueba: ¿qué podría salir mal sin error?

**Respuesta**

> `=ORDENAR(UNICOS(Pedidos!C2:C13))`
>
> UNICOS deja cada cliente una sola vez y ORDENAR los pone de la A a la Z. La lista se actualiza sola si cambian los pedidos.
>
> Qué podría salir mal sin error: UNICOS considera distintos "Hotel Mirador" y "Hotel  Mirador" (con dos espacios), así que un cliente puede aparecer dos veces. Por eso conviene usar la columna C, ya limpia, y no la B. Y, como antes, los pedidos debajo de la fila 13 quedan afuera.

## 10 · CONTAR.SI.CONJUNTO (Mapa · Meta · Prueba) · no se muestra el chat

**Prompt**

> Meta: en Resumen!B8, cuántas facturas "Vencido" tiene el cliente de A8 (en Pedidos, el cliente está en C y el estado en M). Para copiar hacia abajo. Prueba: ¿qué podría dar mal sin error?

**Respuesta**

> `=CONTAR.SI.CONJUNTO(Pedidos!C:C;A8;Pedidos!M:M;"Vencido")`
>
> Cuenta las filas donde el cliente es el de A8 y el estado es "Vencido". Cópiala hasta B12.
>
> Qué podría dar mal sin error: si el estado tiene un espacio de más ("Vencido ") o el nombre del cliente no coincide exactamente, cuenta 0 sin avisar. Compruébalo con un cliente: filtra Pedidos por su nombre y cuenta a mano las vencidas.
