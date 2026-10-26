# video03 · Respuestas de IA (pendientes de correr)

Estado al 26/10/2026: **ninguna respuesta de este archivo salió todavía de claude.ai**. Todas las acciones `respuesta` y los rótulos con frases de Claude en `guion.json` llevan `"pendiente_respuesta_real": true` y textos de borrador que empiezan con «PENDIENTE». El orquestador no tiene acceso a claude.ai: corre todo el creador, antes del **viernes 30/10**.

## Cómo correrlos
- claude.ai con el **plan gratuito** (anota el modelo que muestra la interfaz y la fecha). Guarda cada respuesta **textual** (copiar y pegar) y una **captura**, debajo de su prompt.
- **Conversación A:** solo el prompt 1, con el .xlsx adjunto. Archivo: la hoja Pedidos de la plantilla (`produccion/video03/plantilla/`), guardada sola como `Distribuidora Sur - Pedidos 2026.xlsx`; o `fuente/pedidos.csv` abierto y guardado como .xlsx.
- **Conversación B:** los prompts 2 a 5, en orden y en la misma conversación, **sin archivo**. Es lo que enseña el video: el Mapa describe las columnas y nunca se pegan los datos.
- **Prompt 5b:** el prompt 5 otra vez, en una conversación nueva y con el .xlsx adjunto. Es la condición del showrunner. Anota si cambia la rama (A o B).
- Escenas y beats se cuentan desde 0, en el orden de `guion.json`.
- Copia los prompts tal cual. Si Claude da una fórmula distinta, no la cambies en el guion: anótala y avisa. El guionista ajusta `escribir`/`calcular` y vuelve a correr `plantilla_xlsx.py --verificar`.

---

## Prompt 1 · Mensaje único («Lo probé», escena 1, ≤ 30 s)
```
Te adjunto Distribuidora Sur - Pedidos 2026.xlsx (datos ficticios). Hazme un dashboard de ventas en Excel para la reunión del lunes: indicadores, gráficos y un filtro por vendedor, que se actualice cuando pegue pedidos nuevos.
```
**Qué revisar:**
1. ¿El plan gratuito acepta el .xlsx y lo lee? Si pide pagar, se agotan los mensajes o no lo lee, **eso es lo que se muestra**.
2. ¿Qué entrega: un .xlsx, una página o artefacto (HTML/React), o solo instrucciones?
3. ¿Se rehace al pegar pedidos nuevos (Tabla o rangos dinámicos) o queda fijo?
4. ¿Incluye una tarjeta «este mes contra el anterior»? Si la incluye, ¿cuánto da y avisa del mes incompleto?
5. Compara 2 números con los del video: ventas del año **46.586.220** y octubre **4.574.425**.

**Ramas (escena 1, beat 2):**
- **Funciona (entrega algo usable):** se queda la voz del guion, «Rápido, sí. Pero ¿cómo sabes si esos números están bien?». El rótulo «Veredicto» dice lo que salió (por ejemplo «hecho en 1 mensaje · no es un Excel que se rehaga»), siempre cierto. Sin A/B 3 condicional.
- **Falla o queda a medias:** usar `voz_si_falla` del beat 2. La captura va tal cual y entra el A/B 3 condicional «Le pedí a la IA un dashboard en 1 mensaje: esto salió», con la miniatura C.
- **No se corrió:** se elimina la escena 1 entera (unos 18 s) y la lista de las 4 preguntas pasa a ser la escena siguiente al hook.
- **Rótulo del hook:** «Claude · versión gratuita» solo si el plan gratuito leyó el .xlsx. Si no, «Claude» a secas, y «gratis» queda solo para Excel para la web.

## Prompt 2 · Mapa + Meta de la pregunta 1 (escena 5)
```
Mapa: Excel para la web en español, separador punto y coma. Tabla llamada Pedidos con las columnas Fecha, Cliente, Vendedor, Código, Cant., Precio, Desc., Neto, Vence, Pagado (Sí/No) y Estado (Cobrado, Vencido o Al día). En la hoja Dashboard, B1 es la fecha de corte y B2 el vendedor (o Todos). Usa referencias a la Tabla, como Pedidos[Neto].
Meta: En Dashboard!B3, las ventas netas del año hasta la fecha de corte. En B4, cuántos pedidos hay en ese período. En B5, las ventas del último mes cerrado antes de la fecha de corte.
```
**Qué revisar:**
- Que use la Tabla (`Pedidos[Neto]`, `Pedidos[Fecha]`) y no rangos como H2:H250.
- Que B5 sea el **último mes cerrado** (octubre) y no los últimos 30 días.
- Fórmulas del video (pegarlas en Excel para la web y comparar):
  - B3 `=SUMAR.SI.CONJUNTO(Pedidos[Neto];Pedidos[Fecha];">="&FECHA(AÑO(B1);1;1);Pedidos[Fecha];"<="&B1)` → **46.586.220**
  - B4 `=CONTAR.SI.CONJUNTO(Pedidos[Fecha];">="&FECHA(AÑO(B1);1;1);Pedidos[Fecha];"<="&B1)` → **250**
  - B5 `=SUMAR.SI.CONJUNTO(Pedidos[Neto];Pedidos[Fecha];">"&FIN.MES(B1;-2);Pedidos[Fecha];"<="&FIN.MES(B1;-1))` → **4.574.425**
