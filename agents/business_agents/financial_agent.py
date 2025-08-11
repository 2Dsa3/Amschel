# business_agents/financial_agent.py

import json
from datetime import datetime
from pydantic import BaseModel, Field

# Import Azure OpenAI Service
from ..infrastructure_agents.services.azure_openai_service import AzureOpenAIService, OpenAIRequest

class FinancialAnalysisResult(BaseModel):
    """
    Define la estructura del informe generado por el FinancialAgent.
    """
    solvencia: str = Field(description="Análisis de la solvencia de la empresa (capacidad de pago a largo plazo).")
    liquidez: str = Field(description="Análisis de la liquidez (capacidad de pago a corto plazo).")
    rentabilidad: str = Field(description="Análisis de la rentabilidad (capacidad de generar ganancias).")
    tendencia_ventas: str = Field(description="Descripción de la tendencia de las ventas (crecimiento, estancamiento, decrecimiento).")
    resumen_ejecutivo: str = Field(description="Un párrafo final que resume la salud financiera general de la PYME.")
    success: bool = Field(description="Indica si el análisis fue exitoso", default=True)
    tokens_used: int = Field(description="Tokens utilizados en el análisis", default=0)

async def analyze_financial_document(azure_service: AzureOpenAIService, document_text: str) -> FinancialAnalysisResult:
    """
    Analiza el texto de un documento financiero y extrae un resumen estructurado usando Azure OpenAI.
    """
    try:
        if not document_text.strip():
            return FinancialAnalysisResult(
                solvencia="No hay datos financieros para analizar",
                liquidez="No hay datos financieros para analizar", 
                rentabilidad="No hay datos financieros para analizar",
                tendencia_ventas="No hay datos financieros para analizar",
                resumen_ejecutivo="No se proporcionaron datos financieros",
                success=False,
                tokens_used=0
            )

        prompt = f"""
        Eres un Analista Financiero Contable experto en Normas Internacionales de Información Financiera (NIIF) para PYMEs en Ecuador.
        Tu tarea es analizar el siguiente texto, extraído de un estado financiero del portal de la Superintendencia de Compañías (SCVS).

        **TEXTO DEL DOCUMENTO FINANCIERO:**
        {document_text}

        **TU ANÁLISIS:**
        Basándote únicamente en el texto proporcionado, realiza un análisis conciso de los siguientes puntos:
        1. **Solvencia:** Evalúa la capacidad de la empresa para cumplir con sus obligaciones a largo plazo.
        2. **Liquidez:** Evalúa la capacidad de la empresa para cubrir sus deudas a corto plazo.
        3. **Rentabilidad:** Evalúa la eficiencia de la empresa para generar beneficios.
        4. **Tendencia de Ventas:** Identifica y describe la evolución de los ingresos o ventas.
        5. **Resumen Ejecutivo:** Proporciona un párrafo final que consolide tu opinión profesional sobre la salud financiera general.

        Responde ÚNICAMENTE en formato JSON:
        {{
            "solvencia": "<análisis detallado>",
            "liquidez": "<análisis detallado>",
            "rentabilidad": "<análisis detallado>",
            "tendencia_ventas": "<análisis detallado>",
            "resumen_ejecutivo": "<resumen ejecutivo>"
        }}
        """

        request = OpenAIRequest(
            request_id=f"financial_analysis_{datetime.now().strftime('%H%M%S')}",
            user_id="system",
            agent_id="financial_agent",
            prompt=prompt,
            max_tokens=800,
            temperature=0.1,
            timestamp=datetime.now()
        )

        response = await azure_service.generate_completion(
            request,
            "You are a financial analyst expert. Provide accurate JSON response.",
            use_mini_model=False  # Use GPT-4o for complex financial analysis
        )

        # Parse JSON response
        try:
            result_data = json.loads(response.response_text)
            return FinancialAnalysisResult(
                solvencia=result_data.get("solvencia", "Análisis no disponible"),
                liquidez=result_data.get("liquidez", "Análisis no disponible"),
                rentabilidad=result_data.get("rentabilidad", "Análisis no disponible"),
                tendencia_ventas=result_data.get("tendencia_ventas", "Análisis no disponible"),
                resumen_ejecutivo=result_data.get("resumen_ejecutivo", "Resumen no disponible"),
                success=True,
                tokens_used=response.tokens_used
            )
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return FinancialAnalysisResult(
                solvencia="Análisis disponible en respuesta completa",
                liquidez="Análisis disponible en respuesta completa",
                rentabilidad="Análisis disponible en respuesta completa",
                tendencia_ventas="Análisis disponible en respuesta completa",
                resumen_ejecutivo=response.response_text[:200] + "...",
                success=True,
                tokens_used=response.tokens_used
            )

    except Exception as e:
        return FinancialAnalysisResult(
            solvencia=f"Error en análisis: {str(e)}",
            liquidez=f"Error en análisis: {str(e)}",
            rentabilidad=f"Error en análisis: {str(e)}",
            tendencia_ventas=f"Error en análisis: {str(e)}",
            resumen_ejecutivo=f"Error en análisis financiero: {str(e)}",
            success=False,
            tokens_used=0
        )

# Backward compatibility function
def analyze_financial_document_legacy(api_key: str, document_text: str) -> FinancialAnalysisResult:
    """
    Función de compatibilidad hacia atrás (no recomendada para uso nuevo)
    """
    return FinancialAnalysisResult(
        solvencia="Legacy function called - upgrade to use Azure OpenAI Service",
        liquidez="Legacy function called - upgrade to use Azure OpenAI Service",
        rentabilidad="Legacy function called - upgrade to use Azure OpenAI Service",
        tendencia_ventas="Legacy function called - upgrade to use Azure OpenAI Service",
        resumen_ejecutivo="Legacy function called - upgrade to use Azure OpenAI Service",
        success=False,
        tokens_used=0
    )