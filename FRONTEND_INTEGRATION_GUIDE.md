# Guía de Integración Frontend - PymeRisk

## 🎯 Objetivo
Crear un frontend en Streamlit que permita a los usuarios subir 2 PDFs (balance financiero + información general) y obtener una evaluación de riesgo financiero usando el sistema de IA.

## 📋 Funcionalidades Implementadas

### 1. Interface de Usuario
- ✅ **Upload de PDFs**: Dos campos separados para balance financiero e información general
- ✅ **Extracción de Texto**: Automática usando PyPDF2
- ✅ **Formulario**: Campos para nombre de empresa y referencias comerciales
- ✅ **Validación**: Verificación de archivos requeridos

### 2. Integración con Backend
- ✅ **Azure Orchestrator**: Conexión directa con `agents/azure_orchestrator.py`
- ✅ **Procesamiento Asíncrono**: Manejo de evaluaciones que toman 15-20 segundos
- ✅ **Manejo de Errores**: Captura y visualización de errores

### 3. Visualización de Resultados
- ✅ **Métricas Principales**: Score, nivel de riesgo, tiempo de procesamiento
- ✅ **Análisis Detallado**: Tabs para financiero, reputacional, comportamental
- ✅ **Reporte Consolidado**: Recomendaciones y justificaciones
- ✅ **Información Técnica**: Detalles de la evaluación

## 🔧 Arquitectura Técnica

### Flujo de Datos
```
Usuario → Upload PDFs → Extracción Texto → CompanyData → AzureOrchestrator → EvaluationResult → Visualización
```

### Componentes Clave

#### 1. Extracción de PDFs
```python
def extract_text_from_pdf(pdf_file):
    """Extrae texto de un archivo PDF usando PyPDF2"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()
```

#### 2. Integración con Orquestador
```python
async def evaluate_company_risk(company_data):
    """Evalúa riesgo usando AzureOrchestrator"""
    from agents.azure_orchestrator import AzureOrchestrator, CompanyData
    
    orchestrator = AzureOrchestrator()
    await orchestrator.initialize()
    
    company_data_obj = CompanyData(**company_data)
    result = await orchestrator.evaluate_company_risk(company_data_obj)
    
    return result
```

#### 3. Mapeo de Datos
```python
# PDF Balance Financiero → financial_statements
# PDF Información General → social_media_data (usado como datos reputacionales)
# Formulario → commercial_references, payment_history
```

## 📊 Estructura de Resultados

### Métricas Principales
- **Score Final**: 0-1000 (mayor = menor riesgo)
- **Nivel de Riesgo**: BAJO (651-1000), MEDIO (401-650), ALTO (0-400)
- **Tiempo de Procesamiento**: Segundos
- **Confianza**: Porcentaje de confianza en la evaluación

### Análisis Detallado
1. **Financiero**: Solvencia, liquidez, rentabilidad
2. **Reputacional**: Sentimiento, temas positivos/negativos
3. **Comportamental**: Patrón de pago, fiabilidad de referencias
4. **Consolidado**: Recomendación crediticia, justificación

## 🚀 Deploy en Streamlit Cloud

### Configuración de Secrets
En Streamlit Cloud (Settings → Secrets):

```toml
AZURE_OPENAI_ENDPOINT = "https://hackathon-openai-svc.openai.azure.com/"
AZURE_OPENAI_API_KEY = "8IAJsfvdWCgfljKGu7zjv8oMz6EuCxxnoOCzaA1oZDhu493XbVwzJQQJ99BHACYeBjFXJ3w3AAABACOGWYRJ"
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"
AZURE_OPENAI_DEPLOYMENT = "gpt-4o"
AZURE_OPENAI_MODEL = "gpt-4o"
AZURE_OPENAI_DEPLOYMENT_MINI = "o3-mini"
AZURE_OPENAI_MODEL_MINI = "o3-mini"
```

### Archivos Necesarios
- ✅ `app.py` - Frontend principal
- ✅ `requirements.txt` - Con Streamlit y PyPDF2
- ✅ `.streamlit/config.toml` - Configuración de tema
- ✅ `.gitignore` - Excluye archivos sensibles

## 📝 Fuente de Datos Recomendada

**Superintendencia de Compañías del Ecuador**
https://appscvsgen.supercias.gob.ec/consultaCompanias/societario/busquedaCompanias.jsf

### Documentos Esperados:
1. **Balance Financiero**: Estados financieros, balance general, estado de resultados
2. **Información General**: Datos corporativos, actividad comercial, información legal

## 🔍 Testing y Validación

### Testing Local
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con credenciales reales

# 3. Ejecutar Streamlit
streamlit run app.py
```

### Testing de Componentes
```bash
# Test del orquestador
python test_azure_orchestrator.py

# Test de modelos Azure
python test_quick_dual_models.py

# Test de evaluación desde PDFs
python test_pdf_risk_evaluation.py
```

## 🎨 Características de UI/UX

### Diseño
- **Tema**: Azul corporativo (#1f77b4)
- **Layout**: Wide layout con sidebar
- **Componentes**: Métricas, tabs, expandables
- **Responsive**: Adaptable a diferentes tamaños

### Experiencia de Usuario
- **Guía Visual**: Instrucciones paso a paso
- **Feedback**: Indicadores de progreso y estado
- **Validación**: Mensajes de error claros
- **Resultados**: Visualización intuitiva y detallada

## 🔧 Troubleshooting

### Errores Comunes

#### 1. Error de Importación
```
ModuleNotFoundError: No module named 'agents'
```
**Solución**: Verificar que todos los archivos de `agents/` estén en el repositorio

#### 2. Error de Azure OpenAI
```
AuthenticationError: Invalid API key
```
**Solución**: Verificar configuración de secrets en Streamlit Cloud

#### 3. Error de PDF
```
PdfReadError: Could not read PDF
```
**Solución**: Verificar que el PDF no esté protegido con contraseña

### Logs y Debugging
- Streamlit muestra logs en tiempo real
- Usar `st.error()` para mostrar errores al usuario
- Usar `st.spinner()` para operaciones largas

## 📈 Métricas de Rendimiento

### Objetivos
- ⏱️ **Tiempo de Evaluación**: < 25 segundos
- 🎯 **Success Rate**: > 95%
- 💰 **Costo por Evaluación**: < $0.10 USD
- 📊 **Precisión**: Score consistente y explicable

### Monitoreo
- Logs de Streamlit Cloud
- Métricas de Azure OpenAI
- Tiempo de respuesta por evaluación
- Tasa de errores

## 🔄 Próximas Mejoras

### Funcionalidades Adicionales
- [ ] **Cache de Evaluaciones**: Evitar re-evaluaciones
- [ ] **Exportación de Reportes**: PDF/Word con resultados
- [ ] **Historial**: Base de datos de evaluaciones
- [ ] **Comparación**: Múltiples empresas lado a lado

### Optimizaciones
- [ ] **Extracción Mejorada**: OCR para PDFs escaneados
- [ ] **Validación de Formato**: Verificar estructura de documentos
- [ ] **Procesamiento Paralelo**: Múltiples evaluaciones simultáneas
- [ ] **API REST**: Endpoint para integraciones externas

## 🎯 Resultado Final

**URL de Deploy**: https://deploy-pymerisk-dhtmtkfxynnrd6wqzsztbu.streamlit.app/

**Características Implementadas**:
- ✅ Frontend completo y funcional
- ✅ Integración con sistema de IA
- ✅ Upload y procesamiento de PDFs
- ✅ Visualización de resultados detallada
- ✅ Deploy en Streamlit Cloud
- ✅ Configuración segura de credenciales