# Motor v2 · catálogo para guionistas y directores visuales

`python3 herramientas/motor.py <video>` convierte `produccion/<video>/guion.json` en un video de *motion graphics*: cada cuadro se anima con GSAP y se captura con Chromium. Este documento es la referencia para escribir `guion.json`.

## Reglas de oro para la retención
1. **Algo se mueve cada 2–4 s.** En las escenas `excel` y `chat`, cada beat debe tener al menos una `accion`. Un beat sin acción = imagen quieta mientras se habla.
2. **Un beat = una o dos frases (≤ 25 palabras).** Cada beat se sintetiza por separado y las acciones arrancan al principio del beat: escribe la voz para que nombre lo que aparece en ese momento.
3. **Mostrar, no contar.** Si la voz dice "la fórmula suma las ventas del norte", en pantalla se escribe la fórmula y se resalta el rango.
4. **Cámara al detalle.** `zoom` a la zona de la acción antes de escribir o calcular, `zoom_fuera` para mostrar el resultado completo. Una fórmula se lee en un celular solo con zoom de 1,4x o más.
5. **Variedad:** no más de 3 escenas seguidas de la misma plantilla, y **no más de ~60 % del video en `excel`**. Entre fórmulas, intercala `titular`, `cifra`, `lista`, `capitulo` o un `rotulo`. Cada 60–90 s, un cambio fuerte: `capitulo`, `antes_despues`, `cifra` o `aviso`.

## Estructura

```json
{"titulo": "Título del video", "duracion_objetivo_min": 10,
 "marca": {"nombre": "Atajos IA", "acento": "#ffd400", "visible": false},
 "musica": "produccion/musica/tema.mp3", "nivel_musica": 0.16, "nivel_sfx": 0.55,
 "subtitulos": false, "progreso": true,
 "fuentes": [{"dato": "...", "fuente": "URL", "fecha": "AAAA-MM"}],
 "escenas": [
   {"plantilla": "excel", "capitulo": "Fórmula 1: SI", "transicion": "zoom",
    "datos": {...}, "beats": [{"voz": "...", "voz_tts": "(opcional)", "pausa": 0.3, "accion": {...}}]}]}
```

