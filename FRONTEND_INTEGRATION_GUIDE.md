# 🌐 Guía de Integración Frontend - Sistema de Evaluación de Riesgo Financiero

## 📋 Resumen Ejecutivo

Este documento proporciona una guía completa para desarrollar e integrar un frontend web con el sistema multiagente de evaluación de riesgo financiero para PYMEs. El sistema backend utiliza Azure OpenAI Service y una arquitectura multiagente con flujo de seguridad completo.

## 🎯 Objetivo del Frontend

Crear una interfaz web intuitiva que permita a los usuarios:
1. **Subir PDF** de estados financieros de la Superintendencia de Compañías
2. **Ingresar URL** de red social para análisis reputacional
3. **Proporcionar referencias adicionales** en texto libre
4. **Visualizar resultados** de la evaluación de riesgo en tiempo real
5. **Descargar reportes** en formato PDF/Word

## 🏗️ Arquitectura Propuesta

```mermaid
graph TB
    subgraph "🌐 Frontend (React/Next.js)"
        UI[Interfaz de Usuario]
        UPLOAD[Componente Upload PDF]
        FORM[Formulario de Datos]
        RESULTS[Dashboard de Resultados]
        PROGRESS[Monitor de Progreso]
    end
    
    subgraph "🔗 API Layer (FastAPI)"
        API[FastAPI Backend]
        UPLOAD_EP[/upload-pdf]
        EVAL_EP[/evaluate-risk]
        STATUS_EP[/evaluation-status]
        RESULTS_EP[/evaluation-results]
    end
    
    subgraph "🤖 Sistema Multiagente"
        ORCH[AzureOrchestrator]
        SEC[Security Agents]
        BIZ[Business Agents]
        AUDIT[Audit Logger]
    end
    
    UI --> UPLOAD_EP
    UI --> EVAL_EP
    UI --> STATUS_EP
    UI --> RESULTS_EP
    
    API --> ORCH
    ORCH --> SEC
    ORCH --> BIZ
    ORCH --> AUDIT
```

## 🛠️ Stack Tecnológico Recomendado

### **Frontend**
- **Framework**: Next.js 14+ (React 18+)
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand o React Query
- **File Upload**: react-dropzone
- **Charts**: Chart.js o Recharts
- **PDF Generation**: jsPDF o Puppeteer
- **Real-time**: WebSockets o Server-Sent Events

### **Backend API**
- **Framework**: FastAPI (Python 3.11+)
- **File Processing**: PyPDF2 o pdfplumber
- **Authentication**: JWT tokens
- **CORS**: FastAPI CORS middleware
- **Validation**: Pydantic models

### **Deployment**
- **Frontend**: Vercel o Netlify
- **Backend**: Azure App Service o Docker
- **Database**: Azure SQL Database (ya configurada)
- **Storage**: Azure Blob Storage (para PDFs y reportes)

## 📁 Estructura del Proyecto Frontend

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── page.tsx           # Página principal
│   │   ├── evaluate/          # Página de evaluación
│   │   ├── results/           # Página de resultados
│   │   └── api/               # API routes (opcional)
│   ├── components/
│   │   ├── ui/                # Componentes base (shadcn/ui)
│   │   ├── forms/             # Formularios
│   │   │   ├── CompanyDataForm.tsx
│   │   │   ├── PDFUpload.tsx
│   │   │   └── SocialMediaInput.tsx
│   │   ├── results/           # Componentes de resultados
│   │   │   ├── RiskScoreCard.tsx
│   │   │   ├── AnalysisCharts.tsx
│   │   │   └── AuditTrail.tsx
│   │   └── layout/            # Layout components
│   ├── lib/
│   │   ├── api.ts             # Cliente API
│   │   ├── types.ts           # TypeScript types
│   │   └── utils.ts           # Utilidades
│   ├── hooks/                 # Custom hooks
│   └── stores/                # Estado global
├── public/
├── package.json
└── tailwind.config.js
```

## 🔌 API Backend - Endpoints Requeridos

### **1. Upload PDF Endpoint**
```python
# backend/api/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import PyPDF2
import io

router = APIRouter()

