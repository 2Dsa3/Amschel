# business_agents/financial_agent.py

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class FinancialAnalysisResult(BaseModel):
    """
    Define la estructura del informe generado por el FinancialAgent.
    """
    solvencia: str = Field(description="Análisis de la solvencia de la empresa (capacidad de pago a largo plazo).")
    liquidez: str = Field(description="Análisis de la liquidez (capacidad de pago a corto plazo).")
    rentabilidad: str = Field(description="Análisis de la rentabilidad (capacidad de generar ganancias).")
    tendencia_ventas: str = Field(description="Descripción de la tendencia de las ventas (crecimiento, estancamiento, decrecimiento).")
    resumen_ejecutivo: str = Field(description="Un párrafo final que resume la salud financiera general de la PYME.")

def analyze_financial_document(api_key: str, document_text: str) -> FinancialAnalysisResult:
    """
    Analiza el texto de un documento financiero y extrae un resumen estructurado.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=api_key)
    parser = PydanticOutputParser(pydantic_object=FinancialAnalysisResult)

    prompt_template = """
    Eres un Analista Financiero Contable experto en Normas Internacionales de Información Financiera (NIIF) para PYMEs en Ecuador.
    Tu tarea es analizar el siguiente texto, extraído de un estado financiero del portal de la Superintendencia de Compañías (SCVS).

    **TEXTO DEL DOCUMENTO FINANCIERO:**
    {document_text}

    **TU ANÁLISIS:**
    Basándote únicamente en el texto proporcionado, realiza un análisis conciso de los siguientes puntos:
    1.  **Solvencia:** Evalúa la capacidad de la empresa para cumplir con sus obligaciones a largo plazo.
    2.  **Liquidez:** Evalúa la capacidad de la empresa para cubrir sus deudas a corto plazo.
    3.  **Rentabilidad:** Evalúa la eficiencia de la empresa para generar beneficios.
    4.  **Tendencia de Ventas:** Identifica y describe la evolución de los ingresos o ventas.
    5.  **Resumen Ejecutivo:** Proporciona un párrafo final que consolide tu opinión profesional sobre la salud financiera general.

    **INSTRUCCIONES DE FORMATO:**
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | llm | parser
    
    analysis_result = chain.invoke({"document_text": document_text})
    
    return analysis_result