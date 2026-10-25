# Investigación · IATube, narrativa del momento y nichos que mejor pagan (25/10/2026)

> **Conclusión:** "IATube" no es una tecnología. Es un **método que se vende en cursos** (el más conocido es *IAtube* de Juano YT): canales sin rostro hechos con IA, de punta a punta. El método funciona cuando produce videos **con criterio propio** y falla cuando produce en masa: desde julio de 2025 YouTube desmonetiza canales enteros por **contenido inauténtico**. Este sistema toma lo que sirve de IATube (nicho con RPM alto, cadena de producción con IA, empaque agresivo) y le suma lo que los cursos no dan: agentes que se revisan entre sí, verificación de datos y controles de calidad medibles. Para Atajos IA el nicho actual sigue siendo el correcto. Si se abre un segundo canal, el candidato es **"software y finanzas para pymes y autónomos"** (sección 4).

Las cifras de este documento son estimaciones de fuentes de terceros (blogs de herramientas y agencias), que no coinciden entre sí. El agente `investigador-mercado` las reemplaza con datos reales del canal y de la API de YouTube cada mes.

## 1. Qué es IATube

| | |
|---|---|
| **Qué es** | Una familia de cursos en español ("IAtube" de Juano YT, "AI-Tube Automation" de Iván Sánchez, "Desafío IA-Tube" de Rodrigo Alfaro, "Automatizatube") que enseñan a montar canales *faceless* con IA. |
| **Qué enseñan** | 1) Elegir un nicho con RPM alto. 2) Copiar formatos que ya funcionan ("videos outlier"). 3) Guion con ChatGPT. 4) Voz sintética (ElevenLabs). 5) Imágenes o clips con IA o de stock. 6) Edición en CapCut. 7) Miniaturas y títulos llamativos. 8) Publicar seguido y escalar a varios canales. |
| **Precio** | Entre USD 10 y 99 según la página de venta: los precios y el temario cambian de un sitio a otro. |
| **Por qué "rinde"** | Los casos de éxito que se muestran suelen ser canales en inglés, de nichos con RPM alto (finanzas, historia, true crime), que encontraron un formato *outlier* antes que la competencia. Es sesgo de supervivencia: no se muestran los canales que no despegaron o que perdieron la monetización. |
| **Dónde falla** | Guiones genéricos, voz plana, imágenes repetidas y datos sin verificar. Eso es justo lo que la política de **contenido inauténtico** (antes "contenido repetitivo") castiga, y se evalúa **por canal**, no por video. En julio de 2026 YouTube lo dividió en 3 casos: contenido genérico, repetitivo o de plantilla; contenido perturbador; y personas creadas con IA que hablan de temas sensibles como salud o finanzas. |

**Qué tomamos de IATube y qué cambiamos:**

| IATube | Este sistema |
|---|---|
| Un prompt de ChatGPT escribe el guion | Un guionista escribe, 3 críticos lo atacan y un showrunner decide con una rúbrica medible |
| Copiar el video *outlier* | Detectar el *outlier* con datos (`investigar.py outliers`) y hacer **una versión mejor**, con un ángulo propio |
| Volumen: 1 video por día, varios canales | Calidad: 2 videos largos por semana + Shorts derivados, en un canal con identidad |
| Voz sintética sin aviso | Voz sintética de calidad (Chirp 3 HD), declarada en la descripción |
| Datos sin chequear | Agente `verificador` con fuentes obligatorias para cada cifra |
| Herramientas pagas (ElevenLabs, CapCut Pro, Midjourney) | Herramientas gratuitas (sección 5) |

## 2. La narrativa del momento (octubre de 2026)

1. **Calidad por sobre volumen.** La ola de "IA basura" de 2025 hizo que YouTube aplique la política de contenido inauténtico a canales completos. Los canales sin rostro que sobreviven tienen **un punto de vista**, investigación propia y producción cuidada.
2. **La educación es el formato mejor pagado entre los que crecen.** Un estudio de 144.370 canales (septiembre de 2026) ubica a la educación con el RPM mediano más alto de los 13 nichos medidos (USD 10,22) y con crecimiento por encima de la mediana. Los videos infantiles crecen más, pero pagan USD 0,33.
3. **IA aplicada > noticias de IA.** El público ya no busca "la IA que lo cambia todo". Busca **cómo hacer X con IA** en su trabajo. Es una consulta de búsqueda con intención clara y vida larga.
4. **Videopodcasts y formatos largos** suben en tiempo de visualización. Los **Shorts** funcionan como embudo hacia los videos largos, no como fuente de ingresos.
5. **Transparencia sobre la IA.** Declarar el contenido sintético realista es obligatorio, y YouTube afirma que declararlo no reduce el alcance ni la monetización.

## 3. Nichos por RPM (estimaciones en USD por cada 1.000 vistas)

