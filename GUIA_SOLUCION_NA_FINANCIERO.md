# 🏦 PymeRisk - Sistema de Evaluación de Riesgo Financiero para PYMEs

## 🎯 Solución Completa para Hackathon

### 📋 Resumen Ejecutivo
Sistema de inteligencia artificial que evalúa el riesgo crediticio de PYMEs ecuatorianas en 15-20 segundos, utilizando Azure OpenAI y análisis multidimensional de documentos financieros.

### 🚀 Deploy Funcional
**URL**: https://deploy-pymerisk-dhtmtkfxynnrd6wqzsztbu.streamlit.app/

---

## 🏗️ Arquitectura del Sistema

### Componentes Principales
1. **Frontend Streamlit** (`app.py`)
   - Interface web intuitiva
   - Upload de 2 PDFs (balance + info general)
   - Visualización de resultados en tiempo real

2. **Orquestador IA** (`agents/azure_orchestrator.py`)
   - Coordina evaluación completa
   - Usa GPT-4o + o3-mini para optimizar costos
   - Procesamiento paralelo de agentes

3. **Agentes Especializados**
   - **FinancialAgent**: Análisis de estados financieros
   - **ReputationalAgent**: Evaluación de reputación empresarial
   - **BehavioralAgent**: Análisis de comportamiento de pagos

### Flujo de Evaluación
```
PDFs → Extracción Texto → CompanyData → Azure OpenAI → Análisis Paralelo → Score Final
```

---

## 📊 Funcionalidades Clave

### Entrada de Datos
- ✅ **2 PDFs requeridos**:
  - Balance financiero (estados financieros)
  - Información general de la empresa
