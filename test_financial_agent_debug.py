#!/usr/bin/env python3
"""
Debug específico del agente financiero
"""

import asyncio
from dotenv import load_dotenv
from agents.azure_orchestrator import AzureOrchestrator
from agents.business_agents.financial_agent import analyze_financial_document

async def test_financial_agent():
    """Prueba específica del agente financiero"""
    
    load_dotenv()
    
    # Inicializar orchestrator
    orchestrator = AzureOrchestrator()
    success = await orchestrator.initialize()
    
    if not success:
        print("❌ Error al inicializar el orquestador")
        return
    
    print("🏦 PROBANDO AGENTE FINANCIERO")
    print("=" * 50)
    
    # Datos financieros de prueba
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
    
    print(f"📋 Datos financieros:")
    print(f"   {financial_data[:200]}...")
    
    try:
        print(f"\n🔄 Ejecutando análisis financiero...")
        result = await analyze_financial_document(orchestrator.azure_service, financial_data)
        
        print(f"\n📊 RESULTADO:")
        print(f"   ✅ Éxito: {result.success}")
        print(f"   🎫 Tokens: {result.tokens_used}")
        print(f"   💰 Solvencia: {result.solvencia}")
        print(f"   💧 Liquidez: {result.liquidez}")
        print(f"   📈 Rentabilidad: {result.rentabilidad}")
        print(f"   📊 Tendencia Ventas: {result.tendencia_ventas}")
        print(f"   📝 Resumen: {result.resumen_ejecutivo[:100]}...")
        
        # Verificar si hay problemas
        if result.solvencia == "N/A" or "N/A" in result.solvencia:
            print(f"\n🚨 PROBLEMA DETECTADO: Solvencia devuelve N/A")
        
        if result.liquidez == "N/A" or "N/A" in result.liquidez:
            print(f"🚨 PROBLEMA DETECTADO: Liquidez devuelve N/A")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

async def main():
    await test_financial_agent()

if __name__ == "__main__":
    asyncio.run(main())