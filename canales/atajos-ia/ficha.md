# Ficha del canal · Atajos IA

Todos los agentes leen esta ficha antes de trabajar. Es el resumen operativo; el detalle está en `youtube/`.

> **Reorientación del 25/10/2026 (decisión del creador):** el nicho se angostó de "IA práctica para el trabajo" a **IA aplicada a Excel y al trabajo de oficina**. Excel + IA es el pilar central. Banco de ideas vigente: [`ideas.md`](ideas.md). Monetización: [`productos.md`](productos.md). Donde `youtube/` contradiga esta ficha, manda la ficha.

| | |
|---|---|
| **Canal** | Atajos IA · @AtajosIAoficial · ID UC53Js7WmP8wd5OxJz8KxKJA |
| **Nicho** | IA aplicada a Excel y al trabajo de oficina, en español neutro con "tú" |
| **Promesa** | Excel con IA, sin humo: lo que te llevaba una tarde, en minutos, y con la plantilla lista para usar |
| **Formato** | Motion graphics producidos por código (motor v2: `herramientas/motor.py`, catálogo en `sistema/motor-v2.md`): réplica animada de una hoja de Excel con cursor, fórmulas que se escriben letra a letra, celdas que se calculan en cascada, panel de chat de IA que responde y gráficos que se construyen. Voz sintética Google Chirp 3 HD, declarada. Largos de 7–12 min (8+ min cuando el tema lo sostiene, para anuncios a mitad de video) + 3 Shorts verticales por video |
| **Firma** | 1) El resultado terminado (la hoja, el gráfico, el informe) en pantalla en los primeros 15 s, con el cronómetro "a mano vs. con IA". 2) **Cada video deja una plantilla .xlsx**: gratis a cambio del email (versión básica) o de pago (versión completa), siempre la misma que se ve en pantalla, con datos ficticios. 3) Veredicto honesto: cuándo la IA se equivoca y qué fórmula conviene escribir igual a mano |
| **Audiencia** | "Laura, 32": analista administrativa o asistente contable en Ciudad de México, Bogotá, Buenos Aires o Madrid. Vive en Excel: BUSCARV, filtros y copiar-pegar desde el sistema; las tablas dinámicas le dan miedo y los reportes del lunes le comen la mañana. Ya usa ChatGPT gratis "para preguntas", pero nunca le pidió una fórmula. Busca "cómo hacer X en Excel", "fórmula para…", "plantilla de…". "Martín, 41": dueño de pyme, contador independiente o jefe de ventas; lleva inventario, caja, comisiones o clientes en planillas improvisadas. Quiere que la planilla "se haga sola" sin pagar un ERP. Es el que compra la plantilla de pago y el curso |
| **Herramientas** | Por defecto, lo que la audiencia tiene **gratis**: Excel para la web (cuenta Microsoft gratuita) + ChatGPT gratis o Copilot gratis en el navegador (copilot.microsoft.com). Copilot dentro de Excel, el Modo Agente y Claude para Excel son de pago: se usan solo cuando el video trata de ellos, y el título o el primer minuto lo dicen. Macros VBA y Power Query completo exigen Excel de escritorio: se avisa al principio |
| **Mercados** | México, España, Colombia, Argentina, Chile, Perú y EE. UU. hispano. Más adelante, pistas de audio en inglés en los mejores videos |
| **Pilares** | Excel + IA (50 %) · Flujos de oficina con IA: correo, informes, PDFs, presentaciones (25 %) · IA para tu profesión: contadores, administrativos, RR. HH., ventas (15 %) · Novedades útiles de IA en Excel/Office (10 %) |
| **Temas de RPM alto** | Excel para contadores y finanzas de empresa (flujo de caja, conciliación, presupuesto), dashboards e informes de gestión, CRM y comisiones de ventas, inventario para pymes, Copilot y Microsoft 365 (intención de compra de software), PDFs y facturas a Excel |
| **Cadencia** | 2 videos largos por semana (martes y viernes) + 3 Shorts derivados de cada uno |
| **Marca** | Fondo #0F0F10, acento #FFD400, texto #FFFFFF, tipografía Inter. Verde Excel (#107C41) solo como color de la hoja animada, nunca como color de marca. Miniaturas: 1 protagonista (la hoja terminada o el gráfico), máximo 3 palabras |
| **Tono** | Directo, cercano, escéptico del hype. Nada de "¡esto lo cambia TODO!" ni "Excel ya no hace falta" |

## Reglas que no se negocian
1. **Ejemplos ficticios declarados.** Los documentos y planillas de demo son ficticios y se dice en el video y en la descripción. Nunca datos reales de clientes ni de empresas.
2. **Voz sintética declarada** en la descripción: "Narración con voz sintética. Guion, investigación y demos verificados por el equipo de Atajos IA".
3. **Cada cifra real lleva fuente** (en pantalla con `"fuente"` y en la descripción).
4. **Respuestas de IA reales.** Si una escena muestra "Respuesta de ChatGPT/Copilot/Claude", el texto tiene que haber salido de esa herramienta con ese prompt. Cada fórmula que aparece en pantalla se probó en Excel y da el resultado mostrado.
5. **Nada de consejos de inversión, salud o legales** presentados como recomendación personal. Las plantillas de finanzas son de gestión (registrar, sumar, proyectar), no de qué comprar. Nómina, impuestos y leyes laborales: solo con la advertencia de que dependen del país, y sin calcular por el espectador lo que le corresponde.
6. **Ningún video se parece a otro más de lo que se parecen dos capítulos de una misma serie.** Formato común sí, guion de plantilla no (política de contenido inauténtico). Cada video tiene su caso, su planilla y su error típico propios.
7. **Gratis o pago, dicho claro.** El título o los primeros 30 s aclaran si la herramienta de IA es gratuita o paga, y si hace falta Excel de escritorio. Precios y disponibilidad se verifican el día del guion (cambian seguido: la función `=COPILOT()` se retiró el 14/09/2026 y el Copilot gratis dentro de Excel desapareció para cuentas sin licencia el 15/04/2026).
8. **La plantilla funciona sola.** El .xlsx que se entrega abre en Excel para la web sin errores, no tiene macros (salvo que el video sea de macros, y entonces se avisa) ni vínculos externos.

## Documentos de referencia
- Ideas vigentes (30, ordenadas por potencial): `canales/atajos-ia/ideas.md`
- Escalera de productos: `canales/atajos-ia/productos.md`
- Nicho y audiencia (versión original, previa a la reorientación): `youtube/01-estudio-de-nicho.md`
- Ideas históricas: `youtube/02-100-ideas.md`
- Hooks, títulos, miniaturas y estructuras: `youtube/04-sistema-de-contenido.md`
- Algoritmo: `youtube/05-algoritmo-y-crecimiento.md`
- Monetización general: `youtube/07-monetizacion.md`
- Métricas: `youtube/08-analitica.md`
- Investigación de mercado vigente: `sistema/investigacion/`
- Aprendizajes de videos publicados: `canales/atajos-ia/aprendizajes.md`
