"""Framework de investigación de estrategias para la sesión de Tokio.

Todo se trabaja en UTC. Ninguna decisión usa información posterior al instante
en que se toma: los rangos se cierran con la última barra completa, los
indicadores se desplazan a su hora de cierre y las entradas se ejecutan en la
apertura de la barra siguiente a la vela de confirmación.
"""

__version__ = "0.1.0"
