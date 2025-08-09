# security/supervisor.py

import json
from pydantic import BaseModel, Field
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
class SupervisionReport(BaseModel):
    """
    Define la estructura del informe generado por el agente supervisor.
    """
    anomaly_detected: bool = Field(description="Debe ser 'true' si se detectó cualquier patrón anómalo, de lo contrario 'false'.")
    confidence_score: float = Field(description="Confianza en la detección de la anomalía, de 0.0 (ninguna) a 1.0 (certeza total).", ge=0.0, le=1.0)
    summary: str = Field(description="Un resumen en lenguaje natural de los hallazgos. Si no hay anomalías, indicarlo.")
    recommended_action: Literal["Ninguna", "Revisión Manual Requerida", "Alerta de Seguridad Crítica"] = Field(description="La acción recomendada a seguir.")

def run_security_supervision(api_key: str, log_file_path: str = "audit.log") -> SupervisionReport:
    """
    Lee los últimos eventos del log de auditoría y los analiza en busca de patrones anómalos.
    """
    # 1. Leer los registros del archivo de log
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            # Leemos las últimas N líneas para no sobrecargar el análisis
            log_entries = f.readlines()[-100:] 
        
        if not log_entries:
            return SupervisionReport(anomaly_detected=False, confidence_score=0.0, summary="El archivo de log está vacío. No hay nada que analizar.", recommended_action="Ninguna")
            
        logs_as_string = "".join(log_entries)
    except FileNotFoundError:
        return SupervisionReport(anomaly_detected=True, confidence_score=1.0, summary="Error crítico: El archivo de log 'audit.log' no fue encontrado.", recommended_action="Alerta de Seguridad Crítica")

    # 2. Instanciar el LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=api_key)
    parser = PydanticOutputParser(pydantic_object=SupervisionReport)

    # 3. Diseñar el prompt de auditoría
    prompt_template = """
    Eres un Analista de Ciberseguridad de un Centro de Operaciones de Seguridad (SOC) especializado en sistemas de IA.
    Tu tarea es analizar el siguiente lote de registros de auditoría en formato JSONL (JSON por línea) y detectar patrones de actividad sospechosos o anómalos.

    Busca patrones como:
    - Múltiples intentos de validación fallidos (`VALIDATION_FAILURE`) desde una misma fuente o en un corto período de tiempo.
    - Un pico inusual de errores (`ERROR` o `CRITICAL`).
    - Actividad repetitiva y rápida que podría indicar un ataque automatizado (bot).
    - Cualquier patrón que se desvíe de un comportamiento normal de uso.

    [LOGS DE AUDITORÍA]:
    {log_data}

    **INSTRUCCIONES DE FORMATO:**
    Analiza los logs y responde únicamente con el formato JSON solicitado.
    {format_instructions}
    """
    
    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # 4. Construir y ejecutar la cadena de supervisión
    chain = prompt | llm | parser
    report = chain.invoke({"log_data": logs_as_string})
    
    return report