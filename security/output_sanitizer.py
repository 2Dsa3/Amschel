# security/output_sanitizer.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class SanitizationResult(BaseModel):
    """
    Define la estructura de la respuesta del agente de sanitización de salidas.
    """
    is_safe: bool = Field(description="Debe ser 'true' si el texto original ya era seguro, y 'false' si se requirió alguna modificación.")
    sanitized_text: str = Field(description="El texto final, ya sea el original si era seguro, o la versión con la información sensible enmascarada.")
    details: str = Field(description="Una breve explicación de las acciones tomadas. Por ejemplo, 'No se encontraron problemas' o 'Se redactó 1 dirección de correo electrónico'.")

def sanitize_output(api_key: str, generated_text: str) -> SanitizationResult:
    """
    Analiza un texto generado por una IA para filtrar información sensible.
    """
    # 1. Instanciar el LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0, openai_api_key=api_key)

    # 2. Crear el parser de salida Pydantic
    parser = PydanticOutputParser(pydantic_object=SanitizationResult)

    # 3. Diseñar el "Meta-Prompt" de Cumplimiento y Privacidad
    prompt_template = """
    Eres un Oficial de Cumplimiento y Privacidad (DPO) de una institución financiera.
    Tu única tarea es analizar el [TEXTO GENERADO] por otra IA y asegurarte de que sea seguro y profesional.

    Revisa el texto en busca de lo siguiente:
    1.  **Información Personal Identificable (PII):** Nombres de personas, números de cédula, direcciones de correo electrónico, números de teléfono, direcciones físicas.
    2.  **Información Confidencial:** Nombres de usuario, contraseñas, claves de API, secretos de sistema.
    3.  **Lenguaje Inapropiado:** Contenido ofensivo, sesgado, discriminatorio o no profesional.

    **Acción a tomar:**
    - Si el texto es seguro y no contiene nada de lo anterior, devuélvelo sin cambios.
    - Si encuentras CUALQUIER información sensible, DEBES reemplazarla con un marcador genérico como `[DATO REDACTADO]`. NO la elimines, solo enmascárala.

    [TEXTO GENERADO]:
    {generated_text}

    **INSTRUCCIONES DE FORMATO:**
    Analiza el texto y responde únicamente con el formato JSON solicitado.
    {format_instructions}
    """
    
    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # 4. Construir y ejecutar la cadena de sanitización
    chain = prompt | llm | parser
    
    sanitization_result = chain.invoke({"generated_text": generated_text})
    
    return sanitization_result