- ✅ **Fuente recomendada**: [Supercias Ecuador](https://appscvsgen.supercias.gob.ec/consultaCompanias/societario/busquedaCompanias.jsf)
- ✅ **Extracción automática** con PyPDF2

### Análisis IA
- 🤖 **Azure OpenAI Service**
- 🧠 **GPT-4o**: Análisis financiero complejo
- ⚡ **o3-mini**: Tareas rápidas (reputacional/comportamental)
- 🔄 **Procesamiento paralelo**: 3 agentes simultáneos

### Resultados
- 📈 **Score**: 0-1000 (mayor = menor riesgo)
- 🚦 **Clasificación**: ALTO (0-400), MEDIO (401-650), BAJO (651-1000)
- 📋 **Análisis detallado**: Financiero, reputacional, comportamental
- 💡 **Recomendaciones**: Crediticias con justificación

---

## 🔧 Implementación Técnica

### Stack Tecnológico
- **Frontend**: Streamlit
- **Backend**: Python + AsyncIO
- **IA**: Azure OpenAI (GPT-4o + o3-mini)
- **Deploy**: Streamlit Cloud
- **Procesamiento**: PyPDF2 para extracción

### Configuración Segura
```toml
# Secrets en Streamlit Cloud (NO en código)
AZURE_OPENAI_ENDPOINT = "https://hackathon-openai-svc.openai.azure.com/"
AZURE_OPENAI_API_KEY = "[CONFIGURADO EN CLOUD]"
AZURE_OPENAI_DEPLOYMENT = "gpt-4o"
AZURE_OPENAI_DEPLOYMENT_MINI = "o3-mini"
```

### Archivos Clave
- `app.py` - Frontend principal
- `agents/azure_orchestrator.py` - Orquestador IA
- `requirements.txt` - Dependencias
- `.streamlit/config.toml` - Configuración UI

---

## 📈 Métricas de Rendimiento

### Resultados Actuales
- ⏱️ **Tiempo promedio**: 15-20 segundos
- 🎯 **Success rate**: 100%
- 💰 **Tokens promedio**: 3,000-8,000 por evaluación
- 🔄 **Concurrencia**: Soporte para múltiples evaluaciones

### Optimización de Costos
- **Estrategia dual**: GPT-4o para análisis complejos, o3-mini para tareas simples
- **Distribución**: 60% financiero, 20% reputacional, 20% comportamental
- **Eficiencia**: ~$0.05-0.10 USD por evaluación

---

## 🎨 Experiencia de Usuario

### Interface Intuitiva
- 📱 **Responsive design**
- 🎨 **Tema corporativo** (azul #1f77b4)
- 📋 **Guía paso a paso**
- ⚡ **Feedback en tiempo real**

### Visualización de Resultados
- 📊 **Métricas principales** en dashboard
- 📑 **Tabs organizados** por tipo de análisis
- 🔍 **Detalles expandibles**
- 📈 **Gráficos y indicadores visuales**

---

## 🔒 Seguridad y Deploy

### Configuración Segura
- ✅ **Variables sensibles** en Streamlit Cloud secrets
- ✅ **Archivos .env** excluidos del repositorio
- ✅ **API keys** no expuestas en código
- ✅ **Validación de entrada** para prevenir ataques

### Deploy en Streamlit Cloud
1. **Repositorio**: Código sin credenciales
2. **Secrets**: Configurados en cloud dashboard
3. **Dependencies**: requirements.txt actualizado
4. **URL**: https://deploy-pymerisk-dhtmtkfxynnrd6wqzsztbu.streamlit.app/

---

## 🎯 Casos de Uso

### Sector Financiero
- **Bancos**: Evaluación rápida de créditos PYME
- **Cooperativas**: Análisis de riesgo para socios
- **Fintech**: Scoring automático para plataformas

### Empresas
- **Proveedores**: Evaluación de clientes potenciales
- **Inversionistas**: Due diligence automatizado
- **Consultores**: Herramienta de análisis financiero

---

## 📚 Documentación Completa

### Archivos de Referencia
- `SISTEMA_INFO.txt` - Información técnica completa
- `DEPLOY_GUIDE.md` - Guía de deploy paso a paso
- `FRONTEND_INTEGRATION_GUIDE.md` - Integración frontend-backend
- `DOCUMENTATION.md` - Documentación técnica detallada

### Testing y Validación
- `test_azure_orchestrator.py` - Test del orquestador
- `test_pdf_risk_evaluation.py` - Test con PDFs
- `main_integrated.py` - Demostración completa

---

## 🚀 Próximos Pasos

### Mejoras Inmediatas
- [ ] **OCR**: Para PDFs escaneados
- [ ] **Cache**: Evitar re-evaluaciones
- [ ] **API REST**: Para integraciones
- [ ] **Base de datos**: Historial de evaluaciones

### Escalabilidad
- [ ] **Múltiples idiomas**: Soporte internacional
- [ ] **Más fuentes**: Integración con APIs financieras
- [ ] **ML personalizado**: Modelos específicos por sector
- [ ] **Dashboard analytics**: Métricas agregadas

---

## 🏆 Valor Diferencial

### Innovación Técnica
- ✨ **IA Dual**: GPT-4o + o3-mini para optimización
- ⚡ **Velocidad**: 15-20 segundos vs horas manuales
- 🎯 **Precisión**: Análisis multidimensional
- 💰 **Costo-efectivo**: Optimización automática de tokens

### Impacto de Negocio
- 📈 **Escalabilidad**: Miles de evaluaciones diarias
- 🎯 **Precisión**: Reducción de riesgo crediticio
- ⏱️ **Eficiencia**: Automatización completa
- 🌍 **Accesibilidad**: Interface web simple

---

## 📞 Información de Contacto

**Sistema**: PymeRisk - Evaluación de Riesgo Financiero IA
**Deploy**: https://deploy-pymerisk-dhtmtkfxynnrd6wqzsztbu.streamlit.app/
**Tecnología**: Azure OpenAI + Streamlit
**Estado**: ✅ Funcional y desplegado

---

*Sistema desarrollado para hackathon con enfoque en PYMEs ecuatorianas, utilizando datos de Superintendencia de Compañías del Ecuador.*