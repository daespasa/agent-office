# Agent Office

Una oficina virtual en el navegador para organizar proyectos y agentes de IA con estética de juego de gestión isométrico.

**Estado: especificación y relevo para implementar. Todavía no existe una aplicación ejecutable.**

Cada proyecto ocupa una sala y los agentes aparecen como trabajadores. Al seleccionar uno se ve su tarea, actividad, permisos, errores, resultados y evidencias. El diseño se inspira en la claridad de Prison Architect y la oficina de Game Dev Tycoon, con gráficos originales.

El proyecto será generalista: proveedores de modelos y runtimes de agentes mediante adaptadores, endpoints locales o remotos, demostración sin credenciales y memoria Markdown compatible opcionalmente con Obsidian. Hermes será una integración posible, no un requisito. “Cualquier proveedor” significa una interfaz extensible y capacidades declaradas; no una promesa de compatibilidad automática con todas las APIs.

Para la siguiente IA: empieza por [AGENTS.md](AGENTS.md) y [IMPLEMENTATION.md](IMPLEMENTATION.md). La especificación principal está en inglés para facilitar contribuciones internacionales.

- [Diseño](design.md)
- [Requisitos](docs/product/requirements.md)
- [Arquitectura](docs/architecture.md)
- [Plan y criterios de entrega](docs/backlog.md)
- [Estado de continuidad](docs/ai-team/state.md)

Comprobación disponible hoy: `python3 scripts/check_spec.py`. No ejecuta una aplicación ni realiza llamadas a modelos.
