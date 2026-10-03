# 06 · Producción con IA: el flujo de trabajo

> **Principio:** la IA acelera la investigación, el borrador, la edición y el empaque. **La demostración, la voz, el criterio y la verificación son humanos.** Eso hace que el canal sea mejor y además lo mantiene dentro de la política de contenido inauténtico de YouTube (julio de 2026).

## 1. Pipeline por video (meta: ~4,5 h por video largo + 3 Shorts)

| Etapa | Tiempo | IA hace | Tú haces |
|---|---|---|---|
| 1. Investigación | 30 min | Busca consultas, resume a los 5 primeros competidores y detecta huecos | Eliges el ángulo y la promesa |
| 2. Empaque | 20 min | Propone 20 títulos y 10 conceptos de miniatura | Eliges 3 + 3 |
| 3. Guion | 40 min | Primer borrador con la estructura de [04](04-sistema-de-contenido.md) | Lo reescribes con tu voz y verificas todo |
| 4. Prueba de la demo | 20 min | — | Haces la tarea real y mides el tiempo |
| 5. Grabación | 45 min | — | Pantalla y voz (el guion a la vista, sin leer de forma robótica) |
| 6. Edición | 70 min | Corta silencios, transcribe, propone zooms y sugiere B-roll | Ritmo, claridad y revisión |
| 7. Miniaturas | 25 min | Fondos y recortes | Composición final y texto |
| 8. Publicación | 15 min | Descripción, capítulos y tags a partir de la transcripción | Revisión y programación |
| 9. Reutilización | 30 min | Detecta los mejores momentos y los reencuadra en vertical | Eliges y ajustas los Shorts |
| 10. Análisis | 10 min | Resume las métricas | Decides los cambios |

## 2. Herramientas recomendadas

Los precios y las funciones cambian: **verifica el plan actual antes de pagar.** Empieza con lo gratuito y paga solo cuando el cuello de botella sea claro.

| Función | Opción gratis o barata | Opción pro (cuando haya ingresos) |
|---|---|---|
| Investigación de temas | YouTube autocompletar, vidIQ/TubeBuddy (gratis), Google Trends | vidIQ Boost |
| Investigación con fuentes | Perplexity, NotebookLM, modo búsqueda de ChatGPT, Claude o Gemini | — |
| Guion | ChatGPT / Claude / Gemini (gratis) | Plan pago de **una** de ellas |
| Grabación de pantalla | OBS Studio (gratis) | Screen Studio (Mac) o Camtasia |
| Audio | Micrófono USB dinámico + reducción de ruido en el editor | Adobe Podcast Enhance |
| Edición | CapCut (escritorio) o DaVinci Resolve (gratis) | Descript (edición por texto) |
| Miniaturas | Canva (gratis), Photopea | Canva Pro, Photoshop |
| Subtítulos | Automáticos de YouTube + corrección | CapCut / Descript |
| Shorts desde el video largo | Reencuadre manual en CapCut | Opus Clip u otro recortador automático |
| Gestión | Notion o Google Sheets + Calendar | — |
| Newsletter | Beehiiv, Substack o MailerLite (planes gratis) | El mismo, en plan pago |

**Voz:** usar **tu voz real**. Si alguna vez usas voz sintética (por ejemplo, para doblar a otro idioma), hay que declararlo y marcar la opción de "contenido alterado o sintético" cuando corresponda.

## 3. Plantillas de prompts de producción

**Investigación**
```
Soy creador de un canal de YouTube en español sobre IA práctica para el trabajo (público: oficinistas, profesionales y pymes no técnicos).
Tema: [TEMA]. 
1) Lista 15 formas en que la gente buscaría esto en YouTube (en español de LatAm y España).
2) ¿Qué preguntas concretas tiene alguien que busca esto?
3) ¿Qué errores o dudas comunes tiene?
4) Propón 3 ángulos diferentes a "tutorial genérico".
No inventes estadísticas; si das un dato, marca que debo verificarlo.
```

**Análisis de la competencia** (pegando las transcripciones o descripciones de los 3–5 primeros videos)
```
Estos son los videos que hoy rankean para "[CONSULTA]". Para cada uno: promesa, estructura, qué hace bien y qué deja sin resolver. Luego: ¿qué video debería hacer yo para ser claramente mejor que todos?
```

