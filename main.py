# main.py (Versión de prueba para el BehavioralAgent)

import os
from dotenv import load_dotenv
from security import setup_logger
from business_agents.behavioral_agent import analyze_behavior

def test_behavioral_agent():
    """
    Prueba la funcionalidad del BehavioralAgent con datos de ejemplo.
    """
    load_dotenv()
    audit_logger = setup_logger()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: Clave API no encontrada.")
        return

    # --- Simulación de Texto con Referencias e Historial de Pagos ---
    ejemplo_texto_comportamental = """
    - Referencia de 'Aceros del Pacífico' (Proveedor, 3 años): 'Innovaciones Andinas es uno de nuestros mejores clientes. 
      Sus pagos son consistentemente puntuales, nunca hemos tenido un solo retraso. La comunicación es proactiva.'
    - Referencia de 'Logística Global' (Socio logístico, 1 año): 'Son muy organizados. A veces se demoran uno o dos días 
      en pagar la factura después del vencimiento, pero siempre pagan y avisan. Los consideramos un socio fiable.'
    - Historial de Pagos (últimos 12 meses): 10 de 12 facturas pagadas a tiempo. 2 facturas pagadas con 1-3 días de retraso. 
      Cero facturas impagas.
    """

    print("--- Probando el Agente BehavioralAgent ---")
    
    try:
        # Llamamos al agente con el texto de ejemplo
        resultado = analyze_behavior(api_key=api_key, behavioral_data_text=ejemplo_texto_comportamental)

        # Imprimimos el resultado estructurado
        print("\n--- INFORME DEL AGENTE DE COMPORTAMIENTO ---")
        print(f"📈 Patrón de Pago: {resultado.patron_de_pago}")
        print(f"🤝 Fiabilidad de Referencias: {resultado.fiabilidad_referencias}")
        print(f"📊 Riesgo Comportamental: {resultado.riesgo_comportamental}")
        print("\n📝 Resumen Ejecutivo:")
        print(resultado.resumen_ejecutivo)
        print("------------------------------------------")
        
        audit_logger.info({"agent": "BehavioralAgent", "action": "ANALYSIS_SUCCESS"})

    except Exception as e:
        print(f"❌ Error durante el análisis de comportamiento: {e}")
        audit_logger.error({"agent": "BehavioralAgent", "action": "ANALYSIS_ERROR", "error": str(e)})

if __name__ == "__main__":
    test_behavioral_agent()