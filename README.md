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

- **IA**: OpenAI GPT-4o con proxy de seguridad
- **Framework**: LangChain + CrewAI
- **Backend**: FastAPI
- **Frontend**: Streamlit + Plotly
- **Datos**: JSON/SQLite (prototipo)
- **Seguridad**: Proxy de anonimización, validación multicapa

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