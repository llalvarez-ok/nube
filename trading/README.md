# RIC Delta Divergencias EA (MetaTrader 5)

Expert Advisor que opera las divergencias precio/CVD del indicador **RIC Delta Pro** en M1, M3, M5 y M15.

## Reglas
- Divergencia **alcista** confirmada en una temporalidad → compra de esa temporalidad.
- Divergencia **bajista** confirmada → venta de esa temporalidad.
- La operación se cierra con la **primera divergencia contraria de la misma temporalidad**. Con `Al cerrar... abrir en el nuevo sentido` activado (por defecto) la posición se da vuelta; si no, queda sin posición hasta la próxima divergencia.
- Una divergencia en el mismo sentido de la posición abierta se ignora (no se piramida).
- Cada temporalidad es independiente: las señales de M1 solo tocan la operación de M1, y así con las demás.

## Réplica del indicador
- Pivotes con `Longitud de pivote` (5 por defecto) a cada lado; la señal se confirma `longitud` velas después del pivote, igual que en TradingView (no repinta).
- Delta: en M3/M5/M15 se clasifican las velas M1 internas como compradoras/vendedoras (misma regla del indicador); en M1 se usa la estimación por posición del cierre, que es lo que hace el indicador en un gráfico de 1 minuto.
- La divergencia compara el CVD continuo (sin reinicio diario), como el indicador.
- Volumen: real si el símbolo lo tiene, si no volumen de ticks (configurable).
- Empates en pivotes: la vela central tiene que ser estrictamente mayor que las de la izquierda y mayor o igual que las de la derecha (criterio de `ta.pivothigh`). Puede haber diferencias mínimas con TradingView por el feed de cada broker.

## Cuentas y activos
- **Hedging**: una posición por temporalidad, con magic `base + minutos` (2026101, 2026103, 2026105, 2026115).
- **Netting / exchange**: el EA lleva una posición virtual por temporalidad y ajusta la posición neta del símbolo con la diferencia. Las virtuales se guardan en variables globales del terminal para sobrevivir a reinicios. Si la posición se cierra por fuera del EA, las virtuales vuelven a cero.
- Lotes ajustados al mínimo, máximo y paso de cada símbolo; modo de llenado detectado del símbolo; respeta símbolos “solo compras”, “solo ventas” o “solo cierre”; filtro opcional de spread y control de margen libre.

## Instalación
1. Copiar `RIC_Delta_Divergencias_EA.mq5` en `MQL5/Experts/` (Archivo → Abrir carpeta de datos).
2. Compilar en MetaEditor (F7).
3. Arrastrar al gráfico del activo (cualquier temporalidad; el EA lee M1/M3/M5/M15 por su cuenta) y activar Trading algorítmico.
4. Probar primero en el Probador de estrategias con “Cada tick basado en ticks reales” y en cuenta demo.

No hay stop loss ni take profit: la salida es solo por divergencia contraria. No es asesoramiento financiero.
