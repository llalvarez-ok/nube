---
name: piloto-automatico
description: Ciclo autónomo semanal del canal (analítica → investigación → ideas → producción de los videos de la semana). Lo usan las rutinas programadas; también se puede invocar a mano con "piloto automático".
---
# Piloto automático

Este es el ciclo que corre la rutina programada. Todo lo que pueda hacerse sin el creador se hace; lo que no, se deja listo y se le avisa.

1. **Estado.** `python3 herramientas/pipeline.py estado`. Lee `canales/<canal>/ficha.md` y `aprendizajes.md`.
2. **Analítica (si hay videos publicados).** Agente `analista`: diagnóstico de los videos a 2, 7 y 28 días, revisión semanal en `youtube/revisiones/` (los lunes), reglas nuevas en aprendizajes.md.
3. **Banco de ideas.** Si hay menos de 4 ideas aprobadas sin producir: `investigar-nicho` en modo (b) y luego la etapa "idea" de `producir-video` para las 4 mejores oportunidades (cada una con su `pipeline.py nuevo`).
4. **Producción.** Corre `producir-video` sobre los videos de la semana (los 2 más avanzados que no estén `listo`) hasta `listo` o hasta una escalada.
5. **Cierre.** Commit y push de todo. Escribe `produccion/AAAA-MM-DD-resumen.md` con: videos listos para subir (con su publicacion.md), escaladas que necesitan decisión, métricas clave y pedidos al creador. Ese resumen es lo único que el creador tiene que leer.

Límites: no subas ni publiques videos por API (proyecto no auditado), no cambies la estrategia del canal sin el creador (eso se propone en el resumen), y respeta la cuota de la API de YouTube (máximo 8 consultas de `investigar.py nicho` por día).
