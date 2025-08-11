#!/usr/bin/env python3
"""
Debug específico del agente financiero para identificar el problema de N/A
"""

import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv

from agents.azure_orchestrator import AzureOrchestrator
from agents.business_agents.financial_agent import analyze_financial_document

async def debug_financial_agent_detailed():
    """Debug detallado del agente financiero"""
    
    load_dotenv()
    
    print("🔍 DEBUG DETALLADO DEL AGENTE FINANCIERO")
    print("=" * 60)
    
    # Inicializar orchestrator
    orchestrator = AzureOrchestrator()
    success = await orchestrator.initialize()
    
    if not success:
        print("❌ Error al inicializar el orquestador")
        return
    
    print("✅ Orquestador inicializado correctamente")
    
    # Datos financieros de prueba (los mismos que están fallando)
    financial_data = """
    ESTADO FINANCIERO - MEGASTORE RETAIL CHAIN S.A.
    Período: Enero - Diciembre 2023
    
    BALANCE GENERAL:
    Activos Totales: $25,000,000
    - Activos Corrientes: $12,000,000
    - Efectivo: $2,500,000
    - Inventarios: $8,000,000
    - Cuentas por cobrar: $1,500,000
    - Activos Fijos: $13,000,000
    
    Pasivos Totales: $18,000,000
    - Pasivos Corrientes: $8,500,000
    - Deuda a largo plazo: $9,500,000
    
    Patrimonio: $7,000,000
    
    ESTADO DE RESULTADOS:
    Ingresos: $45,000,000
    Utilidad Neta: $1,800,000
    Flujo de Caja: $3,200,000
    Margen de Utilidad: 4%
    ROE: 25.7%
    Ratio Deuda/Patrimonio: 2.57
    """
    
    print(f"\n📋 Datos financieros de prueba:")
    print(f"   Longitud: {len(financial_data)} caracteres")
    print(f"   Primeras líneas: {financial_data[:200]}...")
    
    try:
        print(f"\n🔄 Ejecutando análisis financiero...")
        
        # Llamar directamente al agente financiero
        result = await analyze_financial_document(orchestrator.azure_service, financial_data)
        
        print(f"\n📊 RESULTADO DETALLADO:")
        print(f"   ✅ Éxito: {result.success}")
        print(f"   🎫 Tokens: {result.tokens_used}")
        
        print(f"\n📋 CAMPOS INDIVIDUALES:")
        print(f"   💰 Solvencia: '{result.solvencia}'")
        print(f"   💧 Liquidez: '{result.liquidez}'")
        print(f"   📈 Rentabilidad: '{result.rentabilidad}'")
        print(f"   📊 Tendencia Ventas: '{result.tendencia_ventas}'")
        print(f"   📝 Resumen: '{result.resumen_ejecutivo[:100]}...'")
        
        # Verificar si hay problemas específicos
        problems = []
        if result.solvencia == "N/A" or "N/A" in result.solvencia:
            problems.append("Solvencia devuelve N/A")
        if result.liquidez == "N/A" or "N/A" in result.liquidez:
            problems.append("Liquidez devuelve N/A")
        if result.rentabilidad == "N/A" or "N/A" in result.rentabilidad:
            problems.append("Rentabilidad devuelve N/A")
        
        if problems:
            print(f"\n🚨 PROBLEMAS DETECTADOS:")
            for problem in problems:
                print(f"   ❌ {problem}")
        else:
            print(f"\n✅ No se detectaron problemas con N/A")
            
    except Exception as e:
        print(f"\n❌ ERROR DURANTE ANÁLISIS:")
        print(f"   Error: {str(e)}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()

async def test_direct_api_call():
    """Prueba directa de la API para ver la respuesta raw"""
    
    print(f"\n🔧 PRUEBA DIRECTA DE API")
    print("-" * 40)
    
    load_dotenv()
    
    orchestrator = AzureOrchestrator()
    success = await orchestrator.initialize()
    
    if not success:
        print("❌ Error al inicializar")
        return
    
    # Crear request manual
    from agents.infrastructure_agents.services.azure_openai_service_enhanced import OpenAIRequest
    
    simple_prompt = """
    Analiza estos datos financieros:
    
    Activos: $25,000,000
    Pasivos: $18,000,000
    Patrimonio: $7,000,000
    Ingresos: $45,000,000
    
    Responde SOLO en JSON:
    {
        "solvencia": "análisis de solvencia",
        "liquidez": "análisis de liquidez",
        "rentabilidad": "análisis de rentabilidad",
        "tendencia_ventas": "análisis de ventas",
        "resumen_ejecutivo": "resumen"
    }
    """
    
    request = OpenAIRequest(
        request_id=f"debug_{datetime.now().strftime('%H%M%S')}",
        user_id="debug",
        agent_id="debug_financial",
        prompt=simple_prompt,
        max_tokens=800,
        temperature=0.1,
        timestamp=datetime.now()
    )
    
    try:
        print("📤 Enviando request a Azure OpenAI...")
        response = await orchestrator.azure_service.generate_completion(
            request,
            "Eres un analista financiero. Responde en JSON.",
            use_mini_model=False  # Usar GPT-4o
        )
        
        print(f"\n📥 RESPUESTA RAW:")
        print(f"   Tokens usados: {response.tokens_used}")
        print(f"   Tiempo: {response.processing_time_ms}ms")
        print(f"   Respuesta completa:")
        print(f"   {response.response_text}")
        
        # Intentar parsear JSON
        try:
            parsed = json.loads(response.response_text)
            print(f"\n✅ JSON PARSEADO CORRECTAMENTE:")
            for key, value in parsed.items():
                print(f"   {key}: {value}")
        except json.JSONDecodeError as e:
            print(f"\n❌ ERROR PARSEANDO JSON: {e}")
            print(f"   Respuesta no es JSON válido")
            
    except Exception as e:
        print(f"\n❌ ERROR EN API CALL: {str(e)}")
        import traceback
        traceback.print_exc()

async def test_with_different_models():
    """Prueba con diferentes modelos para ver si hay diferencia"""
    
    print(f"\n🤖 PRUEBA CON DIFERENTES MODELOS")
    print("-" * 40)
    
    load_dotenv()
    
    orchestrator = AzureOrchestrator()
    success = await orchestrator.initialize()
    
    if not success:
        return
    
    simple_data = "Activos: $100,000, Pasivos: $60,000, Patrimonio: $40,000"
    
    # Test con GPT-4o
    print("📊 Probando con GPT-4o...")
    try:
        result_gpt4 = await analyze_financial_document(orchestrator.azure_service, simple_data)
        print(f"   ✅ GPT-4o - Éxito: {result_gpt4.success}")
        print(f"   💰 Solvencia: {result_gpt4.solvencia[:50]}...")
    except Exception as e:
        print(f"   ❌ GPT-4o Error: {str(e)}")
    
    # Verificar estadísticas del servicio
    if hasattr(orchestrator.azure_service, 'get_service_stats'):
        stats = orchestrator.azure_service.get_service_stats()
        print(f"\n📈 ESTADÍSTICAS DEL SERVICIO:")
        print(f"   Total requests: {stats.get('total_requests', 0)}")
        print(f"   Successful: {stats.get('successful_requests', 0)}")
        print(f"   Rate limited: {stats.get('rate_limited_requests', 0)}")
        print(f"   Success rate: {stats.get('success_rate', 0):.1f}%")

async def main():
    """Función principal de debug"""
    print("🐛 INICIANDO DEBUG COMPLETO DEL AGENTE FINANCIERO")
    print("=" * 80)
    
    # Test 1: Debug detallado
    await debug_financial_agent_detailed()
    
    # Test 2: API call directa
    await test_direct_api_call()
    
    # Test 3: Diferentes modelos
    await test_with_different_models()
    
    print(f"\n🎯 DEBUG COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())