@router.post("/upload-pdf")
async def upload_financial_pdf(file: UploadFile = File(...)):
    """
    Procesa PDF de estados financieros de la Superintendencia
    """
    try:
        # Validar tipo de archivo
        if file.content_type != "application/pdf":
            raise HTTPException(400, "Solo se permiten archivos PDF")
        
        # Leer contenido del PDF
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        
        # Extraer texto de todas las páginas
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() + "\n"
        
        # Validar que contiene información financiera
        financial_keywords = ["activos", "pasivos", "patrimonio", "ingresos", "gastos"]
        if not any(keyword in extracted_text.lower() for keyword in financial_keywords):
            raise HTTPException(400, "El PDF no parece contener estados financieros válidos")
        
        return JSONResponse({
            "success": True,
            "extracted_text": extracted_text,
            "filename": file.filename,
            "pages": len(pdf_reader.pages),
            "message": "PDF procesado exitosamente"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error procesando PDF: {str(e)}")
```

### **2. Risk Evaluation Endpoint**
```python
# backend/api/evaluation.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
import asyncio
import uuid

router = APIRouter()

class EvaluationRequest(BaseModel):
    company_name: str
    company_id: Optional[str] = None
    financial_statements: str  # Texto extraído del PDF
    social_media_url: Optional[HttpUrl] = None
    additional_references: Optional[str] = None
    user_id: str = "web_user"

@router.post("/evaluate-risk")
async def start_risk_evaluation(request: EvaluationRequest):
    """
    Inicia evaluación de riesgo usando AzureOrchestrator
    """
    try:
        from agents.azure_orchestrator import AzureOrchestrator, CompanyData
        
        # Generar ID único si no se proporciona
        if not request.company_id:
            request.company_id = f"WEB_{uuid.uuid4().hex[:8].upper()}"
        
        # Procesar URL de red social (scraping básico)
        social_media_data = ""
        if request.social_media_url:
            social_media_data = await scrape_social_media(str(request.social_media_url))
        
        # Crear datos de la empresa
        company_data = CompanyData(
            company_id=request.company_id,
            company_name=request.company_name,
            financial_statements=request.financial_statements,
            social_media_data=social_media_data,
            commercial_references=request.additional_references or "Referencias proporcionadas por el usuario",
            payment_history="Historial no disponible - evaluación basada en datos proporcionados",
            metadata={
                "source": "web_frontend",
                "social_media_url": str(request.social_media_url) if request.social_media_url else None,
                "created_at": datetime.now().isoformat()
            }
        )
        
        # Inicializar orquestador
        orchestrator = AzureOrchestrator()
        await orchestrator.initialize()
        
        # Iniciar evaluación (asíncrona)
        evaluation_task = asyncio.create_task(
            orchestrator.evaluate_company_risk(company_data)
        )
        
        # Guardar tarea en memoria/cache para seguimiento
        evaluation_id = f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.company_id}"
        
        return JSONResponse({
            "success": True,
            "evaluation_id": evaluation_id,
            "company_id": request.company_id,
            "company_name": request.company_name,
            "status": "started",
            "message": "Evaluación iniciada exitosamente"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error iniciando evaluación: {str(e)}")

async def scrape_social_media(url: str) -> str:
    """
    Función básica para extraer datos de redes sociales
    NOTA: Implementar según la red social específica
    """
    # Implementación básica - expandir según necesidades
    return f"Datos de red social extraídos de: {url}"
```

### **3. Status Monitoring Endpoint**
```python
@router.get("/evaluation-status/{evaluation_id}")
async def get_evaluation_status(evaluation_id: str):
    """
    Obtiene el estado actual de una evaluación
    """
    try:
        # Implementar lógica de seguimiento de estado
        # Puede usar Redis, base de datos, o memoria compartida
        
        return JSONResponse({
            "evaluation_id": evaluation_id,
            "status": "in_progress",  # started, in_progress, completed, failed
            "current_phase": "business_analysis",
            "progress_percentage": 65,
            "estimated_completion": "2024-01-15T10:35:00Z",
            "phases_completed": [
                "security_supervision",
                "input_validation"
            ],
            "current_agent": "financial_agent"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo estado: {str(e)}")
```

### **4. Results Endpoint**
```python
@router.get("/evaluation-results/{evaluation_id}")
async def get_evaluation_results(evaluation_id: str):
    """
    Obtiene los resultados completos de una evaluación
    """
    try:
        # Obtener resultados del orquestador o base de datos
        
        return JSONResponse({
            "evaluation_id": evaluation_id,
            "company_name": "Empresa Ejemplo S.A.",
            "final_score": 850,
            "risk_level": "BAJO",
            "confidence": 0.92,
            "processing_time": 45.2,
            "timestamp": "2024-01-15T10:30:00Z",
            "analyses": {
                "financial": {
                    "solvencia": "Empresa con sólida capacidad de pago...",
                    "liquidez": "Liquidez adecuada para operaciones...",
                    "rentabilidad": "Rentabilidad sostenible...",
                    "tokens_used": 850
                },
                "reputational": {
                    "sentimiento_general": "Positivo",
                    "puntaje_sentimiento": 0.8,
                    "temas_positivos": ["Servicio al cliente", "Calidad"],
                    "tokens_used": 650
                },
                "behavioral": {
                    "patron_de_pago": "Puntual",
                    "fiabilidad_referencias": "Alta",
                    "riesgo_comportamental": "Bajo",
                    "tokens_used": 720
                }
            },
            "consolidated_report": {
                "justification": "La empresa presenta un perfil de riesgo bajo...",
                "contributing_factors": [
                    "Sólida posición financiera",
                    "Reputación positiva en el mercado",
                    "Historial de pagos confiable"
                ],
                "credit_recommendation": "Aprobar crédito con condiciones estándar"
            },
            "audit_trail": [
                {
                    "timestamp": "2024-01-15T10:25:00Z",
                    "event_type": "SECURITY_SUPERVISION",
                    "agent_id": "security_supervisor",
                    "success": True
                }
            ]
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo resultados: {str(e)}")
```

## 🎨 Componentes Frontend Clave

### **1. Formulario Principal**
```tsx
// src/components/forms/CompanyDataForm.tsx
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { PDFUpload } from './PDFUpload'
import { SocialMediaInput } from './SocialMediaInput'

interface CompanyDataFormProps {
  onSubmit: (data: CompanyFormData) => void
  isLoading: boolean
}

interface CompanyFormData {
  companyName: string
  financialPDF: File | null
  socialMediaUrl: string
  additionalReferences: string
}

export function CompanyDataForm({ onSubmit, isLoading }: CompanyDataFormProps) {
  const [formData, setFormData] = useState<CompanyFormData>({
    companyName: '',
    financialPDF: null,
    socialMediaUrl: '',
    additionalReferences: ''
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-2xl mx-auto">
      <div className="space-y-2">
        <label className="text-sm font-medium">Nombre de la Empresa *</label>
        <Input
          value={formData.companyName}
          onChange={(e) => setFormData(prev => ({ ...prev, companyName: e.target.value }))}
          placeholder="Ej: Innovaciones Andinas S.A."
          required
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">Estados Financieros (PDF) *</label>
        <PDFUpload
          onFileSelect={(file) => setFormData(prev => ({ ...prev, financialPDF: file }))}
          selectedFile={formData.financialPDF}
        />
        <p className="text-xs text-gray-500">
          Sube el PDF de estados financieros obtenido de la Superintendencia de Compañías
        </p>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">Red Social para Análisis</label>
        <SocialMediaInput
          value={formData.socialMediaUrl}
          onChange={(url) => setFormData(prev => ({ ...prev, socialMediaUrl: url }))}
        />
        <p className="text-xs text-gray-500">
          URL de Facebook, Instagram, Google Business, etc. (opcional)
        </p>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">Referencias Adicionales</label>
        <Textarea
          value={formData.additionalReferences}
          onChange={(e) => setFormData(prev => ({ ...prev, additionalReferences: e.target.value }))}
          placeholder="Información adicional sobre proveedores, clientes, historial comercial..."
          rows={4}
        />
      </div>

      <Button 
        type="submit" 
        disabled={isLoading || !formData.companyName || !formData.financialPDF}
        className="w-full"
      >
        {isLoading ? 'Procesando...' : 'Iniciar Evaluación de Riesgo'}
      </Button>
    </form>
  )
}
```

### **2. Componente de Upload PDF**
```tsx
// src/components/forms/PDFUpload.tsx
'use client'

import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface PDFUploadProps {
  onFileSelect: (file: File | null) => void
  selectedFile: File | null
}

export function PDFUpload({ onFileSelect, selectedFile }: PDFUploadProps) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0])
    }
  }, [onFileSelect])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024 // 10MB
  })

  const removeFile = () => {
    onFileSelect(null)
  }

  if (selectedFile) {
    return (
      <div className="flex items-center justify-between p-4 border rounded-lg bg-green-50">
        <div className="flex items-center space-x-3">
          <FileText className="h-8 w-8 text-green-600" />
          <div>
            <p className="font-medium text-green-800">{selectedFile.name}</p>
            <p className="text-sm text-green-600">
              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={removeFile}
          className="text-red-600 hover:text-red-800"
        >
          <X className="h-4 w-4" />
        </Button>
      </div>
    )
  }

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
        isDragActive 
          ? 'border-blue-400 bg-blue-50' 
          : 'border-gray-300 hover:border-gray-400'
      }`}
    >
      <input {...getInputProps()} />
      <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
      {isDragActive ? (
        <p className="text-blue-600">Suelta el archivo PDF aquí...</p>
      ) : (
        <div>
          <p className="text-gray-600 mb-2">
            Arrastra y suelta tu PDF aquí, o haz clic para seleccionar
          </p>
          <p className="text-sm text-gray-500">
            Solo archivos PDF, máximo 10MB
          </p>
        </div>
      )}
    </div>
  )
}
```

