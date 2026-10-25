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

- `voz_tts`: el texto que se manda a la voz cuando la pronunciación lo pide ("B-U-S-C-A-R-X", "punto y coma"); los subtítulos usan `voz`.
- `marca.visible`: muestra el logo arriba a la izquierda (apagado por defecto: YouTube ya pone la marca de agua del canal y el logo choca con los zooms).
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
| `antes_despues` | `antes: {segundos, texto, beat}`, `despues: {segundos, texto, beat}` | Antes en el beat 0, después en el 1; los relojes corren |
| `lista` | `titulo`, `items: [{texto, detalle, icono, beat}]` | Un elemento por beat (o el de su `beat`) |
| `capitulo` | `numero`, `total`, `titulo` | Entra con barrido; dura al menos 2,2 s |
| `aviso` | `titulo`, `texto`, `nivel: "rojo"`, `icono` | Sacudida del ícono y sonido de alerta |
| `comparar` | `titulo`, `columnas`, `filas`, `ganador` (índice), `ganador_beat`, `beats_filas` | Una fila por beat; el ganador se pinta de amarillo |
| `excel` | ver abajo | Acciones por beat |
| `chat` | `app` ("ChatGPT", "Copilot", "Claude"), `modelo` ("versión gratuita") | Acciones `prompt` y `respuesta` |
| `imagen` | `imagen` (ruta desde la raíz del repo; usa `herramientas/recursos.py`), `titulo`, `texto`, `credito`, `foco` ("30% 40%") | Foto a pantalla completa con acercamiento lento y leyenda |
| `final` | `titulo` | Dura al menos 20 s (pantalla final de YouTube); deja huecos para el video y el botón de suscribirse |

### `excel`
`datos`: `archivo`, `hoja`, `asistente` ("Copilot"), `pestana`, `anchos` (px por columna, 210 por defecto), `celdas` (filas desde la fila 1; la primera es el encabezado), `seleccion_inicial`. Se ven 12 filas y unas 7 columnas.

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
| `grafico` | `titulo`, `etiquetas`, `valores`, `textos`, `destacar`, `x`, `y`, `ancho` | Gráfico de barras que crece sobre la hoja |
| `panel_ia` | `prompt`, `respuesta`, `formula`, `boton` | Panel lateral de IA: se escribe el prompt, se envía y la respuesta aparece palabra por palabra, con la fórmula y el botón "Insertar" |
| `insertar` | `celda`, `formula`, `valor` | Clic en "Insertar": la fórmula queda en la celda con su resultado |
| `rotulo` | `texto`, `sub`, `numero` ("01"), `hasta` (s, 3,2) | Zócalo grande que entra desde la izquierda, en espacio de pantalla (no lo afecta el zoom). Úsalo al empezar cada fórmula o idea clave: puntúa sin salir de la hoja. También existe en `chat` |
| `cerrar_panel`, `quitar_refs`, `mover` (`celda`) | | |

Cada acción admite `retraso` (segundos desde el inicio del beat). Las acciones de un beat se encadenan por tiempo: deja ~1,5 s entre un `escribir` y su `calcular` (usa `retraso` o un beat nuevo).

### `chat`
| Acción | Campos |
|---|---|
| `prompt` | `texto`, `duracion` (se escribe en la caja y sube como mensaje) |
| `respuesta` | `texto`, `formula`, `duracion` (aparece palabra por palabra; la fórmula, en bloque de código) |

**El texto de `respuesta` tiene que ser la respuesta real** de esa herramienta a ese prompt (puede recortarse, sin cambiar el sentido).

## Comandos
- `python3 herramientas/motor.py <video> --cuadros 2,8.5,30`: capturas PNG en esos segundos (`build/cuadros/`), para revisar sin renderizar todo.
- `--sin-voz`: vista previa con tiempos estimados y efectos de sonido. `--borrador`: 960×540. `--alta`: 2560×1440 para subir (YouTube les da mejor calidad a los videos 1440p). `--desde/--hasta`: un tramo.
- Velocidad: ~14 cuadros/s con 4 núcleos (un video de 10 min tarda ~20 min).
- Efectos de sonido sintetizados (sin licencias), en `produccion/render/sfx/`: whoosh, clic, tecleo, pop, ding, subida, alerta, enviar, respuesta, brillo, arrastre, tic, zoom.
