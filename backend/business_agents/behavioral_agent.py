# business_agents/behavioral_agent.py

from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class BehavioralAnalysisResult(BaseModel):
    """
    Define la estructura del informe generado por el BehavioralAgent.
    """
    patron_de_pago: str = Field(description="Clasificación del patrón de pago histórico: 'Puntual', 'Con Retrasos Leves', 'Moroso'.")
    fiabilidad_referencias: str = Field(description="Evaluación de la fortaleza y fiabilidad de las referencias comerciales: 'Alta', 'Media', 'Baja'.")
    riesgo_comportamental: str = Field(description="Nivel de riesgo general basado en el comportamiento: 'Bajo', 'Moderado', 'Alto'.")
    resumen_ejecutivo: str = Field(description="Un párrafo que resume la fiabilidad y el comportamiento general de la empresa.")

def analyze_behavior(api_key: str, behavioral_data_text: str) -> BehavioralAnalysisResult:
    """
    Analiza un texto con referencias e historial de pagos y extrae un análisis de comportamiento.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=api_key)
    parser = PydanticOutputParser(pydantic_object=BehavioralAnalysisResult)

    prompt_template = """
    Eres un Analista de Crédito especializado en la evaluación de riesgos no financieros y comportamentales.
    Tu tarea es analizar el siguiente texto, que contiene referencias comerciales y un historial de pagos simulado para una PYME.

    **TEXTO A ANALIZAR (REFERENCIAS E HISTORIAL):**
    {behavioral_data_text}

    **TU ANÁLISIS:**
    Lee el texto y evalúa la fiabilidad y consistencia de la empresa. Debes realizar las siguientes tareas:
    1.  **Patrón de Pago:** Basado en el historial, clasifica su comportamiento de pago como 'Puntual', 'Con Retrasos Leves', o 'Moroso'.
    2.  **Fiabilidad de Referencias:** Evalúa la calidad de las referencias. ¿Son fuertes y positivas? Clasifícalas como 'Alta', 'Media', o 'Baja'.
    3.  **Riesgo Comportamental:** Basado en los dos puntos anteriores, determina un nivel de riesgo general ('Bajo', 'Moderado', 'Alto').
    4.  **Resumen Ejecutivo:** Escribe un párrafo final que consolide tu evaluación sobre el carácter y la fiabilidad de la empresa como socio comercial.

    **INSTRUCCIONES DE FORMATO:**
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | llm | parser
    
    analysis_result = chain.invoke({"behavioral_data_text": behavioral_data_text})
    
    return analysis_result

