# Sistema de Evaluación Inteligente de Riesgo Financiero para PYMEs 🏦🤖

## 📋 Descripción del Proyecto

Sistema multiagente basado en IA que utiliza GPT-4o para evaluar el riesgo crediticio de pequeñas y medianas empresas (PYMEs) utilizando datos tradicionales y no tradicionales. Diseñado para instituciones financieras que requieren evaluaciones de riesgo precisas, seguras y auditables.

## 🏗️ Arquitectura

### 10 Agentes Especializados

#### 🔒 Agentes de Seguridad (4)
1. **SecuritySupervisor** - Monitoreo y detección de anomalías
2. **InputValidator** - Validación y sanitización de entradas
3. **OutputSanitizer** - Filtrado de salidas de modelos
4. **AuditLogger** - Registro completo para trazabilidad

#### 💰 Agentes de Negocio (3)
5. **FinancialAgent** - Análisis de estados financieros SCVS
6. **ReputationalAgent** - Análisis de reputación online
7. **BehavioralAgent** - Evaluación de patrones de comportamiento

#### 🏗️ Agentes de Infraestructura (3)
8. **MasterOrchestrator** - Coordinación central del flujo
9. **ScoringAgent** - Consolidación y scoring final (0-1000)
10. **ScenarioSimulator** - Simulaciones "qué pasaría si"

## 🚀 Stack Tecnológico

- **IA**: Azure OpenAI Service (GPT-4o) con proxy / sanitización
- **Orquestación Multi-Agente**: Azure AI Agent Service + Semantic Kernel + (LangChain / CrewAI evaluado)
- **Playground / Prototipado**: Azure AI Foundry Playground para pruebas rápidas de prompts y flujos
- **Grounding / Búsqueda**: Bing Search para contexto actualizado (riesgos geopolíticos / logísticos)
- **Backend API**: FastAPI (servicios REST) + futuras extensiones async
- **Frontend / Consola Dev**: React (Next.js) + Tailwind CSS + React Simple Maps + Plotly (UI producción); Streamlit (monitor y debugging interno)
- **Persistencia**: Azure SQL Database (estructurado) + Azure Blob Storage (artefactos y reportes) + JSON/SQLite (fase prototipo local)
- **Generación de Documentos**: Spire.Doc.Free (reportes Word programáticos)
- **Conectividad DB**: PyODBC (driver SQL Server / Azure SQL)
- **Seguridad**: Proxy de anonimización, validación multicapa, logging de auditoría

## 📁 Estructura del Proyecto

```
├── README.md                    # Este archivo
├── Planificacion/
│   ├── requeriments.md         # 10 requerimientos detallados con criterios de aceptación
│   ├── desing.md              # Arquitectura completa del sistema multiagente
│   └── tasks.md               # Plan de implementación hackathon 3 días
└── src/                       # Código fuente (por implementar)
```

## 📊 Características Principales

- **Scoring Alternativo**: Puntaje 0-1000 con explicabilidad completa
- **Datos Múltiples**: Estados financieros SCVS + redes sociales + referencias
- **Seguridad Robusta**: Proxy de seguridad, validación anti-prompt injection
- **Simulación de Escenarios**: Análisis "qué pasaría si" interactivo
- **Trazabilidad Completa**: Auditoría de todas las decisiones
- **Dashboard Intuitivo**: Visualizaciones claras para toma de decisiones

## 🎯 Objetivos del MVP (72 horas)

✅ 10 agentes funcionando  
✅ Demo impresionante con scoring explicable  
✅ Seguridad implementada  
✅ APIs OpenAI integradas  
✅ Casos de uso reales de PYMEs ecuatorianas  
✅ Simulación interactiva  

## 🔧 Instalación y Uso

```bash
# Clonar repositorio
git clone [URL_DEL_REPO]
cd sistema-riesgo-pymes

# Instalar dependencias
pip install -r requirements.txt

# Configurar API Key de OpenAI
export OPENAI_API_KEY="tu-api-key-aqui"

# Ejecutar aplicación
streamlit run src/app.py
```

## 📖 Documentación

- **[Requerimientos](Planificacion/requeriments.md)**: Especificaciones detalladas con criterios de aceptación
- **[Diseño](Planificacion/desing.md)**: Arquitectura multiagente y componentes técnicos  
- **[Plan de Implementación](Planificacion/tasks.md)**: Roadmap de desarrollo para hackathon

## 🏆 Casos de Uso

1. **Evaluación Rápida**: Scoring automático en < 5 minutos
2. **Análisis Profundo**: Factores explicativos del riesgo
3. **Simulación de Escenarios**: Impacto de cambios en variables clave
4. **Comparación Sectorial**: Benchmarks anónimos del sector
5. **Reportes de Auditoría**: Trazabilidad completa para reguladores

## 🛡️ Seguridad y Cumplimiento

- Proxy de seguridad para anonimización de datos
- Validación anti-prompt injection
- Logs encriptados para auditoría
- Control de acceso basado en roles (RBAC)
- Cumplimiento con regulaciones financieras

## 🤝 Contribución

Este proyecto está diseñado para hackathon. Para contribuir:

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

[Especificar licencia]

## 👥 Equipo

- **Especialista en Seguridad**: Agentes de seguridad y validación
- **Especialista Financiero**: Agentes de negocio y análisis de riesgo  
- **Especialista en Arquitectura**: Infraestructura y coordinación de agentes