### **3. Dashboard de Resultados**
```tsx
// src/components/results/RiskScoreCard.tsx
'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'

interface RiskScoreCardProps {
  score: number
  riskLevel: string
  confidence: number
  companyName: string
}

export function RiskScoreCard({ score, riskLevel, confidence, companyName }: RiskScoreCardProps) {
  const getRiskColor = (level: string) => {
    switch (level.toUpperCase()) {
      case 'BAJO': return 'bg-green-500'
      case 'MEDIO': return 'bg-yellow-500'
      case 'ALTO': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getRiskBadgeVariant = (level: string) => {
    switch (level.toUpperCase()) {
      case 'BAJO': return 'default'
      case 'MEDIO': return 'secondary'
      case 'ALTO': return 'destructive'
      default: return 'outline'
    }
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Evaluación de Riesgo</span>
          <Badge variant={getRiskBadgeVariant(riskLevel)}>
            Riesgo {riskLevel}
          </Badge>
        </CardTitle>
        <p className="text-sm text-gray-600">{companyName}</p>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="text-center">
          <div className="text-6xl font-bold mb-2">
            {score}
            <span className="text-2xl text-gray-500">/1000</span>
          </div>
          <div className={`w-full h-4 rounded-full bg-gray-200 overflow-hidden`}>
            <div 
              className={`h-full transition-all duration-1000 ${getRiskColor(riskLevel)}`}
              style={{ width: `${(score / 1000) * 100}%` }}
            />
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Confianza del Análisis</span>
            <span>{(confidence * 100).toFixed(1)}%</span>
          </div>
          <Progress value={confidence * 100} className="h-2" />
        </div>

        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-green-600">
              {score >= 700 ? '✓' : score >= 400 ? '~' : '✗'}
            </div>
            <div className="text-xs text-gray-500">Crediticio</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-600">
              {confidence >= 0.8 ? '✓' : confidence >= 0.6 ? '~' : '✗'}
            </div>
            <div className="text-xs text-gray-500">Confianza</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-600">
              {riskLevel === 'BAJO' ? '✓' : riskLevel === 'MEDIO' ? '~' : '✗'}
            </div>
            <div className="text-xs text-gray-500">Riesgo</div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
```