- Si sus fórmulas son distintas pero dan lo mismo, se puede mostrar la de Claude (avisa para cambiar `escribir`).

## Prompt 3 · Meta de la pregunta 2 (escena 9)
```
En B6, las ventas de este mes hasta la fecha de corte, y en B7 la variación de este mes contra el mes anterior, en porcentaje. Para el gráfico, en H2:I13, las ventas de cada mes del año, de enero a diciembre.
```
**Qué revisar:**
- Que B7 sea `=B6/B5-1` (o equivalente) → **−90,4 %**, y B6 → **441.000**.
- Los 12 meses fijos, con diciembre en 0 y noviembre en 441.000.
- **Importante para el giro:** ¿avisa ya aquí, sin que se lo pidas, de que noviembre está incompleto?
  - **Si avisa:** es un hallazgo honesto. El beat «¿Se desplomaron las ventas? La fórmula no da error…» se cambia por «Ojo: Claude ya avisa algo. Lo dejo así y lo comprobamos después de las otras dos preguntas». El giro pasa a «la IA a veces avisa sola; la Prueba, siempre», como en video02.
  - **Si no avisa:** el guion queda como está.

## Prompt 4 · Meta de la pregunta 3 (escena 13)
```
En B2 pondré una lista desplegable con Todos, Diego Paz, Carla Ruiz y Tomás Gil. En B10 quiero las ventas del año del vendedor de B2; si dice Todos, las de todos. Y el mismo filtro para las ventas por producto de O2:O8.
```
**Qué revisar:**
- El criterio de «Todos». El guion dice que usa el comodín `*` (`SI(B2="Todos";"*";B2)`). Si Claude propone otra cosa (por ejemplo, `SI(B2="Todos";SUMAR.SI.CONJUNTO(…);…)`), la voz del beat 1 («El truco está en el criterio: …asterisco…») se reescribe con lo que dijo.
- Con Carla Ruiz, B10 → **16.253.850**; con Todos → **46.586.220**.

## Prompt 5 · La Prueba (el paso secreto, escena 18) — **el más importante**
```
Prueba: B7 es la variación de este mes contra el anterior (=B6/B5-1) y hoy muestra −90,4 %. ¿Qué situación puede hacer que esta tarjeta muestre un número creíble pero equivocado, sin dar error? ¿Qué debería mostrar con fecha de corte 03/11/2026?
```
**Qué revisar:** si menciona, con estas u otras palabras, que noviembre lleva 3 días (mes incompleto) contra un octubre completo, y qué propone mostrar.

**Rama A (lo ve):**
- Voz del beat 2: «Lo vio: noviembre lleva tres días, y octubre, treinta y uno.»
- El rótulo lleva la frase **textual** de Claude que lo dice (recortada, sin cambiar el sentido).
- La comprobación de la escena 19 (fecha de corte en 31/10 → +8,6 %) se mantiene como prueba propia.
- Si propone también el mes cerrado o el mismo tramo, se puede decir «y propone lo mismo que vas a ver».

**Rama B (no lo ve):**
- Voz del beat 2: usar `voz_rama_b`: «Esta vez no lo vio. Por eso la prueba también la haces tú: cambio la fecha de corte.»
- El rótulo lleva lo que sí dijo (por ejemplo, «propuso revisar divisiones por cero»), textual.
- Se suma a «Límites» o al titular de la lección: «la IA no siempre ve el problema: la Prueba también la haces tú».
- **Nunca** se escribe que Claude lo vio si no lo vio.

**Prompt 5b (con el .xlsx):** anota la rama. Si en 5 sale B y en 5b sale A (o al revés), el video muestra la de la conversación B (5) y la descripción lo aclara en una línea.

## Lo que el video afirma de Claude y depende de estas corridas
| Escena / beat | Afirmación | Depende de |
|---|---|---|
| 0 / 4 (rótulo) | «Excel para la web gratis + Claude» («versión gratuita» solo si pasa) | Prompt 1 |
| 1 / 1-2 | Lo que salió del mensaje único y el veredicto | Prompt 1 |
| 5 / 3 | «Me da tres fórmulas, una por celda» | Prompt 2 |
| 9 / 1 | «La variación de este mes contra el anterior, y las ventas de cada mes» | Prompt 3 |
| 13 / 1 | «El truco está en el criterio: … asterisco» | Prompt 4 |
| 18 / 1-2 | Respuesta a la Prueba, rama A o B | Prompt 5 |
| 28 / 2 | «el mismo prompt sirve en ChatGPT o Copilot. La respuesta puede cambiar» | Afirmación general, sin corrida |

Cuando estén las respuestas: reemplazar los textos «PENDIENTE…» de `guion.json`, quitar `pendiente_respuesta_real`, completar la columna «Fórmula que dio Claude» de la hoja Prompts (`plantilla_extra`) y poner la fecha en `descripcion_avisos` y `leeme`.