Las tablas públicas son en inglés y para audiencia de EE. UU. **En español, el RPM real suele ser entre 3 y 5 veces menor**, salvo que la audiencia esté en EE. UU. o España. La columna "Español (est.)" aplica ese ajuste.

| Nicho | RPM en inglés | Español (est.) | Riesgo con IA | Comentario |
|---|---|---|---|---|
| Finanzas personales e inversión | 12–40 | 3–9 | **Alto** | Tema sensible ("tu dinero o tu vida"). Desde julio de 2026, las personas creadas con IA que dan consejo financiero no monetizan. |
| Software B2B / SaaS / reseñas de herramientas | 18–38 | 4–9 | Bajo | Anunciantes con presupuesto. Afiliados recurrentes del 20–40 %. |
| IA aplicada al trabajo | 8–25 | 3–7 | Bajo | **Nicho actual de Atajos IA.** Búsqueda con intención, encaja con el formato animado. |
| Bienes raíces (educación) | 12–30 | 2–6 | Medio | Muy local: lo que vale en México no vale en España. |
| Casos de negocio / historia de empresas | 6–22 | 2–5 | Medio | Necesita investigación seria y narrativa fuerte. |
| Educación general / ciencia | 5–12 | 1,5–4 | Medio | Crecimiento sostenido. Mucha competencia. |
| Historia / misterios / true crime | 4–10 | 1–3 | **Alto** | El formato más golpeado por la política de contenido inauténtico. |
| Música para dormir, ASMR, historias de terror | 0,5–2,5 | 0,2–1 | **Alto** | "Trampa de RPM": competencia masiva, pago bajo. |
| Infantil | 0,3–1 | 0,1–0,5 | Alto | Sin comentarios ni anuncios personalizados. |

Fuentes: [AIR Media-Tech](https://air.io/en/audience-growth/whos-growing-fastest-on-youtube-and-which-niches-are-hot-in-2025), [OutlierKit](https://outlierkit.com/resources/faceless-youtube-channels/), [Fliki](https://fliki.ai/blog/best-faceless-youtube-niches), [YouTubeNiches](https://youtubeniches.com/blog/best-faceless-youtube-niches-2026), [upgrowth](https://upgrowth.in/youtube-cpm-by-country-global-comparison-2026/), [TubeAnalytics](https://www.tubeanalytics.net/es/blog/youtube-cpm-by-country), [TechCrunch](https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/).

## 4. Recomendación

1. **Mantener Atajos IA en "IA práctica para el trabajo".** Es el nicho con mejor combinación de RPM, búsqueda, bajo riesgo con IA y encaje con videos animados producidos por agentes. El sistema ya está calibrado para él.
2. **Subir el RPM dentro del mismo canal** con temas que atraen anunciantes de software: "IA + Excel", "IA para contadores", "automatizar facturas", "CRM con IA para pymes". El agente `ideador` le da prioridad a estos temas (columna `rpm` en el puntaje de ideas).
3. **Segundo canal, solo después de los 1.000 suscriptores de Atajos IA:** *"Software y finanzas para pymes y autónomos"* (herramientas de facturación, impuestos de autónomos, comparativas de bancos digitales y ERPs). Tiene RPM de finanzas y software, pero sin dar consejo de inversión, que es lo que YouTube desmonetiza a las voces sintéticas. Se crea con la skill `/nuevo-canal`.
4. **Nichos descartados para un sistema automatizado:** historia/misterios, curiosidades, música para dormir, infantil y consejos de inversión con voz sintética.

## 5. Herramientas gratuitas del sistema

| Tarea | Herramienta | Costo | Límite gratuito |
|---|---|---|---|
| Agentes (investigación, guion, crítica, QC) | Claude Code: subagentes en `.claude/agents/` + rutinas programadas | Incluido en la suscripción | — |
| Datos de YouTube (búsqueda, outliers, tendencias por país) | YouTube Data API v3 | Gratis | 10.000 unidades/día (≈ 90 búsquedas) |
| Analítica propia | YouTube Analytics API | Gratis | — |
| Demanda de búsqueda | Autocompletado de YouTube (`suggestqueries`) | Gratis | Sin clave |
| Voz | Google Cloud TTS, voces Chirp 3 HD | Gratis | 1 millón de caracteres/mes (≈ 90 videos de 10 min) |
| Escenas y miniaturas | HTML + Chromium (Playwright) | Gratis | — |
| Edición, mezcla, normalización, QC | ffmpeg | Gratis | — |
| Imágenes de apoyo | Openverse (licencias CC, sin clave) y Pexels (clave gratuita) | Gratis | Pexels: 200 pedidos/hora |
| Música | Biblioteca de audio de YouTube (descarga manual, sin reclamos) | Gratis | — |
| Tipografía | Inter (OFL) | Gratis | — |