### **4. Monitor de Progreso en Tiempo Real**
```tsx
// src/components/results/ProgressMonitor.tsx
'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { CheckCircle, Clock, AlertCircle } from 'lucide-react'

interface ProgressMonitorProps {
  evaluationId: string
  onComplete: (results: any) => void
}

interface EvaluationStatus {
  status: string
  current_phase: string
  progress_percentage: number
  phases_completed: string[]
  current_agent: string
}

const PHASES = [
  { id: 'security_supervision', name: 'Supervisión de Seguridad', icon: '🛡️' },
  { id: 'input_validation', name: 'Validación de Entrada', icon: '🔍' },
  { id: 'business_analysis', name: 'Análisis de Negocio', icon: '💼' },
  { id: 'output_sanitization', name: 'Sanitización de Salida', icon: '🧹' },
  { id: 'scoring_consolidation', name: 'Consolidación de Scoring', icon: '📊' },
  { id: 'audit_logging', name: 'Registro de Auditoría', icon: '📋' }
]

export function ProgressMonitor({ evaluationId, onComplete }: ProgressMonitorProps) {
  const [status, setStatus] = useState<EvaluationStatus | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const response = await fetch(`/api/evaluation-status/${evaluationId}`)
        const data = await response.json()
        
        setStatus(data)
        
        if (data.status === 'completed') {
          // Obtener resultados finales
          const resultsResponse = await fetch(`/api/evaluation-results/${evaluationId}`)
          const results = await resultsResponse.json()
          onComplete(results)
        } else if (data.status === 'failed') {
          setError('La evaluación falló. Por favor, intenta nuevamente.')
        }
      } catch (err) {
        setError('Error obteniendo estado de la evaluación')
      }
    }

    const interval = setInterval(pollStatus, 2000) // Poll cada 2 segundos
    pollStatus() // Llamada inicial

    return () => clearInterval(interval)
  }, [evaluationId, onComplete])

  if (error) {
    return (
      <Card className="w-full">
        <CardContent className="pt-6">
          <div className="flex items-center space-x-2 text-red-600">
            <AlertCircle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!status) {
    return (
      <Card className="w-full">
        <CardContent className="pt-6">
          <div className="flex items-center space-x-2">
            <Clock className="h-5 w-5 animate-spin" />
            <span>Iniciando evaluación...</span>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Progreso de Evaluación</span>
          <span className="text-sm font-normal">
            {status.progress_percentage}% completado
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <Progress value={status.progress_percentage} className="h-3" />
        
        <div className="space-y-3">
          {PHASES.map((phase) => {
            const isCompleted = status.phases_completed.includes(phase.id)
            const isCurrent = status.current_phase === phase.id
            
            return (
              <div
                key={phase.id}
                className={`flex items-center space-x-3 p-3 rounded-lg ${
                  isCompleted 
                    ? 'bg-green-50 text-green-800' 
                    : isCurrent 
                    ? 'bg-blue-50 text-blue-800' 
                    : 'bg-gray-50 text-gray-600'
                }`}
              >
                <span className="text-xl">{phase.icon}</span>
                <span className="flex-1">{phase.name}</span>
                {isCompleted && <CheckCircle className="h-5 w-5 text-green-600" />}
                {isCurrent && <Clock className="h-5 w-5 animate-spin text-blue-600" />}
              </div>
            )
          })}
        </div>

        {status.current_agent && (
          <div className="text-sm text-gray-600 text-center">
            Agente actual: <span className="font-medium">{status.current_agent}</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
```

