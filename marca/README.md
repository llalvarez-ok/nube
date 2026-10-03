# Identidad visual de Atajos IA

| Archivo | Uso | Medida |
|---|---|---|
| `banner.jpg` | Banner del canal (se aplica por API) | 2560×1440; el texto está dentro del área segura de 1546×423 |
| `logo.png` | **Foto de perfil**: se sube a mano porque la API no lo permite | 800×800 |
| `marca-de-agua.png` | Botón de suscripción sobre los videos (se aplica por API) | 150×150 |
| `*.html` | Fuentes editables, renderizadas con Chromium | — |

**Colores:** fondo #0F0F10 · acento #FFD400 · texto #FFFFFF.

## Lo que se configura por API (`herramientas/configurar_canal.py`)
- Banner
- Descripción del canal
- Palabras clave
- País (AR) e idioma (español)
- Marca de agua
- 5 playlists: "Empieza aquí" y una por cada pilar

## Lo que hay que hacer a mano en YouTube Studio (≈10 min)

En YouTube Studio:
1. **Foto de perfil:** Personalización → Imagen de marca → Foto → subir `logo.png`.
2. **Handle:** Personalización → Información básica → Handle → **@AtajosIAoficial** ✔ (hecho).
3. **Enlaces:** Personalización → Información básica → Vínculos → agregar la newsletter cuando exista.
4. **Valores de subida predeterminados:** Configuración → Valores de subida predeterminados:
   - Categoría: *Ciencia y tecnología*
   - Idioma del video: *Español*
   - Comentarios: *Retener los potencialmente inapropiados para revisión*
5. **Funciones avanzadas:** Configuración → Canal → Funciones aptas → verificar con el teléfono (habilita miniaturas personalizadas y videos de más de 15 min). Si "Funciones avanzadas" pide más historial, se habilita sola con el tiempo.
6. **Comunidad:** Configuración → Comunidad → agregar palabras bloqueadas (spam, links de estafas).
7. **Tráiler y secciones de la página de inicio:** cuando haya 3 o más videos (Personalización → Diseño).
