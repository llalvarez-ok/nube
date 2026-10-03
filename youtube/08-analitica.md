# 08 · Analítica y optimización del rendimiento

> Mirar pocas métricas, a horario fijo, y que cada revisión termine en **una decisión**. Sin decisión, la revisión no sirve.

## 1. Las métricas que importan (y dónde verlas en YouTube Studio)

| Métrica | Pregunta que responde | Dónde | Meta inicial |
|---|---|---|---|
| **Impresiones** | ¿YouTube me está mostrando? | Analytics → Alcance | Tendencia creciente semana a semana |
| **CTR de impresiones** | ¿El empaque convence? | Alcance | 4–8 % |
| **Vistas** | Resultado de lo anterior | General | — |
| **Duración media de visualización** | ¿Cuánto se ve? | Interacción | >3:30 en videos de 10 min |
| **% visto medio / curva de retención** | ¿Dónde se van? | Interacción → Retención | >40 %; >70 % en el segundo 30 |
| **Momentos clave** | Intro, caídas, picos, segmentos de alto rendimiento | Retención → Momentos clave | Caída de la intro <30 % |
| **Suscriptores por video** | ¿Qué formatos convierten? | Audiencia → Suscriptores por contenido | >1 sub cada 100 vistas |
| **Espectadores nuevos vs. recurrentes** | ¿Hay audiencia fiel? | Audiencia | Recurrentes >20 % al mes 3 |
| **Fuentes de tráfico** | ¿De dónde llegan? | Alcance → Fuentes | Búsqueda >40 % los primeros meses |
| **Términos de búsqueda** | ¿Qué escribe la gente? | Fuentes → Búsqueda de YouTube | Fuente de ideas nuevas |
| **Interacción** | Likes, comentarios, compartidos | Interacción | >4 % de likes/vistas |
| **RPM / ingresos** | ¿Cuánto rinde cada 1.000 vistas? | Ingresos (después del YPP) | Seguimiento por tema |
| **Clics a la plantilla / emails** | ¿Convierte fuera de YouTube? | Herramienta de newsletter / UTM | 1–3 % de las vistas |

## 2. Planilla de seguimiento
Usar [plantillas/seguimiento-videos.csv](plantillas/seguimiento-videos.csv): importarla en Google Sheets, con una fila por video, y completar a los **7 y a los 28 días**.

## 3. Diagnóstico de un video: árbol de decisión

```
¿Impresiones > 1.000 en 7 días?
├── NO → Problema de TEMA o de descubrimiento
│        ¿Hay búsqueda real del tema? (vidIQ/autocompletar)
│        ├── NO → Registrar y no repetir el tema
│        └── SÍ → Mejorar el título/la palabra clave y la descripción; enlazarlo desde un video que funcione
└── SÍ → ¿CTR ≥ 4 %?
         ├── NO → Problema de EMPAQUE → nueva miniatura (Probar y comparar) y título
         └── SÍ → ¿Retención a los 30 s ≥ 65 %?
                  ├── NO → Problema de HOOK → anotar la lección para el próximo guion; se puede recortar la intro en el editor de YouTube
                  └── SÍ → ¿% visto ≥ 40 %?
                           ├── NO → Problema de RITMO/PROMESA → mirar dónde cae la curva
                           └── SÍ → ✅ GANADOR → hacer secuela, variante, Shorts y playlist
```

## 4. Revisión semanal (lunes, 30 min)

**Plantilla:** [plantillas/revision-semanal.md](plantillas/revision-semanal.md)

1. **Números de la semana** (5 min): vistas, horas, subs, CTR medio y % visto medio contra la semana anterior.
2. **Los videos de los últimos 7 días** (10 min): pasar cada uno por el árbol de decisión.
3. **Shorts** (5 min): ¿alguno superó 3 veces la media? Entonces es candidato a video largo.
4. **Comentarios y términos de búsqueda** (5 min): sumar 3 ideas a la lista.
5. **Decisiones** (5 min): máximo 3 acciones concretas para la semana.

## 5. Revisión mensual (primer lunes, 90 min)

**Plantilla:** [plantillas/revision-mensual.md](plantillas/revision-mensual.md)

1. **Avance del YPP:** subs y horas contra la meta de la fase ([03 §2](03-sistema-operativo.md#2-objetivos-y-la-cuenta-que-los-sostiene)).
2. **Ranking por pilar:** vistas promedio, CTR, % visto y subs cada 100 vistas, por pilar y por formato. **Pasar un 10 % de la producción del peor pilar al mejor.**
3. **Patrones ganadores:** de los 3 mejores videos del mes, ¿qué tienen en común? (tipo de hook, fórmula de título, estilo de miniatura, duración, tema). Anotarlo en el "Libro de patrones".
4. **Rescate de videos flojos:** los 3 con buena retención y CTR bajo reciben un nuevo empaque.
5. **Curva de retención promedio:** ¿dónde cae siempre? Ajustar la estructura del guion.
6. **Audiencia:** países, edades, horarios. ¿Coincide con las personas de [01](01-estudio-de-nicho.md)?
7. **Ingresos y conversiones:** emails, clics de afiliado, RPM por tema.
8. **Plan del mes siguiente:** 8–9 videos elegidos con estos datos.

## 6. Libro de patrones (se completa con el tiempo)

| Patrón | Evidencia (videos) | Efecto | Aplicar en |
|---|---|---|---|
| *Ej.: un número en la miniatura sube el CTR* | #3, #9 | +1,8 pp de CTR | Todos los tutoriales |
| | | | |

## 7. Mejora de videos con bajo rendimiento
| Síntoma | Intervención | Esperar |
|---|---|---|
| CTR bajo | Nueva miniatura (A/B) y luego un título nuevo | 7 días entre cambios |
| Caída al principio | No se puede re-editar a fondo: recortar en el editor de YouTube y aplicar la lección al siguiente | — |
| Poca búsqueda | Título con la consulta exacta y un capítulo con la palabra clave | 14–28 días |
| Buen video, pocas vistas | Enlazarlo desde la pantalla final del video que mejor funciona y sumarlo a la playlist "Empieza aquí" | 14 días |
| Tema desactualizado | Versión nueva y tarjeta en el viejo hacia el nuevo | — |