## 🔄 Flujo de Usuario Completo

### **1. Página Principal**
```tsx
// src/app/page.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { CompanyDataForm } from '@/components/forms/CompanyDataForm'
import { Button } from '@/components/ui/button'

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleFormSubmit = async (formData: any) => {
    setIsLoading(true)
    
    try {
      // 1. Subir y procesar PDF
      const pdfFormData = new FormData()
      pdfFormData.append('file', formData.financialPDF)
      
      const pdfResponse = await fetch('/api/upload-pdf', {
        method: 'POST',
        body: pdfFormData
      })
      
      const pdfResult = await pdfResponse.json()
      
      if (!pdfResult.success) {
        throw new Error('Error procesando PDF')
      }

      // 2. Iniciar evaluación de riesgo
      const evaluationResponse = await fetch('/api/evaluate-risk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: formData.companyName,
          financial_statements: pdfResult.extracted_text,
          social_media_url: formData.socialMediaUrl,
          additional_references: formData.additionalReferences
        })
      })

      const evaluationResult = await evaluationResponse.json()
      
      if (!evaluationResult.success) {
        throw new Error('Error iniciando evaluación')
      }

      // 3. Redirigir a página de resultados
      router.push(`/results/${evaluationResult.evaluation_id}`)
      
    } catch (error) {
      console.error('Error:', error)
      alert('Error procesando la solicitud. Por favor, intenta nuevamente.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Evaluación de Riesgo Financiero
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Sistema inteligente de evaluación de riesgo para PYMEs usando 
            análisis multiagente con IA
          </p>
        </div>

        <CompanyDataForm 
          onSubmit={handleFormSubmit}
          isLoading={isLoading}
        />

        <div className="mt-12 text-center">
          <h2 className="text-2xl font-semibold mb-6">¿Cómo funciona?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-4xl mb-4">📄</div>
              <h3 className="font-semibold mb-2">1. Sube tu PDF</h3>
              <p className="text-gray-600">
                Estados financieros de la Superintendencia de Compañías
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="font-semibold mb-2">2. Análisis IA</h3>
              <p className="text-gray-600">
                Múltiples agentes analizan finanzas, reputación y comportamiento
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="font-semibold mb-2">3. Obtén Resultados</h3>
              <p className="text-gray-600">
                Score de riesgo, recomendaciones y reporte detallado
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

### **2. Página de Resultados**
```tsx
// src/app/results/[evaluationId]/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { ProgressMonitor } from '@/components/results/ProgressMonitor'
import { RiskScoreCard } from '@/components/results/RiskScoreCard'
import { AnalysisCharts } from '@/components/results/AnalysisCharts'
import { AuditTrail } from '@/components/results/AuditTrail'
import { Button } from '@/components/ui/button'