- `elegir_rama` (en un beat): la voz depende de una respuesta real de IA que todavía no se corrió (variantes en `voz_rama_b`, `voz_si_falla`…). `motor.py` no hace el video final hasta que el beat tiene `rama_elegida` y la `voz` correcta; `--sin-voz` y `--cuadros` sí funcionan.
- `voz_tts`: el texto que se manda a la voz cuando la pronunciación lo pide ("B-U-S-C-A-R-X", "punto y coma"); los subtítulos usan `voz`.
- `marca.visible`: muestra el logo arriba a la izquierda (apagado por defecto: YouTube ya pone la marca de agua del canal y el logo choca con los zooms).
- `fondo_desenfocado: true` (en una escena de texto: `titular`, `capitulo`…): la última escena `excel`/`chat` anterior queda de fondo, desenfocada y oscura, en lugar del negro. Sirve para que un capítulo o un titular no se vea como otra pantalla oscura igual a la anterior.
- `capitulo`: marca un capítulo para la descripción y una marca en la barra de progreso.
- `transicion` (de entrada): `empuje` (por defecto), `zoom` (por defecto en excel y chat), `barrido` (por defecto en capitulo: barrido amarillo con el logo), `fundido`, `corte`.
- Opciones de escena: `entrada` (segundos antes del primer beat, 0,45), `cola` (segundos después del último, 0,35), `extra`.
- Texto con `*asteriscos*` → resaltado con el marcador amarillo (en titular, lista, cifra, aviso, nota y comparar).
- Íconos: cualquier nombre de [Lucide](https://lucide.dev/icons) (`table`, `target`, `sparkles`, `clock`, `file-spreadsheet`, `calculator`, `mail`…).

## Plantillas

| Plantilla | `datos` | Sincronía con los beats |
|---|---|---|
| `titular` | `etiqueta`, `icono`, `lineas: ["...", {"texto": "...", "beat": 1}]`, `sub`, `sub_beat`, `tamano` | Las líneas entran en el beat 0 (o en su `beat`); el `sub` en el beat 1 |
| `cifra` | `valor`, `prefijo`, `sufijo`, `decimales`, `etiqueta`, `fuente` | Cuenta de 0 al valor al empezar |
| `antes_despues` | `antes: {segundos, texto, beat, etiqueta}`, `despues: {…}`; en lugar de `segundos`, `valor` + `sufijo` muestra una cifra ("10" → "5 clientes"). `etiqueta` reemplaza "Antes"/"Después" (p. ej. "Noviembre (hasta el corte)"). `consecuencia: {texto, beat, retraso}` agrega una línea propia debajo de las dos tarjetas | Antes en el beat 0, después en el 1; los relojes (o las cifras) corren |
| `lista` | `titulo`, `items: [{texto, detalle, icono, beat}]` | Un elemento por beat (o el de su `beat`) |
| `capitulo` | `numero`, `total`, `titulo` | Entra con barrido; dura al menos 2,2 s |
| `aviso` | `titulo`, `texto`, `nivel: "rojo"`, `icono` | Sacudida del ícono y sonido de alerta |
| `comparar` | `titulo`, `columnas`, `filas`, `ganador` (índice), `ganador_beat`, `beats_filas`, `resaltar_en` (segundos desde el beat de cada fila en que se pinta el `*marcador*`, para que entre cuando la voz lo dice) | Una fila por beat; el ganador se pinta de amarillo |
| `excel` | ver abajo | Acciones por beat |
| `chat` | `app` ("ChatGPT", "Copilot", "Claude"), `modelo` ("versión gratuita"), `pasos` (tarjetas del método en la cabecera, p. ej. `["Mapa","Meta","Prueba"]`), `etiqueta_fija` (aviso fijo arriba a la derecha, p. ej. "Prompt completo: hoja *Prompts*") | Acciones `prompt`, `respuesta`, `resaltar_prompt`, `lupa`, `paso` |
| `imagen` | `imagen` (ruta desde la raíz del repo; usa `herramientas/recursos.py`), `titulo`, `texto`, `credito`, `foco` ("30% 40%") | Foto a pantalla completa con acercamiento lento y leyenda |
| `final` | `titulo` | Dura al menos 20 s (pantalla final de YouTube); deja huecos para el video y el botón de suscribirse |

### `excel`
`datos`: `archivo`, `hoja`, `asistente` ("Copilot"), `pestana`, `anchos` (px por columna, 210 por defecto), `celdas` (filas desde la fila 1; la primera es el encabezado), `seleccion_inicial`. Se ven 12 filas y unas 7 columnas.
`hojas` (opcional): las pestañas del pie, por ejemplo `["Pedidos", "Dashboard", "Prompts", "Tus datos"]`; `hoja` es la activa.
`filas` (opcional): los números de fila que se ven, en orden, por ejemplo `[1, 241, 242, …, 251]` para mostrar el encabezado inmovilizado y el final de una tabla larga. Las `celdas` siguen siendo las 12 filas visibles, de arriba abajo, y las acciones usan los números reales ("A251"). Una escena con `filas` debería ser `solo_video` (la plantilla no sabe dónde va cada fila).

| Acción | Campos | Qué se ve |
|---|---|---|
| `seleccionar` | `rango` ("B2" o "B2:B13") | El cursor va, hace clic y arrastra la selección |
| `escribir` | `celda`, `texto`, `duracion` | Se escribe letra a letra en la celda y en la barra de fórmulas, con tecleo; se pintan los rangos referidos como en Excel |
| `calcular` | `celda`, `valor`, `derecha` | La fórmula se convierte en el resultado con un destello |
| `rellenar` | `rango`, `valores`, `duracion` | El cursor arrastra el controlador de relleno; los valores caen en cascada |
| `resaltar` | `rango`, `color`, `etiqueta`, `hasta` | Recuadro de color con etiqueta |
| `formato` | `rango` + `fondo` (+ `texto`), o `celdas: {"C3": "#ffd6d6"}` | Las celdas se pintan (formato condicional) |
| `zoom` | `rango`, `escala` (1,3–2,2), `duracion` | La cámara se acerca al rango |
| `zoom_fuera` | `duracion` | Vuelve a la vista completa |
| `nota` | `celda` o `rango`, `texto`, `lado` (auto) | Globo explicativo junto a la celda |
| `quitar_nota` | — | |
| `grafico` | `titulo`, `etiquetas`, `valores`, `textos`, `destacar`, `x`, `y`, `ancho`, `alto` (px de las barras, 300), `max`, `id` | Gráfico de barras que crece sobre la hoja |
| `actualizar_grafico` | `id`, `valores`, `textos`, `destacar`, `etiquetas`, `max` | Las barras del gráfico con ese `id` crecen o bajan a los valores nuevos, con destello del recuadro |
| `tarjeta` | `id`, `titulo`, `valor`, `sub`, `x`, `y`, `ancho` (300), `color` (del número) | Tarjeta de KPI de dashboard: título, número grande y una línea de contexto |
| `actualizar_tarjeta` | `id`, `valor`, `sub`, `color` | Cambia el número de la tarjeta con un destello |
| `desplegable` | `celda`, `opciones`, `elegir` (texto o índice), `valor` | Lista desplegable (validación de datos): se abre bajo la celda y el cursor elige una opción |
| `quitar` | `id` | Retira un gráfico o una tarjeta |
| `panel_ia` | `prompt`, `respuesta`, `formula`, `boton` | Panel lateral de IA: se escribe el prompt, se envía y la respuesta aparece palabra por palabra, con la fórmula y el botón "Insertar" |
| `insertar` | `celda`, `formula`, `valor` | Clic en "Insertar": la fórmula queda en la celda con su resultado |
| `hoja` | `hoja`, `hasta` | El cursor hace clic en esa pestaña del pie y se marca en amarillo (no cambia el contenido de la escena) |
| `rotulo` | `texto`, `sub`, `numero` ("01"), `hasta` (s, 3,2), `posicion` ("arriba": arriba a la derecha, para no tapar las últimas filas ni el pie del gráfico) | Zócalo grande que entra desde la izquierda, en espacio de pantalla (no lo afecta el zoom). Úsalo al empezar cada fórmula o idea clave: puntúa sin salir de la hoja. También existe en `chat` |
| `cerrar_panel`, `quitar_refs`, `mover` (`celda`) | | |

Cada acción admite `retraso` (segundos desde el inicio del beat). Las acciones de un beat se encadenan por tiempo: deja ~1,5 s entre un `escribir` y su `calcular` (usa `retraso` o un beat nuevo).

### `chat`
| Acción | Campos |
|---|---|
| `prompt` | `texto`, `duracion` (se escribe en la caja y sube como mensaje) |
| `respuesta` | `texto`, `formula`, `duracion` (aparece palabra por palabra; la fórmula, en bloque de código) |

| `prompt` (más) | `frases` (textos del prompt que se podrán resaltar), `pausa_en` (texto donde el tecleo se detiene) + `pausa` (s): el prompt se escribe en dos tiempos, al ritmo de la voz |
| `resaltar_prompt` | `frases` (índices de `frases` del último prompt), `lupa` (texto opcional), `hasta`: el prompt queda atenuado y esas frases se pintan de amarillo |
| `lupa` | `texto` (con `*marcador*`), `hasta`, `falta` (borde rojo): recuadro grande de 52 px arriba del chat, legible en el celular, con 3–6 palabras clave |
| `paso` | `n` (índice de `pasos`): enciende esa tarjeta del método; las anteriores quedan como "hechas" |
| `respuesta` (más) | `frase_clave` (parte del texto que se resalta al terminar), `estilo_clave: "falta"` (recuadro rojo: la idea que no aparece), `clave_retraso`, `lupa`, `lupa_hasta`, `recorte: false` (por defecto se ven 3 líneas como máximo, con "…") |

Prompts largos: en pantalla no se lee un prompt de 40–80 palabras. Se muestra completo pero atenuado, se resaltan 3–6 palabras por beat (las que dice la voz) con `resaltar_prompt` o `lupa`, y `etiqueta_fija` remite a la hoja Prompts.
Respuestas aún no corridas: el texto de prueba va con `"maqueta": true` y `nota_maqueta` en el JSON (nunca "PENDIENTE" ni corchetes en pantalla). Al pegar la real se cambia `texto` y `frase_clave`; si hay ramas, la otra va en `rama_b` del mismo objeto.

**El texto de `respuesta` tiene que ser la respuesta real** de esa herramienta a ese prompt (puede recortarse, sin cambiar el sentido).

## Comandos
- `python3 herramientas/motor.py <video> --cuadros 2,8.5,30`: capturas PNG en esos segundos (`build/cuadros/`), para revisar sin renderizar todo.
- `--sin-voz`: vista previa con tiempos estimados y efectos de sonido. `--borrador`: 960×540. `--alta`: 2560×1440 para subir (YouTube les da mejor calidad a los videos 1440p). `--desde/--hasta`: un tramo.
- Velocidad: ~14 cuadros/s con 4 núcleos (un video de 10 min tarda ~20 min).
- Efectos de sonido sintetizados (sin licencias), en `produccion/render/sfx/`: whoosh, clic, tecleo, pop, ding, subida, alerta, enviar, respuesta, brillo, arrastre, tic, zoom.