---

**🚀 ¡Listo para hackear con agentes inteligentes!** 🤖💻

## 🛠️ Backend Technologies (Azure Ecosistema Detallado)

| Componente | Rol Principal | Uso en MVP |
|------------|---------------|-----------|
| Azure AI Agent Service | Orquestación modular de workflows multi-agente | Definir y ejecutar pipelines coordinados (scoring, simulación, auditoría) |
| Azure OpenAI Service | Modelos LLM (GPT-4o) para reasoning y generación | Análisis textual, resumen, explicación de factores de riesgo |
| Azure AI Foundry Playground | Entorno visual de pruebas | Iterar prompts y comportamientos antes de codificarlos |
| Semantic Kernel | Memoria contextual y plugins ligeros | Encapsular funciones de negocio (plugins financieros / reputación) |
| Grounding con Bing Search | Contexto actualizado externo | Obtener señales reputacionales y macro-riesgos recientes |
| Azure Blob Storage | Almacenamiento de artefactos | Guardar reportes, configuraciones de agentes, logs exportados |
| Azure SQL Database | Base relacional central | Tablas: empresas, estados financieros, métricas agregadas, históricos de scoring |
| FastAPI | Backend REST de alto desempeño | Endpoints: /score, /simulate, /reports, /health |
| Streamlit | Consola interna de monitoreo | Visualizar flujo de agentes, métricas, experimentos |
| Spire.Doc.Free | Generación de documentos | Creación de reportes auditables (DOCX/PDF) |
| PyODBC | Conector a SQL Server/Azure SQL | CRUD y consultas parametrizadas seguras |

### Flujo Conceptual
1. FastAPI recibe solicitud de evaluación -> registra intento en Azure SQL.
2. Orquestador (Azure AI Agent Service + Semantic Kernel) invoca agentes especializados.
3. Agentes financieros / reputacionales consultan datos internos (Azure SQL) y contexto externo (Bing Search).
4. Resultados parciales se consolidan; ScoringAgent genera puntaje y explicación.
5. Reporte se compone (Spire.Doc.Free) y se almacena en Blob Storage; metadatos en Azure SQL.
6. Streamlit muestra en tiempo real estados y logs depurados.

### Próximos Pasos Técnicos Recomendados
- Definir esquema inicial (DDL) de Azure SQL (empresas, estados_financieros, eventos_riesgo, scores, auditoria).
- Implementar capa DAL con PyODBC y funciones parametrizadas.
- Crear primer pipeline de agente en Semantic Kernel (plugin: calcular_ratios_financieros).
- Añadir servicio de grounding: wrapper Bing Search con caché temporal.
- Establecer convención de logging estructurado (JSON) para auditoría.
- Template de reporte DOCX (placeholders para métricas clave y explicaciones SHAP/similars).

> Esta sección formaliza la alineación del MVP con servicios Azure escalables manteniendo un camino claro desde prototipo local hasta producción regulada.

## 🎨 Frontend Technologies

| Tecnología | Rol | Uso en MVP |
|------------|-----|-----------|
| React | Librería UI declarativa | Componentes reutilizables (dashboards, formularios) |
| Next.js | Framework full‑stack React | Routing, SSR/SSG para SEO y performance, API routes auxiliares |
| Tailwind CSS | Framework CSS utility-first | Estilos consistentes rápidos, dark mode, responsive grid |
| React Simple Maps | Visualización geográfica | Mapas de riesgo geopolítico / exposición logística |
| Plotly | Gráficas interactivas | Series temporales, distribuciones, comparativos sectoriales |
| Streamlit (interno) | Panel operativo dev | Observabilidad de agentes y experimentación rápida |

### Estrategia de Capas UI
1. Capa Pública (Next.js): Portal para analistas y decisores (login, dashboard riesgo, simulaciones).
2. Capa Interna (Streamlit): Telemetría, tuning de prompts, inspección de logs.
3. Librería de Componentes: Botones, tablas, cards de métricas, semáforos de riesgo (Tailwind + design tokens).
4. Visual Data Layer: Hooks para fetching (SWR/React Query) sobre endpoints FastAPI.

### Roadmap Frontend Inicial
- Configurar monorepo o carpetas separadas (`/frontend` y `/backend`).
- Bootstrap Next.js + Tailwind + ESLint + Prettier.
- Definir theme (color scale riesgo: verde → amarillo → rojo + neutro gris).
- Implementar layout base (sidebar navegación, header métricas globales, área contenido).
- Componentes MVP: CardScore, TablaEmpresas, MapaExposicion, PanelSimulacion, TimelineEventos.
- Integrar autenticación (futuro: Azure AD / Entra ID) placeholder local.

### Endpoints Frontend ↔ Backend Planeados
- GET /score/{empresa_id}
- POST /score (nueva evaluación)
- POST /simulate (escenario hipotético)
- GET /reports/{id}
- GET /companies (lista + filtros)
- GET /risk/events (eventos reputacionales / externos)

### Métricas de UX Relevantes
- TTFD < 1s en dashboard principal (carga skeleton + fetch async)
- Interacciones gráficas < 100ms (optimizar memoization)
- Accesibilidad: Contraste AA y navegación teclado completa.

> Esta sección describe la capa de presentación escalable complementaria al stack backend ya definido.