**Empaque**
```
Promesa del video: [PROMESA]. Público: [PERSONA de 01]. 
Dame 20 títulos (<60 caracteres, palabra clave "[KW]" al inicio en al menos 10) usando estas fórmulas: [pegar fórmulas de 04 §3].
Luego 10 conceptos de miniatura: 1 elemento visual protagonista + máximo 3 palabras que NO repitan el título.
```

**Guion**
```
Escribe un guion para YouTube de [N] minutos con esta estructura: [pegar estructura A/B/C de 04 §5].
Tono: cercano, directo, español neutro con "tú", sin hype, frases cortas para leer en voz alta.
Incluye marcas [PANTALLA] y [TEXTO], un hook con el resultado en la primera línea, un bucle abierto, un CTA de suscripción con motivo después del primer resultado, un reenganche a mitad y un cierre que lleve a: [SIGUIENTE VIDEO].
Deja entre [corchetes] todo dato, tiempo o resultado que deba medir yo en la demo. No inventes resultados.
```

**Publicación** (pegando la transcripción final)
```
Con esta transcripción: 1) descripción (primeras 2 líneas con la palabra clave "[KW]" y el beneficio), 2) capítulos con marcas de tiempo, 3) 3 Shorts candidatos (minuto de inicio y fin, hook de 1 línea), 4) comentario fijado con una pregunta.
```

## 4. Estándares de grabación
- Resolución 1080p o más; la pantalla al 125–150 % de zoom para que se lea en el celular.
- Modo oscuro, pestañas y notificaciones cerradas, y **una cuenta de demo sin datos personales**.
- Grabar por bloques (un paso = una toma) para editar más fácil.
- Voz: micrófono a 10–15 cm, habitación con textiles; grabar 10 s de silencio para el perfil de ruido.

## 5. Estándares de edición
- Primer fotograma = resultado.
- Cortar todos los silencios de más de 0,4 s y acelerar las esperas de carga a 4–8x.
- Zoom al cursor en cada clic importante.
- Texto en pantalla con los números, el "Paso N de M" y los prompts clave.
- Música baja (−25 dB) y sin derechos de autor (biblioteca de audio de YouTube).
- Pantalla final de 20 s, que empieza mientras todavía se habla.

## 6. Reutilización: 1 video → 10 piezas

| Pieza | Plataforma | Cómo |
|---|---|---|
| 3 Shorts | YouTube Shorts | Momentos de "aha", en vertical 9:16 y con subtítulos grandes |
| Los mismos 3 | TikTok y Reels de Instagram | **Sin marca de agua** de otra plataforma; texto nativo de cada app |
| 1 carrusel | Instagram y LinkedIn | Los pasos del tutorial como slides (Canva) |
| 1 publicación de texto | LinkedIn | "Cronometré X. Pasé de 2 h a 12 min. Así:" + 5 pasos |
| 1 email | Newsletter | El prompt de la semana + el link al video |
| 1 publicación de Comunidad | YouTube | Encuesta sobre el siguiente tema |

## 7. Checklists de control de calidad

**Antes de grabar**
- [ ] El empaque (título y miniatura) está elegido y testeado contra competidores
- [ ] La demo se hizo de verdad, el tiempo está medido y los resultados están anotados
- [ ] Todo dato o afirmación sobre herramientas está verificado hoy
- [ ] Los archivos de demo no tienen datos personales ni confidenciales

**Antes de publicar**
- [ ] El hook muestra el resultado en el segundo 0–3
- [ ] La promesa del título se cumple antes del 70 % del video
- [ ] Audio sin ruido, volumen normalizado (~−14 LUFS)
- [ ] El texto se lee en el celular (verificado en un teléfono)
- [ ] Subtítulos revisados (nombres de herramientas bien escritos)
- [ ] Descripción con palabra clave, capítulos, link al lead magnet y aviso de afiliados si hay links
- [ ] Pantalla final y tarjeta a mitad de video configuradas
- [ ] 3 miniaturas cargadas en "Probar y comparar"
- [ ] La opción de contenido alterado/sintético está marcada si corresponde
- [ ] Comentario fijado listo

**Después de publicar (48 h)**
- [ ] Todos los comentarios respondidos
- [ ] CTR y retención revisados ([08](08-analitica.md))
- [ ] Shorts programados para los días siguientes
