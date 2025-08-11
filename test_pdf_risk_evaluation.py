"""
Script de prueba para evaluar riesgo financiero desde PDFs, redes sociales y referencias comerciales.
Permite cargar rutas de 2 PDFs, una URL de red social y texto de referencias comerciales.
"""

import asyncio
from agents.azure_orchestrator import AzureOrchestrator

def main():
    print("\n=== TEST DE EVALUACIÓN DE RIESGO DESDE PDFs ===")

    # Solicitar rutas de los PDFs
    pdf1 = input("Ruta del primer PDF: ").strip()
    pdf2 = input("Ruta del segundo PDF: ").strip()

    # Solicitar URL de red social
    social_media_url = input("URL de red social (opcional): ").strip()

    # Solicitar referencias comerciales
    commercial_references = input("Texto de referencias comerciales: ").strip()

    # Validar entradas
    if not pdf1 or not pdf2:
        print("❌ Debes proporcionar las rutas de ambos PDFs.")
        return

    # Ejecutar evaluación
    asyncio.run(run_evaluation(pdf1, pdf2, social_media_url, commercial_references))

async def run_evaluation(pdf1, pdf2, social_media_url, commercial_references):
    print("\n🚀 Inicializando orquestador...")
    orchestrator = AzureOrchestrator()
    await orchestrator.initialize()

    print("\n📂 Procesando PDFs y datos adicionales...")
    try:
        # Evaluar riesgo desde PDFs
        result = await orchestrator.evaluate_company_risk_from_pdfs(
            [pdf1, pdf2],
            company_name="Empresa de Prueba",
            user_id="console_user"
        )

        # Mostrar resultados
        print("\n=== RESULTADOS DE LA EVALUACIÓN ===")
        print(f"Empresa: {result.company_name}")
        print(f"Score Final: {result.final_score}")
        print(f"Nivel de Riesgo: {result.risk_level}")
        print(f"Tiempo de Procesamiento: {result.processing_time:.2f} segundos")
        print("\n--- Análisis Detallado ---")
        print("Análisis Financiero:", result.financial_analysis)
        print("Análisis Reputacional:", result.reputational_analysis)
        print("Análisis Comportamental:", result.behavioral_analysis)
        print("\n--- Reporte Consolidado ---")
        print(result.consolidated_report)

    except Exception as e:
        print(f"❌ Error durante la evaluación: {e}")

if __name__ == "__main__":
    main()
