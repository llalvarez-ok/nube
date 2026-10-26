# Ideas · Atajos IA (Excel + IA) · 25/10/2026

Las 30 primeras ideas del canal reorientado, **ordenadas por potencial**. El orden combina 5 criterios: demanda de búsqueda, que sea evergreen, RPM, que se luzca en el formato animado (hoja que se calcula, chat que responde, gráfico que se arma) y que deje una plantilla vendible. Las 5 primeras son las de lanzamiento.

**Pilares:** P1 = Excel + IA (50 %) · P2 = Flujos de oficina con IA (25 %) · P3 = IA para tu profesión (15 %) · P4 = Novedades de IA en Excel/Office (10 %). En esta lista: 15 de P1, 7 de P2, 5 de P3 y 3 de P4.

## Cómo leer la "evidencia"

- **No se pudieron medir volúmenes de búsqueda.** El 25/10/2026 el autocompletado de YouTube (`investigar.py sugerencias`) y Google quedaron bloqueados por el proxy de la sesión (403), y no había credenciales de la API de YouTube en el entorno. La evidencia es cualitativa: lo que devolvió WebSearch (guías en español, plantillas que ya se venden, documentación oficial). Lo que no se pudo comprobar dice **"sin verificar"**.
- **Pendiente antes de producir:** correr `python3 herramientas/investigar.py nicho "<palabra clave>" --region MX` (y ES) con las palabras clave de las 10 primeras, con las credenciales cargadas, y reordenar si alguna da demanda baja.
- **Competencia de referencia:** el canal en español con cifras públicas recientes es *Microsoft Excel a Todo Nivel* (~325 mil suscriptores, 2.173 videos, datos de julio de 2026, [developereducators.com](https://developereducators.com/channel/metn/)). Los grandes canales de Excel que enseñan IA (Kevin Stratvert, Teacher's Tech) están en inglés.

## Estado de las herramientas de IA (verificado el 25/10/2026)

| Herramienta | Costo | Qué hay que saber |
|---|---|---|
| **Excel para la web** | Gratis con cuenta Microsoft (5 GB de OneDrive) | Tiene fórmulas modernas (BUSCARX, FILTRAR, UNICOS), tablas dinámicas, gráficos y formato condicional. **No** ejecuta macros VBA, y Power Query y el modelo de datos completos piden Excel de escritorio ([WPS](https://www.wps.com/office-quick-solution/office-app-problems/why-excel-features-are-missing-in-the-free-web-version-and-how-to-fix-it/)) |
| **ChatGPT gratis** | Gratis | Escribe fórmulas y analiza archivos subidos (.xlsx, .csv, PDF), con límites de uso. Fuentes de terceros hablan de ~3 archivos por día y ~10 mensajes cada 5 h con el modelo principal; OpenAI no publica las cifras exactas ([TechRepublic](https://www.techrepublic.com/article/news-what-is-free-chatgpt-2026/), [Zenken](https://ai.zenken.co.jp/en/post/chatgpt-usage/)) |
| **Copilot gratis (copilot.microsoft.com)** | Gratis | Chat en el navegador: sirve para pedir fórmulas y pasos. **No está dentro de Excel** ([Lilach Bullock](https://www.lilachbullock.com/is-copilot-free/)) |
| **Copilot dentro de Excel** | **De pago** | Microsoft 365 Personal (USD 9,99/mes o 99,99/año) y Family (USD 12,99/mes o 129,99/año) incluyen 60 créditos de IA al mes **solo para el titular**; Microsoft 365 Premium (USD 19,99/mes o 199,99/año) da más uso. Exige guardar el archivo en OneDrive con autoguardado ([myexcelonline](https://www.myexcelonline.com/blog/is-copilot-in-excel-free/), [Office Watch](https://office-watch.com/2026/microsoft-365-plans-overview/)). En empresas, el Copilot Chat gratis **dejó de estar dentro de Word, Excel y PowerPoint el 15/04/2026** para usuarios sin licencia; la licencia Microsoft 365 Copilot cuesta ~USD 30 por usuario al mes ([Office Watch](https://office-watch.com/2026/microsoft-removes-copilot-chat-word-excel-powerpoint-april-2026/)). Office Watch reportó el 14/10/2026 que Copilot llegaría a todos los miembros de Family y Premium con un cupo compartido: **sin confirmar** en las páginas de Microsoft ([Office Watch](https://office-watch.com/2026/microsoft-365-family-copilot-sharing/)) |
| **Modo Agente de Excel** | **De pago** | Disponible con licencia Microsoft 365 Copilot y con Personal, Family y Premium. La documentación de Microsoft lo marcó en inglés y con restricciones en la UE y el Reino Unido; hay que confirmar el idioma español antes de grabar ([Microsoft Tech Community](https://techcommunity.microsoft.com/blog/excelblog/agent-mode-in-excel-is-now-generally-available-on-excel-for-web/4476092), [soporte de Microsoft](https://support.microsoft.com/office/a2fd6fe4-97ac-416b-b89a-22f4d1357c7a)) |
| **Función `=COPILOT()`** | Retirada | **Dejó de estar disponible el 14/09/2026** sin haber salido de la vista previa. No hacer videos sobre ella ([Windows Central](https://www.windowscentral.com/artificial-intelligence/microsoft-copilot/microsoft-is-ditching-the-copilot-function-in-excel-before-it-even-launches), [Office Watch](https://office-watch.com/2026/excel-copilot-function-removed/)) |
| **Claude para Excel** | **De pago** (Claude Pro, USD 20/mes o más) | Complemento disponible para Pro desde el 24/01/2026; disponibilidad general anunciada el 07/05/2026 según fuentes secundarias ([The Decoder](https://the-decoder.com/anthropic-activates-claudes-excel-integration-for-all-pro-subscribers), [Pillitteri](https://pasqualepillitteri.it/en/news/2143/claude-microsoft-365-outlook-beta)) |
| **Gemini en Google Sheets** | De pago para cuentas personales (Google One AI Premium) | Fuera del foco del canal; solo como comparación ([soporte de Google](https://support.google.com/docs/answer/14356410?hl=en-SC)) |

**Regla que sale de esta tabla:** los videos de lanzamiento usan **Excel para la web + ChatGPT gratis** (o Copilot gratis en el navegador). La IA da la fórmula o el plan, y la hoja se arma en Excel gratis. Copilot dentro de Excel aparece desde la idea 6, siempre con "de pago" en el primer minuto.

## Resumen

| # | Título | Palabra clave | Pilar | IA (costo) |
|---|---|---|---|---|
| 1 | Fórmulas de Excel con ChatGPT: 10 que te ahorran horas | fórmulas de excel con chatgpt | P1 | ChatGPT (gratis) |
| 2 | Dashboard en Excel con IA paso a paso (plantilla gratis) | dashboard en excel | P1 | ChatGPT (gratis) |
| 3 | BUSCARV y BUSCARX con IA: cruza dos listas sin errores | buscarv / buscarx | P1 | ChatGPT (gratis) |
| 4 | Tabla dinámica en Excel con IA: de cero a informe | tabla dinámica en excel | P1 | Copilot en el navegador o ChatGPT (gratis) |
| 5 | PDF a Excel con IA gratis: tablas sin copiar a mano | pdf a excel | P2 | ChatGPT (gratis, con límite diario) |
| 6 | Copilot en Excel: tutorial completo y lo que hace de verdad | copilot en excel | P1 | Copilot en Excel (pago) |
| 7 | Limpiar datos en Excel con IA: duplicados y errores fuera | limpiar datos en excel | P1 | ChatGPT (gratis) |
| 8 | Control de gastos en Excel con IA (plantilla automática) | control de gastos en excel | P1 | ChatGPT (gratis) |
| 9 | Inventario en Excel con IA: entradas, salidas y alertas | inventario en excel | P1 | ChatGPT (gratis) |
| 10 | Macros en Excel con ChatGPT sin saber programar | macros en excel | P1 | ChatGPT (gratis) + Excel de escritorio |
| 11 | Flujo de caja en Excel con IA para pymes | flujo de caja en excel | P3 | ChatGPT (gratis) |
| 12 | Gráficos en Excel con IA: del dato al gráfico que convence | gráficos en excel | P1 | ChatGPT (gratis) |
| 13 | Función SI en Excel con IA: anidadas sin enredarte | función si excel | P1 | ChatGPT (gratis) |
| 14 | Facturas PDF a Excel con IA: 30 facturas en una tabla | facturas pdf a excel | P2 | ChatGPT (gratis con límite; Plus para lotes) |
| 15 | Copilot en Excel vs ChatGPT gratis: ¿vale la pena pagar? | copilot excel vale la pena | P4 | Copilot (pago) vs ChatGPT (gratis) |
| 16 | Analizar datos en Excel con IA: 5 preguntas a tus ventas | analizar datos en excel | P1 | ChatGPT (gratis) |
| 17 | Formato condicional en Excel con IA: semáforos en 1 minuto | formato condicional excel | P1 | ChatGPT (gratis) |
| 18 | Conciliación bancaria en Excel con IA paso a paso | conciliación bancaria excel | P3 | ChatGPT (gratis) |
| 19 | Diagrama de Gantt en Excel con IA (plantilla gratis) | diagrama de gantt en excel | P2 | ChatGPT (gratis) |
| 20 | CRM en Excel con IA: seguimiento de clientes gratis | crm en excel | P3 | ChatGPT (gratis) |
| 21 | Excel a PowerPoint con IA: informe mensual en 10 minutos | excel a powerpoint | P2 | ChatGPT o Copilot en el navegador (gratis) |
| 22 | Errores de Excel (#N/A, #¡VALOR!): la IA te dice por qué | errores de excel | P1 | ChatGPT (gratis) |
| 23 | Combinar correspondencia con Excel e IA: 100 correos | combinar correspondencia | P2 | ChatGPT (gratis) + Word/Outlook de escritorio |
| 24 | Comisiones de ventas en Excel con IA: cálculo automático | comisiones de ventas excel | P3 | ChatGPT (gratis) |
| 25 | Power Query con IA: une 12 archivos de Excel en uno | power query | P1 | ChatGPT (gratis) + Excel de escritorio |
| 26 | Control de asistencia en Excel con IA para RR. HH. | control de asistencia excel | P3 | ChatGPT (gratis) |
| 27 | Modo Agente de Excel: lo probé con un caso real | modo agente excel | P4 | Copilot en Excel (pago) |
| 28 | Informe con IA: resume un Excel enorme en un correo | informe con ia | P2 | ChatGPT (gratis) |
| 29 | Claude en Excel vs Copilot: cuál conviene en 2026 | claude en excel | P4 | Claude Pro y Copilot (ambos pago) |
| 30 | Acta de reunión con IA: tareas y responsables en Excel | acta de reunión con ia | P2 | ChatGPT (gratis) |

---

## Ideas de lanzamiento (1–5)

### 1. Fórmulas de Excel con ChatGPT: 10 que te ahorran horas
- **Palabra clave:** fórmulas de excel con chatgpt (secundarias: chatgpt para excel, fórmulas de excel)
- **Pilar:** P1 · **IA:** ChatGPT gratis + Excel para la web gratis
- **Plantilla:** "10 fórmulas resueltas": un .xlsx con una pestaña por fórmula, el prompt exacto que la generó y un caso para practicar (**gratis** a cambio del email; es el lead magnet base del canal)
- **Por qué funciona:** es el puente exacto entre las dos búsquedas del canal y cada fórmula es un mini resultado visible (la celda se calcula en pantalla).
- **Evidencia:** hay guías escritas en español sobre el tema en medios grandes ([Xataka](https://www.xataka.com/basics/chatgpt-para-formulas-excel-como-usar-inteligencia-artificial-para-crearlas), [Digital Trends](https://es.digitaltrends.com/computadoras/chatgpt-para-escribir-formulas-de-excel/), [WWWhatsNew, 2024](https://wwwhatsnew.com/2024/01/22/manejo-de-formulas-de-excel-con-chatgpt-una-guia-practica/)), señal de demanda; muchas son de 2023–2024 (desactualizadas). WebSearch no devolvió videos de YouTube en español sobre fórmulas con ChatGPT: posible hueco, **sin verificar** en YouTube.

### 2. Dashboard en Excel con IA paso a paso (plantilla gratis)
- **Palabra clave:** dashboard en excel (secundarias: dashboard en excel con ia, panel de control excel)
- **Pilar:** P1 · **IA:** ChatGPT gratis (elige los KPIs y escribe las fórmulas) + Excel para la web gratis (tablas dinámicas, gráficos, segmentaciones)
- **Plantilla:** "Dashboard de ventas": versión de 1 mes **gratis**; versión de 12 meses con KPIs, metas y comparativo interanual **de pago** (entra en el pack de USD 9–19)
- **Por qué funciona:** es el video más vistoso del formato animado (los gráficos se construyen solos) y es la plantilla que mejor se vende en el nicho.
- **Evidencia:** guías en español actualizadas a 2026 sobre dashboards con IA ([G-Talent, "Dashboard Excel 2026: guía con IA y KPIs"](https://www.g-talent.net/blogs/microsoft/dashboard-excel-2026-guia-ia-kpis)) y herramientas pagas que venden justo esto ([ExcelDashboard AI](https://creati.ai/es/ai-tools/excel-dashboard-ai/)). Hay tutoriales de dashboards en YouTube, pero los que aparecieron en la búsqueda son en inglés y sin IA ([hlrnet](https://hlrnet.com/technoblog/inicio/?p=57266)). Volumen: **sin verificar**.
- **Seguimiento (26/10/2026, video03):** Excel tiene un modo dashboard nativo con Copilot (Insiders o de pago, [Kenji Explains, 16/10/2026](https://youtu.be/PxmvWAOksls), 173 mil vistas en 10 días). Verificar disponibilidad y precio en español; candidato a idea P4 ("Modo dashboard de Excel: lo probé") cuando salga de Insiders.

### 3. BUSCARV y BUSCARX con IA: cruza dos listas sin errores
- **Palabra clave:** buscarv / buscarx (secundarias: buscarv no funciona, cruzar dos listas en excel)
- **Pilar:** P1 · **IA:** ChatGPT gratis + Excel para la web gratis (BUSCARX está en Excel para la web y Microsoft 365; no en Excel 2016 o anteriores: avisarlo)
- **Plantilla:** "Cruce de listas": clientes vs. pagos con BUSCARV, BUSCARX y el control de "no encontrados" (**gratis**)
- **Por qué funciona:** BUSCARV es la función más conocida de Excel y el error #N/A es el dolor diario de Laura; la IA explica el porqué en lenguaje humano.
- **Evidencia:** las fuentes describen BUSCARV como la función de búsqueda más usada y a BUSCARX como su reemplazo ([DEV Community](https://dev.to/dusmamud/5-most-used-excel-functions-by-data-analysts-and-why-you-should-master-them-3lhf), [Syncfusion](https://www.syncfusion.com/web-stories/lookup-functions-in-excel)). Volumen en español y antigüedad de los videos: **sin verificar**.

### 4. Tabla dinámica en Excel con IA: de cero a informe
- **Palabra clave:** tabla dinámica en excel (secundarias: tablas dinámicas, cómo hacer una tabla dinámica)
- **Pilar:** P1 · **IA:** Copilot gratis en el navegador o ChatGPT gratis (qué preguntarle a los datos y cómo armar la tabla) + Excel para la web gratis
- **Plantilla:** "Informe de ventas con tabla dinámica": base de 500 filas ficticias + tabla y gráfico dinámico listos (**gratis**)
- **Por qué funciona:** es la función que más miedo da y el antes/después es brutal (500 filas → informe de una pantalla), ideal para animar arrastrando campos.
- **Evidencia:** guías en español que se siguen actualizando en 2026, señal de búsqueda evergreen ([G-Talent, tablas dinámicas 2026](https://www.g-talent.net/blogs/microsoft/tablas-dinamicas-excel-espana-2026-ejemplos-reportes), [Coderhouse](https://www.coderhouse.com/us/blog/paso-a-paso-como-crear-una-tabla-dinamica-en-excel), [Guru99](https://www.guru99.com/es/pivot-tables-in-excel-beginner-s-guide.html)), y herramientas de IA que la venden como caso de uso ([Kimi](https://www.kimi.com/es-419/resources/pivot-table-in-excel)). Volumen: **sin verificar**.

### 5. PDF a Excel con IA gratis: tablas sin copiar a mano
- **Palabra clave:** pdf a excel (secundarias: convertir pdf a excel, pdf a excel con ia)
- **Pilar:** P2 · **IA:** ChatGPT gratis (subir el PDF y pedir la tabla; límite diario de archivos en el plan gratis) o Copilot gratis en el navegador
- **Plantilla:** "Registro de facturas de proveedores" con validación de totales (**gratis**) + el prompt anti-errores ("si no ves el número, deja la celda vacía")
- **Por qué funciona:** dolor universal de oficina y transformación muy visual (PDF → tabla que se llena); el veredicto honesto (escaneos malos, números a revisar) da confianza.
- **Evidencia:** varias herramientas compiten por esta búsqueda con páginas en español ([Formula Bot](https://www.formulabot.com/es/convertir-pdf-a-excel), [Tenorshare](https://www.tenorshare.es/convertir-pdf/extraer-datos-de-pdf-a-excel-con-ia.html), [UPDF](https://updf.com/?p=323524)), señal de demanda comercial. Videos en español: **sin verificar**.

## Ideas 6–30

### 6. Copilot en Excel: tutorial completo y lo que hace de verdad
- **Palabra clave:** copilot en excel · **Pilar:** P1 · **IA:** Copilot dentro de Excel (**pago**: Microsoft 365 Personal/Family con 60 créditos al mes, o Premium)
- **Plantilla:** "30 prompts para Copilot en Excel" + libro de práctica (**gratis**)
- **Por qué funciona:** intención de compra de software (RPM alto) y mucha gente que ya paga Microsoft 365 no sabe que lo tiene.
- **Evidencia:** existen el tutorial de [DataCamp en español](https://www.datacamp.com/es/tutorial/excel-copilot-tutorial) y la [guía oficial de Microsoft](https://support.microsoft.com/es-es/Excel/copilot/get-started-with-copilot-in-excel); el tutorial en video más citado es en inglés (Teacher's Tech, [HubSite 365](https://www.hubsite365.com/en-ww/crm-pages/how-to-use-copilot-in-excel-the-complete-beginners-course.htm)). Videos en español: **sin verificar**.

### 7. Limpiar datos en Excel con IA: duplicados y errores fuera
- **Palabra clave:** limpiar datos en excel · **Pilar:** P1 · **IA:** ChatGPT gratis + Excel para la web (ESPACIOS, NOMPROPIO, Quitar duplicados, Relleno rápido)
- **Plantilla:** "Limpiador de bases": hoja con fórmulas de limpieza encadenadas (**gratis**)
- **Por qué funciona:** todo el que exporta de un sistema sufre esto; la animación "base sucia → base limpia" es muy satisfactoria.
- **Evidencia:** **sin verificar**.

### 8. Control de gastos en Excel con IA (plantilla automática)
- **Palabra clave:** control de gastos en excel · **Pilar:** P1 · **IA:** ChatGPT gratis (categoriza movimientos y escribe SUMAR.SI.CONJUNTO)
- **Plantilla:** "Control de gastos mensual" básico **gratis**; versión anual con gráficos y presupuesto **de pago** (USD 7–9)
- **Por qué funciona:** búsqueda masiva y estacional (enero), y es el producto de plantilla más probado del mercado. Es gestión, no consejo de inversión.
- **Evidencia:** empresas de software usan plantillas de control de gastos como imán de emails ([Factorial ES](https://factorial.es/plantillas/plantilla-control-gastos), [Factorial MX](https://factorial.mx/formatos/formato-control-gastos), [Quipu](https://getquipu.com/blog/plantilla-excel-de-control-de-compras/)) y se venden versiones de pago en Gumroad a USD 8 ([ejemplo](https://dannafinanzas.gumroad.com/l/riknws)).

### 9. Inventario en Excel con IA: entradas, salidas y alertas
- **Palabra clave:** inventario en excel · **Pilar:** P1 · **IA:** ChatGPT gratis
- **Plantilla:** "Inventario con alerta de stock mínimo" (**de pago**, USD 12–19; versión simple gratis)
- **Por qué funciona:** el público pyme (Martín) compra; la alerta que se pone roja cuando baja el stock es un gran momento visual.
- **Evidencia:** se venden plantillas de pago de "sistema automático de inventarios en Excel" con tutorial en YouTube ([Skillshare](https://www.skillshare.com/es/shop/digital-products/templates/949684684/sistema-automatico-de-inventarios-en-excel)) y hay guías en español de ClickUp y Perú Contable ([ClickUp](https://clickup.com/es-ES/blog/238124/como-gestionar-el-inventario-en-excel), [Perú Contable](https://www.perucontable.com/excelcontable/?p=1838)).

### 10. Macros en Excel con ChatGPT sin saber programar
- **Palabra clave:** macros en excel · **Pilar:** P1 · **IA:** ChatGPT gratis + **Excel de escritorio** (las macros VBA no corren en Excel para la web; avisarlo en los primeros 30 s)
- **Plantilla:** "3 macros listas" (.xlsm, **de pago** dentro del pack; con aviso de seguridad de macros)
- **Por qué funciona:** "automatizar sin programar" es aspiracional y el código que se escribe solo luce mucho animado.
- **Evidencia:** existe al menos un video en español con este ángulo ("El truco definitivo para automatizar Excel con ChatGPT", resumido en [Lilys](https://lilys.ai/es/notes/ai-automation-20251017/ultimate-excel-automation-chatgpt-no-coding-best-ai)), señal de que el tema rinde. Volumen: **sin verificar**.

### 11. Flujo de caja en Excel con IA para pymes
- **Palabra clave:** flujo de caja en excel · **Pilar:** P3 (contadores y pymes) · **IA:** ChatGPT gratis
- **Plantilla:** "Flujo de caja proyectado a 12 meses" (**de pago**, USD 12–19)
- **Por qué funciona:** RPM alto (finanzas de empresa, anunciantes B2B) y plantilla con precio probado.
- **Evidencia:** plantillas gratis como imán en software contable ([Quipu](https://getquipu.com/blog/plantilla-excel-de-estado-de-flujos-de-efectivo/), [Tiendanube](https://www.tiendanube.com/recursos/planillas/flujo-de-caja-plantilla-excel)) y una de pago para pymes chilenas a CLP 9.990 en [Payhip](https://payhip.com/b/ZDpQk).

### 12. Gráficos en Excel con IA: del dato al gráfico que convence
- **Palabra clave:** gráficos en excel · **Pilar:** P1 · **IA:** ChatGPT gratis (qué gráfico usar y por qué)
- **Plantilla:** "8 gráficos de gestión listos" (**gratis**)
- **Por qué funciona:** el formato animado brilla (barras que crecen) y deriva en Shorts fáciles.
- **Evidencia:** **sin verificar**.

### 13. Función SI en Excel con IA: anidadas sin enredarte
- **Palabra clave:** función si excel · **Pilar:** P1 · **IA:** ChatGPT gratis
- **Plantilla:** "Ejercicios de SI, SI.CONJUNTO y Y/O" (**gratis**)
- **Por qué funciona:** consulta básica y eterna; la IA traduce "si vende más de X y es cliente nuevo…" a fórmula.
- **Evidencia:** **sin verificar**.

### 14. Facturas PDF a Excel con IA: 30 facturas en una tabla
- **Palabra clave:** facturas pdf a excel · **Pilar:** P2 · **IA:** ChatGPT gratis para pocas facturas (límite diario de archivos); ChatGPT Plus o Claude Pro para lotes (pago, decirlo)
- **Plantilla:** "Libro de facturas recibidas" con control de duplicados (**de pago** dentro del pack)
- **Por qué funciona:** secuela directa de la idea 5 para el público administrativo-contable, con intención de compra.
- **Evidencia:** misma señal comercial que la idea 5. Específica de facturas: **sin verificar**.

### 15. Copilot en Excel vs ChatGPT gratis: ¿vale la pena pagar?
- **Palabra clave:** copilot excel vale la pena · **Pilar:** P4 · **IA:** Copilot en Excel (pago) vs ChatGPT (gratis), mismas 5 tareas cronometradas
- **Plantilla:** "Las 5 tareas de la prueba" para que el espectador repita la comparación (**gratis**)
- **Por qué funciona:** comparativa con intención de compra y debate en comentarios.
- **Evidencia:** la confusión es real y documentada: Copilot en Excel no es gratis y cambió de condiciones dos veces en 2026 ([myexcelonline](https://www.myexcelonline.com/blog/is-copilot-in-excel-free/), [Office Watch](https://office-watch.com/2026/microsoft-removes-copilot-chat-word-excel-powerpoint-april-2026/)).

### 16. Analizar datos en Excel con IA: 5 preguntas a tus ventas
- **Palabra clave:** analizar datos en excel · **Pilar:** P1 · **IA:** ChatGPT gratis (análisis de archivos subidos)
- **Plantilla:** "Base de ventas + 5 preguntas" (**gratis**)
- **Por qué funciona:** muestra a la IA respondiendo preguntas de negocio sobre una hoja; el veredicto honesto (verificar cada número) diferencia al canal.
- **Evidencia:** **sin verificar**.

### 17. Formato condicional en Excel con IA: semáforos en 1 minuto
- **Palabra clave:** formato condicional excel · **Pilar:** P1 · **IA:** ChatGPT gratis (reglas con fórmula)
- **Plantilla:** "Semáforo de vencimientos" (**gratis**)
- **Por qué funciona:** el cambio de color en cascada es el momento más "Short" del canal.
- **Evidencia:** **sin verificar**.

### 18. Conciliación bancaria en Excel con IA paso a paso
- **Palabra clave:** conciliación bancaria excel · **Pilar:** P3 (contadores) · **IA:** ChatGPT gratis
- **Plantilla:** "Conciliación bancaria con marcado automático" (**de pago**, USD 12–19)
- **Por qué funciona:** tarea mensual obligatoria de todo contador; RPM B2B alto.
- **Evidencia:** en español hay modelos en Excel y hasta un chatbot de conciliación para contadores ([Actualícese](https://actualicese.com/rutas/books/cierre-mensual-empresarial-soluciones-integrales-en-excel/page/1-modelos-de-conciliacion-bancaria-individual-y-conjunta-en-excel), [Actualícese, chatbots](https://actualicese.com/creacion-de-chatbots-que-te-sirvan-como-asistentes-contables/)); Microsoft tiene un agente de conciliación para Excel de pago ([Microsoft Learn](https://learn.microsoft.com/en-us/copilot/finance/reconcile/reconcile-overview)).

### 19. Diagrama de Gantt en Excel con IA (plantilla gratis)
- **Palabra clave:** diagrama de gantt en excel · **Pilar:** P2 · **IA:** ChatGPT gratis (de la lista de tareas al cronograma)
- **Plantilla:** "Gantt con formato condicional" (**gratis**)
- **Por qué funciona:** las barras que se pintan solas son ideales para animar; búsqueda evergreen de oficina.
- **Evidencia:** **sin verificar**.

### 20. CRM en Excel con IA: seguimiento de clientes gratis
- **Palabra clave:** crm en excel · **Pilar:** P3 (ventas) · **IA:** ChatGPT gratis
- **Plantilla:** "Mini CRM con embudo y próximos contactos" (**de pago**, USD 12–19)
- **Por qué funciona:** CPM de ventas/CRM alto y puente natural a afiliados de CRM.
- **Evidencia:** **sin verificar**.

### 21. Excel a PowerPoint con IA: informe mensual en 10 minutos
- **Palabra clave:** excel a powerpoint · **Pilar:** P2 · **IA:** ChatGPT gratis o Copilot gratis en el navegador (conclusiones y guion de slides) + PowerPoint para la web gratis
- **Plantilla:** "Informe mensual": .xlsx de datos + .pptx con gráficos vinculados (**de pago** dentro del pack)
- **Por qué funciona:** une los dos programas que Laura usa cada lunes.
- **Evidencia:** **sin verificar**.

### 22. Errores de Excel (#N/A, #¡VALOR!): la IA te dice por qué
- **Palabra clave:** errores de excel · **Pilar:** P1 · **IA:** ChatGPT gratis
- **Plantilla:** "Diccionario de errores" con causa y arreglo de cada uno (**gratis**)
- **Por qué funciona:** se busca en el momento del dolor; formato lista con 7 errores = 7 Shorts.
- **Evidencia:** guías en inglés ya muestran a ChatGPT explicando #VALUE! ([The Bricks](https://thebricks.com/resources/guide-how-to-learn-excel-formulas-using-chatgpt)). En español: **sin verificar**.

### 23. Combinar correspondencia con Excel e IA: 100 correos
- **Palabra clave:** combinar correspondencia · **Pilar:** P2 · **IA:** ChatGPT gratis (redacta el texto personalizado por columna) + Word y Outlook de escritorio
- **Plantilla:** "Base de contactos + plantilla de correo" (**gratis**)
- **Por qué funciona:** dolor clásico de oficina con un número concreto en el título.
- **Evidencia:** **sin verificar**.

### 24. Comisiones de ventas en Excel con IA: cálculo automático
- **Palabra clave:** comisiones de ventas excel · **Pilar:** P3 (ventas) · **IA:** ChatGPT gratis
- **Plantilla:** "Liquidador de comisiones por tramos" (**de pago**, USD 9–12)
- **Por qué funciona:** problema concreto de jefes de ventas y administrativos, con fórmulas por tramos que lucen animadas.
- **Evidencia:** **sin verificar**.

### 25. Power Query con IA: une 12 archivos de Excel en uno
- **Palabra clave:** power query · **Pilar:** P1 · **IA:** ChatGPT gratis + **Excel de escritorio** (Power Query completo no está en Excel para la web)
- **Plantilla:** "12 archivos mensuales de ejemplo + consulta lista" (**de pago** dentro del pack)
- **Por qué funciona:** público avanzado que compra curso; "12 archivos en 1 clic" es una promesa fuerte.
- **Evidencia:** **sin verificar**.

### 26. Control de asistencia en Excel con IA para RR. HH.
- **Palabra clave:** control de asistencia excel · **Pilar:** P3 (RR. HH.) · **IA:** ChatGPT gratis
- **Plantilla:** "Asistencia, horas y vacaciones" (**de pago**, USD 9–12). No calcula sueldos ni aplica leyes laborales de ningún país (regla 5)
- **Por qué funciona:** tarea mensual de RR. HH. y pymes con plantilla vendible.
- **Evidencia:** **sin verificar**.

### 27. Modo Agente de Excel: lo probé con un caso real
- **Palabra clave:** modo agente excel · **Pilar:** P4 · **IA:** Modo Agente de Copilot en Excel (**pago**)
- **Plantilla:** el libro del caso, antes y después del agente (**gratis**)
- **Por qué funciona:** novedad con poca cobertura en español y ángulo de prueba honesta.
- **Evidencia:** Microsoft lo marcó disponible en Excel para la web y escritorio ([Tech Community](https://techcommunity.microsoft.com/blog/excelblog/agent-mode-in-excel-is-now-generally-available-on-excel-for-web/4476092)); en español hay pocos textos ([DataCamp](https://www.datacamp.com/es/blog/agent-mode-in-excel), [Tecnoloblog](https://www.tecnoloblog.com/?p=3612)). **Confirmar soporte en español antes de grabar.**

### 28. Informe con IA: resume un Excel enorme en un correo
- **Palabra clave:** informe con ia · **Pilar:** P2 · **IA:** ChatGPT gratis
- **Plantilla:** "Plantilla de correo de reporte semanal" + prompt (**gratis**)
- **Por qué funciona:** el "qué le digo a mi jefe" de cada lunes, con un antes/después claro.
- **Evidencia:** **sin verificar**.

### 29. Claude en Excel vs Copilot: cuál conviene en 2026
- **Palabra clave:** claude en excel · **Pilar:** P4 · **IA:** Claude para Excel (Claude Pro, pago) vs Copilot en Excel (pago)
- **Plantilla:** "Las tareas de la prueba" (**gratis**)
- **Por qué funciona:** comparativa de software con intención de compra; casi sin cobertura en español.
- **Evidencia:** Claude para Excel abierto a Pro desde enero de 2026 ([The Decoder](https://the-decoder.com/anthropic-activates-claudes-excel-integration-for-all-pro-subscribers)). Videos en español: **sin verificar**.

### 30. Acta de reunión con IA: tareas y responsables en Excel
- **Palabra clave:** acta de reunión con ia · **Pilar:** P2 · **IA:** ChatGPT gratis (de la transcripción a una tabla de tareas)
- **Plantilla:** "Seguimiento de tareas de reuniones" (**gratis**)
- **Por qué funciona:** flujo de oficina cotidiano que termina en Excel y conecta con el pilar central.
- **Evidencia:** **sin verificar**.

---

**Ideas descartadas a propósito:** la función `=COPILOT()` (retirada el 14/09/2026), nómina "calculada" por país (riesgo legal, regla 5) y cualquier plantilla de inversiones o trading (regla 5).
