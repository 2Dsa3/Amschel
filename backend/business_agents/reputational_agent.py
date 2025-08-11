# business_agents/reputational_agent.py

from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# --- Contrato de Entrada ---
class ReputationAnalysisResult(BaseModel):
    """
    Define la estructura del informe generado por el ReputationalAgent.
    """
    sentimiento_general: str = Field(description="El sentimiento general detectado: 'Positivo', 'Neutral', o 'Negativo'.")
    puntaje_sentimiento: float = Field(description="Un puntaje numérico del sentimiento, de -1.0 (muy negativo) a 1.0 (muy positivo).", ge=-1.0, le=1.0)
    temas_positivos: List[str] = Field(description="Una lista de los 3 temas o palabras clave positivas más recurrentes.")
    temas_negativos: List[str] = Field(description="Una lista de los 3 temas o palabras clave negativas más recurrentes.")
    resumen_ejecutivo: str = Field(description="Un párrafo que resume la reputación online general de la empresa.")


def analyze_reputation(api_key: str, social_media_text: str) -> ReputationAnalysisResult:
    """
    Analiza un cuerpo de texto de redes sociales y extrae un análisis de reputación.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=api_key)
    parser = PydanticOutputParser(pydantic_object=ReputationAnalysisResult)

    prompt_template = """
    Eres un especialista en Marketing Digital y Reputación Online (ORM). Tu tarea es analizar un conjunto de comentarios y reseñas sobre una PYME.

    **TEXTO A ANALIZAR (COMENTARIOS Y RESEÑAS):**
    {social_media_text}

    **TU ANÁLISIS:**
    Lee y analiza todo el texto proporcionado para determinar la percepción pública de la empresa. Debes realizar las siguientes tareas:
    1.  **Sentimiento General:** Clasifica el sentimiento predominante en el texto como 'Positivo', 'Neutral' o 'Negativo'.
    2.  **Puntaje de Sentimiento:** Asigna un puntaje numérico preciso entre -1.0 y 1.0.
    3.  **Temas Positivos:** Identifica y lista hasta 3 temas o aspectos que los clientes elogian más.
    4.  **Temas Negativos:** Identifica y lista hasta 3 temas o problemas de los que los clientes se quejan más.
    5.  **Resumen Ejecutivo:** Escribe un párrafo final que resuma la reputación online general de la empresa y su posicionamiento en el mercado digital.

    **INSTRUCCIONES DE FORMATO:**
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | llm | parser
    
    analysis_result = chain.invoke({"social_media_text": social_media_text})
    
    return analysis_result