export default function ResultsPage() {
  const params = useParams()
  const evaluationId = params.evaluationId as string
  const [results, setResults] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  const handleEvaluationComplete = (evaluationResults: any) => {
    setResults(evaluationResults)
    setIsLoading(false)
  }

  const downloadReport = async () => {
    // Implementar descarga de reporte PDF
    const response = await fetch(`/api/generate-report/${evaluationId}`)
    const blob = await response.blob()
    
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `reporte-riesgo-${evaluationId}.pdf`
    a.click()
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold text-center mb-8">
              Procesando Evaluación
            </h1>
            <ProgressMonitor 
              evaluationId={evaluationId}
              onComplete={handleEvaluationComplete}
            />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold">Resultados de Evaluación</h1>
            <Button onClick={downloadReport}>
              Descargar Reporte PDF
            </Button>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-8">
              <RiskScoreCard 
                score={results.final_score}
                riskLevel={results.risk_level}
                confidence={results.confidence}
                companyName={results.company_name}
              />
              
              <AnalysisCharts analyses={results.analyses} />
            </div>

            <div className="space-y-8">
              <AuditTrail auditTrail={results.audit_trail} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

## 🚀 Pasos de Implementación

### **Fase 1: Setup Inicial (1-2 días)**
1. **Crear proyecto Next.js**
   ```bash
   npx create-next-app@latest risk-evaluation-frontend --typescript --tailwind --app
   cd risk-evaluation-frontend
   npm install @radix-ui/react-* react-dropzone chart.js react-chartjs-2
   ```

2. **Configurar shadcn/ui**
   ```bash
   npx shadcn-ui@latest init
   npx shadcn-ui@latest add button input textarea card progress badge
   ```

3. **Estructura de carpetas**
   - Crear estructura según el diagrama anterior
   - Configurar TypeScript types
   - Setup de utilidades y hooks

### **Fase 2: Backend API (2-3 días)**
1. **Crear FastAPI backend**
   ```bash
   pip install fastapi uvicorn python-multipart PyPDF2 pydantic
   ```

2. **Implementar endpoints**
   - Upload PDF endpoint
   - Risk evaluation endpoint
   - Status monitoring endpoint
   - Results endpoint

3. **Integración con AzureOrchestrator**
   - Importar y usar el sistema multiagente existente
   - Manejo de errores y logging
   - Configuración de CORS

### **Fase 3: Frontend Core (3-4 días)**
1. **Componentes de formulario**
   - CompanyDataForm
   - PDFUpload con drag & drop
   - SocialMediaInput con validación

2. **Componentes de resultados**
   - RiskScoreCard con animaciones
   - ProgressMonitor en tiempo real
   - AnalysisCharts con Chart.js

3. **Páginas principales**
   - Homepage con formulario
   - Results page con dashboard
   - Error handling y loading states

### **Fase 4: Funcionalidades Avanzadas (2-3 días)**
1. **Real-time updates**
   - WebSockets o Server-Sent Events
   - Progress monitoring
   - Status notifications

2. **Generación de reportes**
   - PDF generation con jsPDF
   - Plantillas de reportes
   - Download functionality

3. **Optimizaciones**
   - Caching de resultados
   - Lazy loading
   - Performance optimizations

### **Fase 5: Testing y Deployment (1-2 días)**
1. **Testing**
   - Unit tests con Jest
   - Integration tests
   - E2E tests con Playwright

2. **Deployment**
   - Frontend en Vercel/Netlify
   - Backend en Azure App Service
   - CI/CD pipeline

## 📊 Consideraciones Técnicas

### **Seguridad**
- **Validación de archivos**: Solo PDFs, límite de tamaño
- **Sanitización de inputs**: Validar URLs y texto
- **Rate limiting**: Prevenir abuso del sistema
- **HTTPS**: Todas las comunicaciones encriptadas

### **Performance**
- **Lazy loading**: Cargar componentes bajo demanda
- **Caching**: Cache de resultados y estados
- **Optimización de imágenes**: Next.js Image optimization
- **Bundle splitting**: Code splitting automático

### **UX/UI**
- **Responsive design**: Mobile-first approach
- **Loading states**: Indicadores de progreso claros
- **Error handling**: Mensajes de error informativos
- **Accessibility**: WCAG 2.1 compliance

### **Monitoring**
- **Analytics**: Google Analytics o similar
- **Error tracking**: Sentry para errores
- **Performance monitoring**: Web Vitals
- **User feedback**: Sistema de feedback integrado

## 🔧 Configuración de Desarrollo

### **Variables de Entorno**
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development

# Backend (.env)
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_DEPLOYMENT_MINI=o3-mini
```

### **Scripts de Desarrollo**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:e2e": "playwright test"
  }
}
```

## 📈 Métricas de Éxito

### **Técnicas**
- **Tiempo de carga**: < 3 segundos
- **Tiempo de evaluación**: < 60 segundos
- **Uptime**: > 99.5%
- **Error rate**: < 1%

### **Usuario**
- **Tasa de conversión**: > 80% completar evaluación
- **Satisfacción**: > 4.5/5 estrellas
- **Tiempo de uso**: < 5 minutos por evaluación
- **Retorno de usuarios**: > 60%

## 🎯 Roadmap Futuro

### **Versión 1.1**
- **Dashboard de historial**: Ver evaluaciones anteriores
- **Comparación de empresas**: Comparar múltiples evaluaciones
- **Alertas automáticas**: Notificaciones de cambios de riesgo

### **Versión 1.2**
- **API pública**: Para integraciones externas
- **Webhooks**: Notificaciones automáticas
- **Bulk processing**: Evaluación de múltiples empresas

### **Versión 2.0**
- **Machine learning**: Mejora continua del modelo
- **Análisis predictivo**: Predicción de riesgo futuro
- **Integración bancaria**: APIs de bancos ecuatorianos

---

## 📞 Contacto y Soporte

Para dudas sobre la implementación:
- **Documentación técnica**: Este documento
- **Código backend**: Sistema multiagente ya implementado
- **Testing**: Usar `test_final_integration.py` como referencia

**¡El sistema backend está listo y probado al 100%! Solo falta crear la interfaz web siguiendo esta guía.** 🚀